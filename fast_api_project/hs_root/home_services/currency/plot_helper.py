import io
import zoneinfo
import logging
from collections import OrderedDict
from datetime import date, datetime, timedelta
from io import BytesIO

import matplotlib.pyplot as plt
import pytz
from matplotlib.ticker import FormatStrFormatter
from sqlalchemy.orm import Session

from currency.crud import get_currency_rates_request_date, get_currency_rates
from config import (
    CURRENCY_PLOT_COLORS,
    CURRENCY_PLOT,
    NUMBER_DAY_FOR_PLOT,
    APP_LOGGER_NAME, TIME_ZONE,
)

app_logger = logging.getLogger(APP_LOGGER_NAME)


def split_request_dates(sorted_list: list, number_point: int) -> list:
    """
    Return the control points of the graph.
    """
    source_len = len(sorted_list)
    index_list = list()
    div_number = 1 if source_len // number_point == 0 else source_len // number_point
    for x in range(source_len):
        if x % div_number == 0:
            if len(index_list) < number_point - 1:
                index_list.append(x)

    # Added last index.
    index_list.append(source_len - 1)

    result_list = list()
    for index in index_list:
        result_list.append(sorted_list[index])

    return result_list


def remove_extra_keys(data: dict, number_point: int):
    """
    Remove the extra keys if it needs. Solving a time zone problem.
    """
    if len(data) > number_point:
        del_keys = list()
        for k, _ in data.items():
            extra_key = k - timedelta(days=1)
            if extra_key in data:
                del_keys.append(extra_key)

        if len(del_keys) > 0:
            for key in del_keys:
                data.pop(key)


def get_currency_rates_data(db: Session) -> dict:
    """
    Get currency rates dictionary.
    """

    data = {}
    current_tz = pytz.timezone(TIME_ZONE)

    try:
        currency_all_request_dates = get_currency_rates_request_date(db)

        rd = sorted(
            list(set([d[0].date() for d in currency_all_request_dates]))
        )

        if len(rd) < NUMBER_DAY_FOR_PLOT:
            return data

        request_dates = split_request_dates(rd, NUMBER_DAY_FOR_PLOT)

        for r_date in request_dates:
            start_date_time = datetime(
                r_date.year,
                r_date.month,
                r_date.day,
                0,
                0,
                0,
                tzinfo=zoneinfo.ZoneInfo(key="UTC"),
            )
            end_date_time = datetime(
                r_date.year,
                r_date.month,
                r_date.day,
                23,
                59,
                59,
                tzinfo=zoneinfo.ZoneInfo(key="UTC"),
            )
            currency_rate = get_currency_rates(db, start_date_time, end_date_time)

            if currency_rate:
                for curr in currency_rate:

                    utc_date = curr.request_date.replace(tzinfo=zoneinfo.ZoneInfo(key="UTC"))
                    current_date = utc_date.astimezone(current_tz)

                    if current_date.date() in data:
                        if str(curr.provider) in data[current_date.date()]:
                            if (
                                    str(curr.currency)
                                    in data[current_date.date()][str(curr.provider)]
                            ):
                                data[current_date.date()][str(curr.provider)][
                                    str(curr.currency)
                                ] = curr.amount
                            else:
                                data[current_date.date()][str(curr.provider)][
                                    str(curr.currency)
                                ] = curr.amount
                        else:
                            data[current_date.date()][str(curr.provider)] = {
                                str(curr.currency): curr.amount
                            }
                    else:
                        data[current_date.date()] = {
                            str(curr.provider): {str(curr.currency): curr.amount}
                        }

        # Remove the extra keys if it needs.
        remove_extra_keys(data, NUMBER_DAY_FOR_PLOT)

        return data

    except Exception as e:
        app_logger.error(f"Error when generating data for exchange rate chart: {e}")
        return data


def generate_plot(data: dict) -> BytesIO | None:
    """
    Generate a plot.
    """
    if not data:
        return None

    try:
        sorted_currency_dict = OrderedDict(sorted(data.items()))
        common_x = [date.strftime(d, "%d.%m.%Y") for d in sorted_currency_dict]
        # common_x = [d for d in sorted_currency_dict]
        plt.gca().cla()
        plt.gca().yaxis.set_major_formatter(FormatStrFormatter("%.2f"))
        plt.gcf().autofmt_xdate()

        for curr_name in CURRENCY_PLOT:
            currencylayer_y = []
            cbrf_y = []

            for value in sorted_currency_dict.values():
                for a, b in OrderedDict(sorted(value.items())).items():
                    if a == "Currencylayer":
                        currencylayer_y.append(b[curr_name])
                    elif a == "CBRF":
                        cbrf_y.append(b[curr_name])

            plt.plot(
                common_x,
                currencylayer_y,
                color=CURRENCY_PLOT_COLORS[curr_name],
                linestyle="dashed",
                linewidth=1,
                marker=".",
                markerfacecolor=CURRENCY_PLOT_COLORS[curr_name],
                markersize=5,
                label=f"Currencylayer: {curr_name}",
            )

            plt.plot(
                common_x,
                cbrf_y,
                color=CURRENCY_PLOT_COLORS[curr_name],
                linestyle="dashed",
                linewidth=1,
                marker=".",
                markerfacecolor=CURRENCY_PLOT_COLORS[curr_name],
                markersize=5,
                label=f"CBRF: {curr_name}",
            )

        plt.ylabel("Rate, rub")

        plt.title("Currency fluctuations")
        plt.legend()

        buf = io.BytesIO()
        plt.savefig(buf, format="jpg")
        buf.seek(0)

        return buf

    except Exception as e:
        app_logger.error(f"Error while generating currency rate chart: {e}")
        return None
