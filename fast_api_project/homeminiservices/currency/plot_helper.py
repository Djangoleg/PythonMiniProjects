import io
import zoneinfo
import logging
from collections import OrderedDict
from datetime import date, datetime
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


def find_middle(lst):
    if not lst:
        return None

    length = len(lst)  # Get the length of the list

    if length % 2 != 0:  # Check if the length is odd
        middle_index = length // 2
        return lst[middle_index]

    # If the length is even
    first_middle_index = length // 2 - 1
    second_middle_index = length // 2
    return lst[first_middle_index], lst[second_middle_index]


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

        request_dates = list()
        request_dates.append(rd[0])

        middle = find_middle(rd)
        if isinstance(middle, date):
            request_dates.append(middle)
        else:
            [request_dates.append(x) for x in middle]

        request_dates.append(rd[len(rd) - 1])

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
