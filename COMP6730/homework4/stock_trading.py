# coding: utf-8
## COMP1730/6730 S2 2022 - Homework 4
# Submission is due 09:00am, Monday the 19th of September, 2022.

## YOUR ANU ID: u7549569
## YOUR NAME: Tianyang Han

## You should implement one function stock_trade; you may define
## more functions if this will help you to achieve the functional
## correctness, and to improve the code quality of you program

import math

def stock_trade(stock_price, capital, p):
    """
    Trade and sell stocks following by the rules.

    Args:
        stock_price: A list of stock price each day (type: list)
        capital: Cash that can be traded at the moment (type: float)
        p: Proportion of capital to buy stocks and stocks to sell (type: float)

    Returns:
        The profit or loss at the end of trading. (type: float)
    """

    if (not(stock_price)):
        return 0.0
    ori_capital = capital
    capital = float(capital)
    num = 0.0             # numbers of shares
    for day in range(len(stock_price)):
        if day == 0:    # day 0 only do the purchase operation
            if can_buy(stock_price[day], capital, p):
                num, capital = buy(stock_price[day], capital, p, num)
            else:
                continue
        else:
            if stock_price[day] > stock_price[day-1]:   # sell the stock
                if can_sell((num * (1-p))//1):
                    num, capital = sell(stock_price[day], capital, p, num)
                else:
                    continue
            elif stock_price[day] < stock_price[day-1]:  # buy the stock
                if can_buy(stock_price[day], capital, p):
                    num, capital = buy(stock_price[day], capital, p, num)
                else:
                    continue
    # after finishing
    stock = stock_price[-1] * num       # current held stock part
    return (capital + stock) - ori_capital


def can_sell(num):
    """
    To identify if there is enough stock to sell

    Args:
        num: integer number of shares to be sold (type: float)

    Returns:
        Boolean: True means can sell, false means cannot sell
    """
    if num >= 1:        #whether the available sold stock is more than one share
        return True
    else:
        return False


def can_buy(stock_price, capital, p):
    """
    To identify if there is enough capital to buy stocks

    Args:
        stock_price: The stock price of the day (type: int)
        capital: Cash that can be traded at the moment (type: float)
        p: Proportion of capital to buy stocks and stocks to sell (type: float)

    Returns:
        Boolean: True means can buy, false means cannot buy
    """
    money = capital * round(1.0-p,2)
    num = money / stock_price
    if num>=1:              #whether the available capital can buy a share
        return True
    else:
        return False


def buy(stock_price, capital, p, num):
    """
    To buy stock with specific proportion capital

    Args:
        stock_price: The stock price of the day (type: int)
        capital: Cash that can be traded at the moment (type: float)
        p: Proportion of capital to buy stocks (type: float)
        num: integer number of shares held

    Returns:
        nun: integer number of shares held (type: float)
        capital: Cash that can be traded at the moment (type: float)
    """
    num += capital * round(1 - p,2) // stock_price
    capital -= stock_price * (capital * round(1 - p,2) // stock_price)
    return num,capital


def sell(stock_price, capital, p, num):
    """
    To sell stock with specific proportion shares

    Args:
        stock_price: The stock price of the day (type: int)
        capital: Cash that can be traded at the moment (type: float)
        p: Proportion of shares to sell (type: float), positive num between
        num: integer number of shares held

    Returns:
        nun: integer number of shares held (type: float)
        capital: Cash that can be traded at the moment (type: float)
    """
    capital += stock_price * ((num * round(1-p,2)) // 1)
    num = num - ((num * round(1-p,2)) // 1)  # the integer of num_sell_shares
    return num, capital


def test_stock_trade():
    ''' some typical trading situations but by no means exhaustive
    '''
    assert math.isclose( stock_trade([1,1,1,1,1], 100, 0.5), 0.0 )
    assert math.isclose( stock_trade([100, 50, 50], 10, 0.01), 0.0 )
    assert math.isclose( stock_trade([50, 100, 50], 10, 0.01), 0.0 )
    assert math.isclose( stock_trade([1,2,3,4,5], 2, 0.5), 5-1 )
    assert math.isclose( stock_trade(tuple(), 100, 0.5), 0.0 )
    assert math.isclose( stock_trade([1, 10, 2.0, 5.0], 50, 0.5), 268.0 )
    assert math.isclose( stock_trade([1, 10, 2.0, 2.0, 5.0, 5], 50, 0.5), 268.0 )


def test_stock_trade_more():
    ''' some typical trading situations but by no means exhaustive
    '''
    assert math.isclose( stock_trade([1, 100, 10, 10], 10, 0.9), 10-1 )
    assert math.isclose( stock_trade([], 100, 0.5), 0.0 )
    assert math.isclose( stock_trade(tuple(), 100, 0.5), 0.0 )
    print('all tests passed')

test_stock_trade()
test_stock_trade_more()

print(stock_trade((1, 10, 2.0, 2.0, 5.0, 5), 50, 0.5))