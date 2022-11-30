## COMP1730/6730 Homework 2

## YOUR ANU ID: u7549569
## YOUR NAME: Tianyang Han

## You should implement the function `combinations(n, k)` below.
## You can use the factorial function to help you, and the other
## functions to test that your solution works.

def combinations(n, k):
    '''
    Returns the number of ways to select k distinct elements from
    a set of size n (also known as 'n choose k').
    Assumption: n and k are non-negative integers, with 0 <= k <= n.
    The function must return an _integer_ value.
    '''
    ## The statement 'return 0' below is a place-holder: you
    ## should replace it with your implementation of the function.
    numerator = factorial(n)
    denominator = factorial(k) * factorial(n-k)
    result = numerator/denominator
    return int(result)

def factorial(n):
    '''
    Return the factorial of n (also known as 'n!').
    n must be a non-negative integer (0! is defined to be 1).

    Note: For the purpose of this homework assignment, you do
    not need to worry about how this function works; just trust
    that it does what it's supposed to, as long as you call it
    with the right kind of argument.
    '''
    f = 1
    while n > 0:
        f = n * f
        n = n - 1
    assert n == 0
    return f

def print_pascals_triangle(n):
    '''
    Print the numbers in the first n rows of Pascal's triangle
    (see https://en.wikipedia.org/wiki/Pascal%27s_triangle).
    This function can be used to test your implementation of the
    combinations function. If you have done it correctly, you
    should see an output like this:

    1
    1 1
    1 2 1
    1 3 3 1
    1 4 6 4 1

    and so on.

    Note: You should not modify this function, and you don't need
    to worry about how it works. Just use it to test your solution.
    '''
    for i in range(n):
        for j in range(i + 1):
            print(' ', combinations(i, j), end='')
        print() # new line after each row

def test_combinations():
    '''
    This function runs a number of tests of the combinations function.
    If it works ok, you will just see the output ("all tests passed") at
    the end when you call this function; if some test fails, there will
    be an error message.
    '''
    # simple test cases:
    assert combinations(5, 2) == 10
    assert type(combinations(5, 2)) is int
    assert combinations(5, 3) == 10
    assert type(combinations(5, 3)) is int
    # how to pick 2, 3, or 4 tutors from 23:
    assert combinations(23, 2) == 253
    assert combinations(23, 3) == 1771
    assert combinations(23, 4) == 8855
    # number of possible 5-card hands from a deck of 52 cards:
    assert combinations(52, 5) == 2598960
    # some edge cases:
    assert combinations(0, 0) == 1
    assert type(combinations(0, 0)) is int
    assert combinations(1, 0) == 1
    assert type(combinations(1, 0)) is int
    assert combinations(1, 1) == 1
    assert type(combinations(1, 1)) is int
    assert combinations(100, 0) == 1
    assert type(combinations(100, 0)) is int
    assert combinations(100, 100) == 1
    assert type(combinations(100, 100)) is int
    print("all tests passed")



test_combinations()