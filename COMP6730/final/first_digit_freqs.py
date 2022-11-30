# COMP1730 S2 2022 - final exam

# Implement the function first_digit_freqs below.
# (The statements there are just a dummy code that doesn't solve the problem:
# you should replace it with your solution.)
# You can define other functions if it helps you decompose and solve
# the problem.
# The function is_equal is a part of the testing code, you don't need to
# change it.
# Do NOT use global variables!
# Do NOT import any module that you do not use!


def first_digit_freqs(b, n):
    '''Computes and returns frequencies of the first digits in b^i, i=1..n sequence'''
    freqs = {k:v for k,v in zip(range(1,10), [0]*9)}
    lst = []
    for i in range(n):
        lst.append(int(str(b**i)[0]))       # get first digit for all the element and add to the list
    for j in lst:
        freqs[j]+=1
    return freqs

def test_first_digit_freqs():
    d1 =  {1: 3, 2: 2, 3: 1, 4: 1, 5: 1, 6: 1, 7: 0, 8: 1, 9: 0}
    assert first_digit_freqs(2, 10) == d1
    d2 = {1: 29, 2: 19, 3: 12, 4: 8, 5: 8, 6: 7, 7: 7, 8: 5, 9: 5}
    assert first_digit_freqs(3, 100) == d2
    d3 = {1: 15, 2: 8, 3: 7, 4: 5, 5: 4, 6: 3, 7: 4, 8: 1, 9: 3}
    assert first_digit_freqs(7, 50) == d3

    print('all tests passed')

