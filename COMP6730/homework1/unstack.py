# COMP1730/6730 Homework 1.

## YOUR ANU ID: u7549569
## YOUR NAME: Tianyang Han

import robot

## Functions to move right and left by two spaces.
def right_two_spaces():
    robot.drive_right()
    robot.drive_right()

def left_two_spaces():
    robot.drive_left()
    robot.drive_left()

## Perform an unstacking manoeuvre.
## Assumption: At the start of the manoeuvre, the robot (gripper) is
## in front of the stack, at the base of the stack, and the gripper
## is folded back.
def unstack_to_the_left():
    # Step 1: Grasp the next block above the base.
    grasp_blocks_above()
    # Step 2: Move to the left.
    left_two_spaces()
    # Step 3: put down the block(s) we're holding, and re-position
    # the gripper so that we can repeat the manoeuvre in front of
    # the blocks that were put down.
    put_down_blocks()

## Raise gripper and grasp the block one level up.
## Assumption: Gripper is folded and lift is at base level.
def grasp_blocks_above():
    robot.gripper_to_open()
    robot.lift_up()
    robot.gripper_to_closed()

## Put down the blocks we're holding, and position gripper to
## repeat the unstacking manoeuvre.
## Assumption: The gripper is one level up, holding one or more blocks.
def put_down_blocks():
    # Move the lift down, and release the blocks.
    robot.lift_down()
    robot.gripper_to_open()
    # Because there is now a block to the right (the one that we
    # unstacked from), we must do the up-fold-down manoeuvre.
    robot.lift_up()
    robot.gripper_to_folded()
    robot.lift_down()

## Unstack a tower of two blocks.
## Assumption: The robot starts in front of the left position, and
## the tower to be unstacked is in the middle.
def unstack_tower_of_two():
    # Move to the middle
    right_two_spaces()
    # and do the unstacking manoeuvre
    unstack_to_the_left()

## Unstack a tower of three blocks.
## Assumption: The robot starts in front of the left position, and
## the tower to be unstacked is in the right-most position (so that
## there is enough space to the left of it to unstack it).
def unstack_tower_of_three():
    # Move to the right-most stack
    right_two_spaces()
    right_two_spaces()
    # and do the unstacking manoeuvre twice
    unstack_to_the_left()

    ########################################
    # answer code, gripper_state:open
    robot.lift_up()
    robot.gripper_to_closed()    # grasp the top box
    left_two_spaces()   # move to position 0
    robot.lift_down()
    # robot.lift_up()
    # robot.gripper_to_open()   # place the box on height 0
    # robot.gripper_to_folded()  # reset the gripper



################################################################################
#               DO NOT MODIFY ANYTHING BELOW THIS POINT
################################################################################    

def test_unstack_two():
    # Set up a simulation with a tower of two boxes in the middle:
    robot.init(pos = 0, boxes = [[], [], ["red", "green"], [], []])
    # Test the unstacking-of-two function:
    unstack_tower_of_two()

def test_unstack_three():
    # Set up a simulation with a tower of three boxes to the right
    robot.init(pos = 0, boxes = [[], [], [], [], ["red", "green", "blue"]])
    # Test the unstacking-of-three function:
    unstack_tower_of_three()

if __name__ == "__main__" :
    #test_unstack_two()
    test_unstack_three()

a = True
result_list = []
print('What do you need to buy?')
while (a):
    food = input()
    if food !="":
        result_list.append(food)
    else:
        a = False
print(result_list)
