# coding: utf-8
## COMP1730/6730 S2 2022 - Homework 5
# Submission is due 09:00am, Monday the 3rd of October, 2022.

## YOUR ANU ID: u7549569
## YOUR NAME: Tianyang Han

## You should implement one function stock_trade; you may define
## more functions if this will help you to achieve the functional
## correctness, and to improve the code quality of you program

from math import dist, cos, sin, atan2


def advance_position(r, v):
    '''from the current position r advance to the position
    at the next iteration: r -> r + v
    (maybe I do not need this function?)
    '''
    return (r[0] + v[0], r[1] + v[1]) 


def check_contact(r1, r2, tol):
    ''' returns True if points r1 and r2 are withing tol distance from each other'''
    return dist(r1, r2) < tol


def get_chaser_direction(chaser_pos, target_pos):
    """
    return direction of next chaser move based on its current position,
    and position of the target (all positions are x, y tuples)
    """
    chaser_x, chaser_y = chaser_pos
    target_x, target_y = target_pos
    delta_x = target_x - chaser_x
    delta_y = target_y - chaser_y
    angle = atan2(delta_y, delta_x)
    return (cos(angle), sin(angle))

def chaser_crossed_target(chaser_pos, next_chaser_pos,
                          target_pos, next_target_pos):
    '''
    return True if chaser and target paths cross
    Assumes the target will only travel in a horizontal direction
    '''
    Ax1, Ay1 = chaser_pos
    Ax2, Ay2 = next_chaser_pos
    Bx1, By1 = target_pos
    Bx2, By2 = next_target_pos    

    assert By1 == By2, \
            "chaser_crossed_target: target must travel in a horizontal direction"

    if Ax1 == Ax2: #vertical
        if Bx1 > Bx2:  Bx1, Bx2 = Bx2, Bx1
        return Bx1 <= Ax1 <= Bx2

    if Ay1 == Ay2: #horizontal
        if Ay1 != By1:
            return False
        else:
            if Ax1 > Ax2:  Ax1, Ax2 = Ax2, Ax1
            if Bx1 > Bx2:  Bx1, Bx2 = Bx2, Bx1
            return min(Ax2, Bx2) >= max(Ax1, Bx1)

    m = (Ay2 - Ay1) / (Ax2 - Ax1)
    c = Ay1 - m * Ax1
    x = (By1 - c) / m       
    if Ax1 > Ax2:  Ax1, Ax2 = Ax2, Ax1
    if Bx1 > Bx2:  Bx1, Bx2 = Bx2, Bx1
    return (Ax1 <= x <= Ax2) and (Bx1 <= x <= Bx2)


def chase(target_speed, chaser_speed, chaser_pos, max_steps, catching_dist=1e-5):
    '''
    return True if chaser chases target within max_steps time.
    Including the situation "catch on the flight"
    '''
    target_pos = (0,0)
    for i in range(max_steps+1):    # use max+1 instead of max
        if check_contact(chaser_pos, target_pos,catching_dist):         # check at the end of last step catch
            return True

        (cosv, sinv) = get_chaser_direction(chaser_pos, ((i+1) * target_speed, 0))  # next timestep direction
        if i<max_steps:    # not take account of last step as code below have already concerned
            if cosv==-1 and chaser_pos[1] == 0 and (0 < chaser_pos[0] - target_pos[0]) < (chaser_speed + target_speed): return True

            # chaser_pos
            # target_pos
            # chaser_pos_next = (chaser_pos[0]+chaser_speed*cosv, chaser_pos[1]+chaser_speed*sinv)
            # target_pos_next = ((i+1) * target_speed, 0)
            # if at the end of this step after moving, path cross
            if chaser_crossed_target(chaser_pos,(chaser_pos[0]+chaser_speed*cosv, chaser_pos[1]+chaser_speed*sinv),
                                     target_pos,((i+1) * target_speed, 0)):
                if chaser_pos[1]==0:        # chaser at x axis
                    if ((chaser_pos[0]-target_pos[0])*((chaser_pos[0]+chaser_speed*cosv)*((i+1) * target_speed)))<0:  # chaser behind target
                        return True
                    if cosv == 1 and (0 < chaser_pos[0] - target_pos[0]) < (chaser_speed + target_speed): return True  # chaser towards target

        target_pos = ((i+1) * target_speed, 0)      # finish moving at this timestep
        chaser_pos = (chaser_pos[0]+chaser_speed*cosv, chaser_pos[1]+chaser_speed*sinv)
    return False


    
def test_chase_1():
    # generic cases (low precision, should work even if no "catch-on-the-fly" check is used)
    assert not chase(100,10,(10,10),100)
    assert chase(10,11,(10,10),20, catching_dist=0.5)
    assert chase(1.0,1.1,(10,10),50, catching_dist=0.1)
    assert not chase(100,10,(10,10),100)
    print('All tests 1 passed')

def test_chase_2():
    # degenerate (boundary, corner) cases
    assert not chase(10, 5, (5,5), 100) # slow chaser too far from the line -- never catches
    assert chase(5, 10, (-10,0), 20) # fast chaser behind target -- will catch given enough steps
    assert not chase(5, 6, (-10,0), 4) # fast chaser behind target -- won't catch since not enough steps
    assert chase(5, 6, (-10,0), 10) # fast chaser behind target -- will catch at the very end
    print('All tests 2 passed')

test_chase_1()
test_chase_2()
print(chase(5,1,(-1,0),1))
print(chase(0.5,2,(1,0),1))
print(chase(5,3,(1,0),1))
print(chase(2,0.5,(1,0),1))
