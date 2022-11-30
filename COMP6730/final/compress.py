#  COMP1730 S2 2022 - final exam

# Implement the function compress below.
# (The return statement there is a dummy code that doesn't solve the problem:
# you should replace it.)
# You can define other functions if it helps you decompose and solve
# the problem.
# Do NOT use global variables!
# Do NOT import any module that you do not use!

def compress(str1):
    # write your implementation here
    if str1=='':return ''
    start = str1[0]
    count = 1
    res = ""
    if len(str1)==1:
        res += str1[0]
        return res
    for i in range(1,len(str1)):
        if str1[i] == start:
            count+=1
        else:
            if count==1:
                res+=start
            else:
                res+=start+str(count)
            count=1
            start=str1[i]
    if count>1:
        res= res+ str1[len(str1)-1]+str(count)
    else:
        res = res+ str1[len(str1)-1]
    return res # replace with compressed string

def test_number_to_string():
    assert compress('') == ''
    assert compress('R') == 'R'
    assert compress('RR') == 'R2'
    assert compress('RRR') == 'R3'
    assert compress('LLLRL') == 'L3RL'
    assert compress('RLRLRLRLR') == 'RLRLRLRLR'
    assert compress('RLRLRLRLRL') == 'RLRLRLRLRL'
    assert compress('RLRRRRRRLRRLL') == 'RLR6LR2L2'
    assert compress('RLLRRRRRRRRRRRRRRRLR') == 'RL2R15LR'

    print('all tests passed')

