import random
import string
import zoneinfo
from collections import OrderedDict
from datetime import date, datetime

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

from currency.models import CurrencyRate
from config import (
    CURRENCY_PLOT_COLORS,
    CURRENCY_PLOT,
    CURRENCY_PLOT_FILE_PATH,
)

NUMBER_DAY_FOR_PLOT = 3


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


def get_currency_rates_data() -> dict:
    """
    Get currency rates dictionary.
    """

    data = {}

    currency_all_request_dates = (
        CurrencyRate.objects.all()
        .order_by("requestDate")
        .values("requestDate")
        .distinct()
    )

    rd = sorted(
        list(set([d["requestDate"].date() for d in currency_all_request_dates]))
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
        currency_rate = CurrencyRate.objects.filter(
            requestDate__range=(start_date_time, end_date_time)
        )
        if currency_rate:
            for curr in currency_rate:
                if curr.requestDate.date() in data:
                    if str(curr.provider) in data[curr.requestDate.date()]:
                        if (
                            str(curr.currency)
                            in data[curr.requestDate.date()][str(curr.provider)]
                        ):
                            data[curr.requestDate.date()][str(curr.provider)][
                                str(curr.currency)
                            ] = curr.amount
                        else:
                            data[curr.requestDate.date()][str(curr.provider)][
                                str(curr.currency)
                            ] = curr.amount
                    else:
                        data[curr.requestDate.date()][str(curr.provider)] = {
                            str(curr.currency): curr.amount
                        }
                else:
                    data[curr.requestDate.date()] = {
                        str(curr.provider): {str(curr.currency): curr.amount}
                    }

    return data


def generate_plot(data: dict) -> str:
    """
    Generate a plot.
    """

    if not data:
        return "Unknown"

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

    salt = "".join(random.choices(string.ascii_lowercase + string.digits, k=7))
    file_path = CURRENCY_PLOT_FILE_PATH + "curr_plot_" + salt + ".jpg"
    plt.savefig(file_path)
    return file_path
