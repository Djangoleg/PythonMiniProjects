from collections import OrderedDict
from datetime import date

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

CURRENCY_DICT = {
    date(2023, 10, 1): {
        'currencylayer': {
            'USD': 91.3503,
            'EUR': 100.0276
        },
        'cbrf': {
            'USD': 90.3503,
            'EUR': 99.0276
        }
    },
    date(2023, 10, 2): {
        'currencylayer': {
            'USD': 92.3503,
            'EUR': 101.0276
        },
        'cbrf': {
            'USD': 91.3503,
            'EUR': 100.0276
        }
    },
    date(2023, 10, 3): {
        'currencylayer': {
            'USD': 93.3503,
            'EUR': 102.0276
        },
        'cbrf': {
            'USD': 92.3503,
            'EUR': 101.0276
        }
    }
}

# CURRENCIES = ['USD', 'EUR', 'GBP', 'RUB', 'UAH', 'CNY']
CURRENCIES = ['USD', 'EUR']
CURR_COLORS = {'USD': 'green', 'EUR': 'red'}


def generate_graf(currency: dict):
    sorted_currency_dict = OrderedDict(sorted(currency.items()))

    common_x = [date.strftime(d, '%d.%m.%Y') for d in sorted_currency_dict]

    print(*common_x)

    # x_limit = (min(common_x), max(common_x))
    # y_limit = (80.0001, 110.0001)

    plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

    plt.gcf().autofmt_xdate()

    for curr_name in CURRENCIES:

        currencylayer_y = []
        cbrf_y = []

        for value in sorted_currency_dict.values():
            for a, b in OrderedDict(sorted(value.items())).items():
                if a == 'currencylayer':
                    currencylayer_y.append(b[curr_name])
                elif a == 'cbrf':
                    cbrf_y.append(b[curr_name])

        print(f'currencylayer: {curr_name}', *currencylayer_y, CURR_COLORS[curr_name])
        print(f'cbrf: {curr_name}', *cbrf_y, CURR_COLORS[curr_name])

        plt.plot(common_x, currencylayer_y, color=CURR_COLORS[curr_name], linestyle='dashed', linewidth=1,
                 marker='.', markerfacecolor=CURR_COLORS[curr_name], markersize=5,
                 label=f'Currencylayer: {curr_name}')

        plt.plot(common_x, cbrf_y, color=CURR_COLORS[curr_name], linestyle='dashed', linewidth=1,
                 marker='.', markerfacecolor=CURR_COLORS[curr_name], markersize=5, label=f'CBRF: {curr_name}')

    # plt.ylim(y_limit)
    # plt.xlim(x_limit)

    # plt.xlabel('Date')
    plt.ylabel('Rate, rub')

    plt.title('Currency fluctuations')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    generate_graf(CURRENCY_DICT)
