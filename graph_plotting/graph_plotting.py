from collections import OrderedDict
from datetime import date
from decimal import Decimal

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

CURRENCY_DICT_NEW = {
    date(2024, 2, 4): {
        'Currencylayer': {
            'EUR': Decimal('98.35'),
            'GBP': Decimal('114.97'),
            'USD': Decimal('91.00'),
            'UAH': Decimal('2.41'),
            'CNY': Decimal('12.78')
        },
        'CBRF': {
            'USD': Decimal('90.66'),
            'EUR': Decimal('98.64'),
            'GBP': Decimal('114.98'),
            'UAH': Decimal('2.41'),
            'CNY': Decimal('12.60')
        }
    },
    date(2024, 2, 3): {
            'Currencylayer': {
                'EUR': Decimal('98.35'),
                'GBP': Decimal('114.97'),
                'USD': Decimal('91.00'),
                'UAH': Decimal('2.41'),
                'CNY': Decimal('12.78')},
            'CBRF': {
                'USD': Decimal('90.66'),
                'EUR': Decimal('98.64'),
                'GBP': Decimal('114.98'),
                'UAH': Decimal('2.41'),
                'CNY': Decimal('12.60')}
    },
    date(2024, 1, 27): {
        'Currencylayer': {
            'EUR': Decimal('96.69'),
            'GBP': Decimal('113.11'),
            'UAH': Decimal('2.35'),
            'CNY': Decimal('12.54'),
            'USD': Decimal('89.00')
        },
        'CBRF': {
            'USD': Decimal('89.52'),
            'EUR': Decimal('97.09'),
            'GBP': Decimal('113.69'),
            'UAH': Decimal('2.38'),
            'CNY': Decimal('12.44')
        }
    }
}

# CURRENCIES = ['USD', 'EUR', 'GBP', 'RUB', 'UAH', 'CNY']
CURRENCIES = ['USD', 'EUR']
CURR_COLORS = {'USD': 'green', 'EUR': 'red'}


def generate_graf(currency: dict):
    sorted_currency_dict = OrderedDict(sorted(currency.items()))
    # common_x = [date.strftime(d, "%d.%m.%Y") for d in sorted_currency_dict]
    common_x = [d for d in sorted_currency_dict.keys()]
    # Clear figure.
    plt.gca().cla()
    plt.gca().yaxis.set_major_formatter(FormatStrFormatter("%.2f"))
    plt.gcf().autofmt_xdate()

    print(*common_x)

    for curr_name in CURRENCIES:

        currencylayer_y = []
        cbrf_y = []

        for value in sorted_currency_dict.values():
            for a, b in OrderedDict(sorted(value.items())).items():
                if a == 'Currencylayer':
                    currencylayer_y.append(b[curr_name])
                elif a == 'CBRF':
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
    generate_graf(CURRENCY_DICT_NEW)

