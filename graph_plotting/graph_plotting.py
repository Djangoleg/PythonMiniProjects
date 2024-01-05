import matplotlib.pyplot as plt


def get_limits(currencylayer: list, cbrf: list):
    sum_list = set(currencylayer)
    [sum_list.add(x) for x in cbrf]
    return min(sum_list) - 1, max(sum_list) + 1


def generate_graf(currencylayer_x: list, currencylayer_y: list, cbrf_x: list, cbrf_y: list):
    plt.plot(currencylayer_x, currencylayer_y, color='green', linestyle='dashed', linewidth=2,
             marker='o', markerfacecolor='blue', markersize=10, label='Currencylayer')

    plt.plot(cbrf_x, cbrf_y, color='red', linestyle='dashed', linewidth=2,
             marker='o', markerfacecolor='brown', markersize=10, label='CBRF')

    plt.ylim(get_limits(currencylayer_x, cbrf_x))
    plt.xlim(get_limits(currencylayer_y, cbrf_y))

    plt.xlabel('Date')
    plt.ylabel('Cost')

    plt.title('Dollar fluctuations')
    plt.legend()
    plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    currencylayer_x = [1, 2, 3, 4, 5, 6]
    currencylayer_y = [2, 4, 1, 5, 2, 6]

    cbrf_x = [1, 2, 3, 4, 5, 6]
    cbrf_y = [1, 3, 0, 4, 1, 5]

    generate_graf(currencylayer_x=currencylayer_x, currencylayer_y=currencylayer_y,
                  cbrf_x=cbrf_x, cbrf_y=cbrf_y)
