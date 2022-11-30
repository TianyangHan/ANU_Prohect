# COMP1730 S2 2022 - final exam

# Implement the function min_difference below.
# (The statement "return 0.0" is just a dummy implementation: you
# should replace it with your code.)
# You can define other functions if it helps you decompose and solve
# the problem.
# Do NOT use global variables!
# Do NOT import any module that you do not use!
import numpy as np

def min_difference(L):
    if len(L) == 0 or len(L)==1: return 0
    length1 = len(L)
    res_list = []
    for i in L:
        if len(i) == 0:
            return 0

    for i in range(length1-1):
        for j in range(i+1,length1):
            tmp = np.array(L[i]) - np.array(L[j])
            tmp = [abs(ele) for ele in tmp]
            res_list.append(np.sum(tmp))
    return min(res_list)

def test_min_difference():
    '''
    This function runs a number of tests of the min_difference function.
    If it works ok, you will just see the output ("all tests passed") at
    the end when you call this function; if some test fails, there will
    be an error message.
    '''

    assert min_difference([]) == 0
    assert min_difference([[]]) == 0
    assert min_difference([[1, 2]]) == 0
    assert min_difference([[], []]) == 0
    assert min_difference([ [1.2] ]) == 0
    assert abs(min_difference([ [1.2], [2.3] ]) - 1.1) < 1e-6
    assert min_difference([[1, 0, -5, 2], [4, -2, 3, 1]]) == 14
    assert min_difference([[1, 0, -5, 2], [-3, 7, -1, 0]]) == 17
    assert min_difference([[4, -2, 3, 1], [-3, 7, -1, 0]]) == 21
    assert min_difference([ [1, 0, -5, 2], [4, -2, 3, 1], [-3, 7, -1, 0] ]) == 14

    print('all tests passed')


