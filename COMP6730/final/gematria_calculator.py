# COMP1730 S2 2022 - final exam

# Implement the function gematria_calculator below.
# (The statement "return 0" is just a dummy code that does not solve the problem:
# you should replace it with your solution.)
# You can define other functions if it helps you decompose and solve
# the problem.
# Do NOT use global variables!
# Do NOT import any module that you do not use!

def gematria_calculator(word, letter_vals):
    new_word = word.lower()
    res = 0;
    for i in new_word:
        if i not in letter_vals: continue
        if(letter_vals[i] is not None):
            res+=letter_vals[i]
    return res



def test_gematria_calculator():
    letter_vals = {'a':1, 'b':2, 'c':3, 'd':4, 'e':15, 'f':80, 'g':3,
                   'h':8, 'i':10, 'j':20, 'k':30, 'l':330, 'm':40, 'n':50, 'o':70,
                   'p':80, 'q':100, 'r':200, 's':300, 't':400, 'u':6, 'v':6, 'w':800,
                   'x':60, 'y':10, 'z':7}
    assert gematria_calculator('Napoleon', letter_vals) == 666
    letter_vals['t'] = 287
    letter_vals.pop('r')
    assert gematria_calculator('Great Britain', letter_vals) == 666
    assert gematria_calculator('parousia', {'a':200, 'z':1000, 's':300, 'i':50, 'o':20, 'p':4, 'r':3}) == 777

    print('all tests passed')

