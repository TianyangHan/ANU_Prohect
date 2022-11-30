
from __future__ import print_function
from __future__ import division

###
# Robot interface

def init(ip_address = None, visualise = True, width = 5, height = 2,
         pos = -1, boxes = [["red"], [], ["green"], [], ["blue"]]):
    '''Initialise (or re-initialise) the robot interface or simulation.
    For the simulator, optional arguments are width (integer > 0),
    height (integer > 0), boxes (list of lists of color names, or
    string naming a particular initial arrangement, such as "random")
    and visualise (True or False). The ip_address argument should only
    be used when initialising the interface to the physical robot.'''
    global _robot
    if ip_address is not None:
        _robot = _RPCRobot(ip_address)
    else:
        _robot = _SimRobot(visualise, width, height, pos, boxes)

def drive_right():
    '''Drive robot one step to the right. Note that if the gripper
    is not folded (open or closed), this may cause a collision.'''
    if _robot is None:
        raise RobotError("The robot has not been initialised.")
    _robot.drive_right()

def drive_left():
    '''Drive robot one step to the left. Note that if the gripper
    is not folded (open or closed), this may cause a collision.'''
    if _robot is None:
        raise RobotError("The robot has not been initialised.")
    _robot.drive_left()

def lift_up():
    '''Move the lift one step up.'''
    if _robot is None:
        raise RobotError("The robot has not been initialised.")
    _robot.lift_up()

def lift_down():
    '''Move the lift one step down. Note that if the gripper is not
    folded (open or closed), this may cause a collision.'''
    if _robot is None:
        raise RobotError("The robot has not been initialised.")
    _robot.lift_down()

def gripper_to_open():
    '''Move the gripper to the open position (regardless of
    current position). If the gripper is currently folded, this
    may cause a collision.'''
    if _robot is None:
        raise RobotError("The robot has not been initialised.")
    _robot.gripper_to_open()

def gripper_to_closed():
    '''Move the gripper to the closed position (regardless of
    current position). If the gripper is currently folded, this
    may cause a collision.'''
    if _robot is None:
        raise RobotError("The robot has not been initialised.")
    _robot.gripper_to_closed()

def gripper_to_folded():
    '''Move the gripper to the folded position (regardless of
    current position). This may cause a collision.'''
    if _robot is None:
        raise RobotError("The robot has not been initialised.")
    _robot.gripper_to_folded()

def sense_color():
    '''Get a reading from the color sensor. Returns the name of
    the color as a string, or an empty string ("") if no box is
    detected.'''
    if _robot is None:
        raise RobotError("The robot has not been initialised.")
    return _robot.sense_color()

def print_state():
    _robot.print_state()

###
# Everything below is internal to the robot implementation.

import sys
import time
import math

_robot = None

class _RPCRobot:
    '''Robot class interfacing with ev3 via RPYC.'''
    DEFAULT_DRIVE_RIGHT = 575
    DEFAULT_DRIVE_LEFT = 600
    DEFAULT_LIFT_UP = 220
    DEFAULT_LIFT_DOWN = 200

    def __init__(self, ip_address = "192.168.0.1"):
        import rpyc

        self.rpcconn = rpyc.classic.connect(ip_address)
        self.ev3 = self.rpcconn.modules.ev3dev.ev3
        self.battery = self.ev3.PowerSupply()
        self.drive = self.ev3.LargeMotor('outB')
        self.lift = self.ev3.LargeMotor('outD')
        self.gripper = self.ev3.MediumMotor('outC')
        self.sensor = self.ev3.ColorSensor()
        self.proxor = self.ev3.InfraredSensor()

    def print_state(self):
        print("drive at " + str(self.drive.position))
        print("lift at " + str(self.lift.position))
        print("gripper at " + str(self.gripper.position))
        print("sensor read: " + str(self.sensor.value()))
        print("proxor read: " + str(self.proxor.value()))
        print("battery: " + str(self.battery.measured_volts) + "V, "
              + str(self.battery.measured_amps) + "A")

    # moving up doesn't require braking
    def lift_up(self, distance=DEFAULT_LIFT_UP):
        print("lift at " + str(self.lift.position)
              + ", speed " + str(self.lift.speed))
        self.lift.run_to_rel_pos(position_sp = -distance, duty_cycle_sp = -25)
        time.sleep(0.5)
        while abs(self.lift.speed) > 0:
            print("lift at " + str(self.lift.position)
                  + ", speed " + str(self.lift.speed))
            time.sleep(0.25)
        print("(end) lift at " + str(self.lift.position)
              + ", speed " + str(self.lift.speed))

    # moving down requires braking, and even then has to be commanded ~10 short
    def lift_down(self, distance=DEFAULT_LIFT_DOWN):
        print("lift at " + str(self.lift.position)
              + ", speed " + str(self.lift.speed))
        self.lift.run_to_rel_pos(position_sp = distance,
                                 duty_cycle_sp = 25,
                                 stop_command='brake')
        time.sleep(0.5)
        while abs(self.lift.speed) > 0:
            print("lift at " + str(self.lift.position)
                  + ", speed " + str(self.lift.speed))
            time.sleep(0.25)
        print("(end) lift at " + str(self.lift.position)
              + ", speed " + str(self.lift.speed))

    def drive_right(self, distance = DEFAULT_DRIVE_RIGHT):
        print("drive at " + str(self.drive.position)
              + ", speed " + str(self.drive.speed))
        self.drive.run_to_rel_pos(position_sp = distance,
                                  duty_cycle_sp = 50,
                                  stop_command='hold')
        time.sleep(0.5)
        while abs(self.drive.speed) > 0:
            print("drive at " + str(self.drive.position)
                  + ", speed " + str(self.drive.speed))
            time.sleep(0.25)
        print("(end) drive at " + str(self.drive.position)
              + ", speed " + str(self.drive.speed))

    def drive_left(self, distance = DEFAULT_DRIVE_LEFT):
        print("drive at " + str(self.drive.position)
              + ", speed " + str(self.drive.speed))
        self.drive.run_to_rel_pos(position_sp = -distance,
                                  duty_cycle_sp = -50,
                                  stop_command='hold')
        time.sleep(0.5)
        while abs(self.drive.speed) > 0:
            print("drive at " + str(self.drive.position)
                  + ", speed " + str(self.drive.speed))
            time.sleep(0.25)
        print("(end) drive at " + str(self.drive.position)
              + ", speed " + str(self.drive.speed))

    def gripper_to_closed(self):
        print("gripper at " + str(self.gripper.position)
              + ", speed " + str(self.gripper.speed))
        if self.gripper.position > -1900:
            dc = -50
        else:
            dc = 50
        self.gripper.run_to_abs_pos(position_sp = -1900, duty_cycle_sp = dc)
        time.sleep(0.5)
        while abs(self.gripper.speed) > 0:
            print("gripper at " + str(self.gripper.position)
                  + ", speed " + str(self.gripper.speed))
            time.sleep(0.25)
        print("(end) gripper at " + str(self.gripper.position)
              + ", speed " + str(self.gripper.speed))

    def gripper_to_open(self):
        print("gripper at " + str(self.gripper.position)
              + ", speed " + str(self.gripper.speed))
        if self.gripper.position > -1500:
            dc = -100
        else:
            dc = 100
        self.gripper.run_to_abs_pos(position_sp = -1500,
                                    duty_cycle_sp = dc,
                                    stop_command='brake')
        time.sleep(0.5)
        while abs(self.gripper.speed) > 0:
            print("gripper at " + str(self.gripper.position)
                  + ", speed " + str(self.gripper.speed))
            time.sleep(0.25)
        print("(end) gripper at " + str(self.gripper.position)
              + ", speed " + str(self.gripper.speed))

    def gripper_to_folded(self):
        print("gripper at " + str(self.gripper.position)
              + ", speed " + str(self.gripper.speed))
        if self.gripper.position > 0:
            dc = -100
        else:
            dc = 100
        self.gripper.run_to_abs_pos(position_sp = 0,
                                    duty_cycle_sp = dc,
                                    stop_command='brake')
        time.sleep(0.5)
        while abs(self.gripper.speed) > 0:
            print("gripper at " + str(self.gripper.position)
                  + ", speed " + str(self.gripper.speed))
            time.sleep(0.25)
        print("(end) gripper at " + str(self.gripper.position)
              + ", speed " + str(self.gripper.speed))

    def sense_color(self):
        self.sensor.mode = 'COL-COLOR'
        reading = self.sensor.value()
        if reading == 1:
            return "black"
        elif reading == 2:
            return "blue"
        elif reading == 3:
            return "green"
        elif reading == 4:
            return "yellow"
        elif reading == 5:
            return "red"
        elif reading == 6:
            return "white"
        elif reading == 7:
            return "brown"
        else:
            return ""

    def sense_distance(self):
        self.sensor.mode = 'COL-REFLECT'
        reading = self.sensor.value()
        return reading

    def data_collector(self, count, direction):
        self.drive.run_forever(duty_cycle_sp = direction * 50)
        start_time = time.time()
        data = []
        while count > 0:
            sample = (time.time() - start_time, self.drive.position, self.proxor.value(), self.sensor.value())
            data.append(sample)
            print(count, sample)
            time.sleep(0.01)
            count -= 1
        self.drive.stop(stop_command='coast')
        return data

    ## end class RPCRobot


class RobotError (Exception):
    def __init__(self, message):
        super(Exception, self).__init__()
        self.message = message

    def __str__(self):
        return "Robot Error: " + self.message


import threading

class _Visualiser:
    CANVAS_WIDTH = 800
    CANVAS_HEIGHT = 600
    ROBOT_COLOR = "darkgray"
    FOLDED_GRIPPER_ANGLE = 0.05 * math.pi
    OPEN_GRIPPER_ANGLE = -0.5 * math.pi
    CLOSED_GRIPPER_ANGLE = -0.7 * math.pi

    def __init__(self):
        try:
            import tkinter as tk
        except ImportError:
            try:
                import Tkinter as tk
            except ImportError:
                self.root = None
                return
        self.root = tk.Tk()
        try:
            self.root.wm_title("Robot Simulator")
            frame = tk.Frame(self.root)
            frame.pack()
            self.canvas = tk.Canvas(frame,
                                    width=self.CANVAS_WIDTH,
                                    height=self.CANVAS_HEIGHT,
                                    bg="white")
            self.canvas.pack(side="top")
            # self.close_button = tk.Button(frame, text="Close",
            #                               command=self.root.destroy)
            # self.close_button.pack(side="bottom")
        except Exception as exc:
            self.root.destroy()
            raise exc
        self.simulator = None

    def check_window(self):
        if self.root is None:
            return False
        try:
            _state = self.root.state()
            return True
        except:
            print("The visualiser window appears to have been closed.\n" +
                  "Reset the robot if you want to see it again.")
            self.root = None
        return False

    def reset(self, simulator):
        if self.root is not None:
            self.canvas.delete("robot")
            self.canvas.delete("gripper")
            self.canvas.delete("box")
            self.canvas.delete("table")
            self.canvas.delete("error")
            self.sim = simulator
            self.create_objects()
            self.root.update()
        else:
            print("tk not available, visualisation disabled")
            simulator.vis = False

    def run(self):
        if not self.check_window():
            return
        if sys.platform == 'windows':
            thread = threading.Thread(target = lambda : self.root.mainloop())
            thread.start()

    def create_objects(self):
        xscale = self.CANVAS_WIDTH // (self.sim.width + 2)
        yscale = self.CANVAS_HEIGHT // (self.sim.height + 2)
        self.scale = min(xscale, yscale)
        # draw table
        self.canvas.create_line((1 * self.scale) - 2,
                                self.CANVAS_HEIGHT - (self.scale - 2),
                                ((self.sim.width + 1) * self.scale) + 2,
                                self.CANVAS_HEIGHT - (self.scale - 2),
                                width=2, fill="black", tag="table")
        # draw boxes
        print(self.sim.boxes)
        print(self.sim.table)
        self.box_id = [ 0 for item in self.sim.boxes ]
        for (xpos,stack) in enumerate(self.sim.table):
            for (ypos,box) in enumerate(stack):
                assert(box < len(self.sim.boxes))
                color = self.sim.boxes[box]
                bid = self.canvas.create_rectangle((xpos + 1) * self.scale,
                                                   self.CANVAS_HEIGHT - (ypos + 1) * self.scale,
                                                   (xpos + 2) * self.scale,
                                                   self.CANVAS_HEIGHT - (ypos + 2) * self.scale,
                                                   outline="black", fill=color,
                                                   tag="box")
                self.box_id[box] = bid
        self.draw_robot()

    def draw_robot(self):
        assert(self.sim.lift_pos >= 0)
        assert(self.sim.lift_pos < self.sim.height)
        center_x = int((self.sim.drive_pos + 1.5) * self.scale)
        half_width = int(0.7 * self.scale)
        left_x = center_x - half_width
        right_x = center_x + half_width
        sensor_x = int((self.sim.drive_pos + 2.5) * self.scale)
        s_size = int(0.25 * self.scale)
        lift_y = self.CANVAS_HEIGHT - int((self.sim.lift_pos + 1.2) * self.scale)
        sensor_y = self.CANVAS_HEIGHT - int((self.sim.lift_pos + 1.5) * self.scale)
        if self.sim.drive_pos >= -1 and self.sim.drive_pos < self.sim.width:
            self.canvas.create_line(left_x, lift_y, right_x, lift_y,
                                    width=5, fill=self.ROBOT_COLOR, tag="robot")
            self.canvas.create_oval(sensor_x - s_size, sensor_y - s_size,
                                    sensor_x + s_size, sensor_y + s_size,
                                    fill=self.ROBOT_COLOR, tag="robot")
            if self.sim.gripper_state < 0:
                angle = self.FOLDED_GRIPPER_ANGLE
            elif self.sim.gripper_state == 0:
                angle = self.OPEN_GRIPPER_ANGLE
            else:
                angle = self.CLOSED_GRIPPER_ANGLE
            self.draw_gripper(angle, center_x, lift_y)

    def draw_gripper(self, angle, center_x, center_y):
        r = 1.0 * self.scale
        half_width = int(0.7 * self.scale)
        # offset from center of baseline
        pz = math.sin(-angle) * r
        sr = (1 - (0.8/r) * pz) * r
        px = math.cos(angle) * sr
        py = math.sin(angle) * sr
        left_x = center_x - half_width
        right_x = center_x + half_width
        #print(angle / math.pi, r, pz, sr, px, py)
        self.canvas.create_line(right_x, center_y,
                                right_x + px, center_y + py,
                                width=5, fill=self.ROBOT_COLOR,
                                tag="gripper")
        self.canvas.create_line(left_x, center_y,
                                left_x - px, center_y + py,
                                width=5, fill=self.ROBOT_COLOR,
                                tag="gripper")

    def move_gripper(self, from_angle, to_angle, speed = 1):
        angle_diff = (to_angle - from_angle)
        if angle_diff < 0:
            angle_step = -0.04 * speed
        else:
            angle_step = 0.04 * speed
        n_steps = int(angle_diff / angle_step)
        #print(angle_diff, angle_step, n_steps)
        center_x = int((self.sim.drive_pos + 1.5) * self.scale)
        lift_y = self.CANVAS_HEIGHT - int((self.sim.lift_pos + 1.2) * self.scale)
        angle = from_angle
        for i in range(n_steps - 1):
            self.canvas.delete("gripper")
            angle += angle_step
            self.draw_gripper(angle, center_x, lift_y)
            self.root.update()
            time.sleep(0.05)
        self.canvas.delete("gripper")
        self.draw_gripper(to_angle, center_x, lift_y)
        self.root.update()

    def gripper_folded_to_open(self):
        if not self.check_window():
            return
        self.move_gripper(self.FOLDED_GRIPPER_ANGLE,
                          self.OPEN_GRIPPER_ANGLE,
                          speed = 2)

    def gripper_folded_to_closed(self):
        if not self.check_window():
            return
        self.move_gripper(self.FOLDED_GRIPPER_ANGLE,
                          self.CLOSED_GRIPPER_ANGLE,
                          speed = 2)

    def gripper_open_to_folded(self):
        if not self.check_window():
            return
        self.move_gripper(self.OPEN_GRIPPER_ANGLE,
                          self.FOLDED_GRIPPER_ANGLE,
                          speed = 2)

    def gripper_open_to_closed(self):
        if not self.check_window():
            return
        self.move_gripper(self.OPEN_GRIPPER_ANGLE,
                          self.CLOSED_GRIPPER_ANGLE)

    def gripper_closed_to_open(self):
        if not self.check_window():
            return
        self.move_gripper(self.CLOSED_GRIPPER_ANGLE,
                          self.OPEN_GRIPPER_ANGLE)

    def gripper_closed_to_folded(self):
        if not self.check_window():
            return
        self.move_gripper(self.CLOSED_GRIPPER_ANGLE,
                          self.FOLDED_GRIPPER_ANGLE,
                          speed = 2)

    def move_robot_one_step(self, xdir, ydir):
        if self.scale >= 30:
            step_size = self.scale / 30
            moved = 0
            pos = 0
            while moved < self.scale:
                pos += step_size
                offset = int(math.floor(pos - moved))
                if offset > 0:
                    if moved + offset > self.scale:
                        offset = self.scale - moved
                    self.canvas.move("robot", xdir * offset, ydir * offset)
                    self.canvas.move("gripper", xdir * offset, ydir * offset)
                    if self.sim.holding is not None:
                        for box in self.sim.holding:
                            assert(box < len(self.sim.boxes))
                            self.canvas.move(self.box_id[box], xdir * offset, ydir * offset)
                    self.root.update()
                    moved += offset
                    time.sleep(0.01)
        else:
            time_step = 0.30 / self.scale
            assert(time_step >= 0.01)
            for i in range(self.scale):
                self.canvas.move("robot", xdir, ydir)
                self.canvas.move("gripper", xdir, ydir)
                if self.sim.holding is not None:
                    for box in self.sim.holding:
                        assert(box < len(self.sim.boxes))
                        self.canvas.move(self.box_id[box], xdir, ydir)
                self.root.update()
                time.sleep(0.01)

    def move_robot_left(self):
        if not self.check_window():
            return
        self.move_robot_one_step(-1, 0)

    def move_robot_right(self):
        if not self.check_window():
            return
        self.move_robot_one_step(1, 0)

    def move_robot_up(self):
        if not self.check_window():
            return
        self.move_robot_one_step(0, -1)

    def move_robot_down(self):
        if not self.check_window():
            return
        self.move_robot_one_step(0, 1)

    def flag_collision(self, xpos, ypos):
        if not self.check_window():
            return
        assert(xpos >= -1)
        assert(xpos <= self.sim.width + 1)
        assert(ypos >= -1)
        assert(ypos <= self.sim.height + 1)
        x1 = int((xpos + 1.1) * self.scale)
        x2 = int((xpos + 1.9) * self.scale)
        y1 = self.CANVAS_HEIGHT - int((ypos + 1.1) * self.scale)
        y2 = self.CANVAS_HEIGHT - int((ypos + 1.9) * self.scale)
        self.canvas.create_line(x1, y2, x2, y1, width=5, fill="white", tag="error")
        self.canvas.create_line(x1, y1, x2, y2, width=5, fill="white", tag="error")
        self.canvas.create_line(x1, y2, x2, y1, width=3, fill="red", tag="error")
        self.canvas.create_line(x1, y1, x2, y2, width=3, fill="red", tag="error")
        self.root.update()

    ## end class Visualiser


def _random_box_setup(width, height):
    import random
    color_list = ["black", "blue", "green", "yellow", "red", "white", "brown"]
    result = []
    for i in range(0, width, 2):
        stack = []
        for j in range(random.randint(0, height - 1)):
            col = color_list[random.randint(0, len(color_list) - 1)]
            stack.append(col)
        result.append(stack)
        if i + 1 < width:
            result.append([])
    return result

class _SimRobot:
    '''Simulated Robot class.'''

    def __init__(self, visualise = True, width = 5, height = 2,
                 pos = -1, boxes = [["red"], [], ["green"], [], ["blue"]]):
        self.width = width # width of the table
        self.height = height # levels of the lift
        self.drive_pos = pos # where the gripper is; sensor is at +1
        self.lift_pos = 0 # lift is down
        self.gripper_state = -1 # < 0 = folded, 0 = open, > 0 = closed
        self.holding = None
        self.collided = False
        self.collisions = []
        if isinstance(boxes, str):
            if boxes == "random":
                boxes = _random_box_setup(width, height)
            elif boxes == "flat":
                clist = ["red", "green", "blue"]
                boxes = [ [ clist[ (i // 2) % 3 ] ] if i % 2 == 0 else []
                          for i in range(width) ]
            else:
                raise RobotError("Invalid keyword '" + boxes + "' for boxes")
        assert(len(boxes) <= self.width)
        self.boxes = []
        self.table = [ [] for i in range(self.width) ]
        pos = 0
        for stack in boxes:
            for color in stack:
                self.boxes.append(color)
                index = len(self.boxes) - 1
                self.table[pos].append(index)
            pos += 1
        self.vis = visualise
        if self.vis:
            main = sys.modules['__main__']
            #global _visualiser
            if not hasattr(main, '_visualiser'):
                setattr(main, '_visualiser', _Visualiser())
            elif not getattr(main, '_visualiser').check_window():
                setattr(main, '_visualiser', _Visualiser())
            self.visualiser = getattr(main, '_visualiser')
            self.visualiser.reset(self)
            self.visualiser.run()

    def print_state(self, command = None):
        if command is not None:
            print("executing command " + command)
        print("drive position: " + str(self.drive_pos)
              + " (width = " + str(self.width) + ")")
        print("lift position: " + str(self.lift_pos)
              + " (height = " + str(self.height) + ")")
        if self.gripper_state < 0:
            print("gripper is folded")
        elif self.gripper_state == 0:
            print("gripper is open")
        else:
            print("gripper is closed")
            if self.holding is not None:
                print("holding: " + str(self.holding))
        print("boxes on shelf: " + str(self.table))
        if self.collided:
            print("collision flag is set "
                  + ", ".join([str(pos) for pos in self.collisions]))
        else:
            print("collision flag is not set")

    def sense_color(self):
        if self.collided:
            raise RobotError("The robot has hit a box. You must reset it.")
        spos = self.drive_pos + 1
        if spos >= 0 and spos < self.width:
            height = len(self.table[spos])
            if self.lift_pos < height:
                box_num = self.table[spos][self.lift_pos]
                assert(box_num < len(self.boxes))
                return self.boxes[box_num]
            else:
                return ""
        else:
            return ""

    # check if there is an obstacle at drive/lift pos, and raise
    # a collision exception if so; dpos is the x-position to check
    # (not necessarily the actual drive position); both positions
    # are after the move currently being attempted
    def check_for_collision(self, dpos, lpos, more = False):
        if dpos >= 0 and dpos < self.width:
            # height will be zero if table at dpos is clear
            height = len(self.table[dpos])
            if height > lpos:
                self.collided = True
                self.collisions.append((dpos, lpos))
                if self.vis:
                    self.visualiser.flag_collision(dpos, lpos)
            if not more:
                if self.collided:
                    raise RobotError("The robot has hit one or more boxes at "
                                     + ", ".join([str(pos)
                                                  for pos in self.collisions])
                                     + "!")

    def lift_up(self):
        if self.collided:
            raise RobotError("The robot has hit a box. You must reset it.")
        if self.lift_pos + 1 < self.height:
            self.lift_pos = self.lift_pos + 1
        else:
            raise RobotError("The lift is at level " + str(self.lift_pos)
                             + " and can't go any higher!")
        if self.vis:
            self.visualiser.move_robot_up()
        else:
            self.print_state("lift_up")

    def lift_down(self):
        if self.collided:
            raise RobotError("The robot has hit a box. You must reset it.")
        if self.lift_pos > 0:
            self.lift_pos = self.lift_pos - 1
            if self.vis:
                self.visualiser.move_robot_down()
            else:
                self.print_state("lift_down")
            # check for collisions
            if self.holding is not None:
                self.check_for_collision(self.drive_pos, self.lift_pos)
            elif self.gripper_state > 0: # closed
                self.check_for_collision(self.drive_pos, self.lift_pos)
            if self.gripper_state >= 0: # not folded (closed or open)
                self.check_for_collision(self.drive_pos - 1, self.lift_pos,
                                         more = True)
                self.check_for_collision(self.drive_pos + 1, self.lift_pos)
        else:
            raise RobotError("The lift is at level 0 and can't go any lower!")

    def drive_right(self):
        if self.collided:
            raise RobotError("The robot has hit a box. You must reset it.")
        self.drive_pos = self.drive_pos + 1
        if self.vis:
            self.visualiser.move_robot_right()
        else:
            self.print_state("drive_right")
        if self.gripper_state >= 0: # not folded
            self.check_for_collision(self.drive_pos + 1, self.lift_pos,
                                     more = True)
            self.check_for_collision(self.drive_pos - 1, self.lift_pos)

    def drive_left(self):
        if self.collided:
            raise RobotError("The robot has hit a box. You must reset it.")
        self.drive_pos = self.drive_pos - 1
        if self.vis:
            self.visualiser.move_robot_left()
        else:
            self.print_state("drive_left")
        if self.gripper_state >= 0: # not folded
            self.check_for_collision(self.drive_pos - 1, self.lift_pos,
                                     more = True)
            self.check_for_collision(self.drive_pos + 1, self.lift_pos)

    def gripper_to_closed(self):
        if self.collided:
            raise RobotError("The robot has hit a box. You must reset it.")
        if self.gripper_state > 0: # already closed, do nothing
            if not self.vis:
                self.print_state("gripper_to_closed")
            return
        assert(self.holding == None)
        if self.gripper_state == 0: # open
            self.gripper_state = 1 # closed
            self.check_if_holding()
            if self.vis:
                self.visualiser.gripper_open_to_closed()
            else:
                self.print_state("gripper_to_closed")
        elif self.gripper_state < 0: # folded
            self.gripper_state = 1
            self.check_if_holding()
            if self.vis:
                self.visualiser.gripper_folded_to_closed()
            else:
                self.print_state("gripper_to_closed")
            self.check_for_collision(self.drive_pos - 1, self.lift_pos,
                                     more = True)
            self.check_for_collision(self.drive_pos + 1, self.lift_pos,
                                     more = True)
            self.check_for_collision(self.drive_pos - 2, self.lift_pos,
                                     more = True)
            self.check_for_collision(self.drive_pos + 2, self.lift_pos)


    def check_if_holding(self):
        if self.drive_pos >= 0 and self.drive_pos < self.width:
            height = len(self.table[self.drive_pos])
            if self.lift_pos <= (height - 1):
                self.holding = self.table[self.drive_pos][self.lift_pos:]
                self.table[self.drive_pos] = self.table[self.drive_pos][:self.lift_pos]

    def drop_if_holding(self):
        if self.holding is not None:
            # dropping what we're holding, check if it falls
            if self.drive_pos < 0 or self.drive_pos >= self.width:
                # dropped off the table
                self.collided = True
                self.collisions.append((self.drive_pos, self.lift_pos - 1))
                if self.vis:
                    assert(self.lift_pos > 0)
                    self.visualiser.flag_collision(self.drive_pos, self.lift_pos - 1)
                raise RobotError("Dropped box(es) off the table!")
            # else, check if too high
            height = len(self.table[self.drive_pos])
            assert(self.lift_pos >= height)
            if self.lift_pos == height:
                self.table[self.drive_pos] = self.table[self.drive_pos] + self.holding
                self.holding = None
            else:
                self.collided = True
                self.collisions.append((self.drive_pos, self.lift_pos - 1))
                if self.vis:
                    assert(self.lift_pos > 0)
                    self.visualiser.flag_collision(self.drive_pos, self.lift_pos - 1)
                raise RobotError("Dropped box(es) from too high!")

    def gripper_to_open(self):
        if self.collided:
            raise RobotError("The robot has hit a box. You must reset it.")
        if self.gripper_state == 0: # already open, do nothing
            if not self.vis:
                self.print_state("gripper_to_open")
            return
        if self.gripper_state > 0: # closed
            self.gripper_state = 0 # open
            self.drop_if_holding()
            if self.vis:
                self.visualiser.gripper_closed_to_open()
            else:
                self.print_state("gripper_to_open")
        elif self.gripper_state < 0: # folded
            self.gripper_state = 0
            if self.vis:
                self.visualiser.gripper_folded_to_open()
            else:
                self.print_state("gripper_to_open")
            # check for collisions
            self.check_for_collision(self.drive_pos - 1, self.lift_pos,
                                     more = True)
            self.check_for_collision(self.drive_pos + 1, self.lift_pos,
                                     more = True)
            self.check_for_collision(self.drive_pos - 2, self.lift_pos,
                                     more = True)
            self.check_for_collision(self.drive_pos + 2, self.lift_pos)

    def gripper_to_folded(self):
        if self.collided:
            raise RobotError("The robot has hit a box. You must reset it.")
        if self.gripper_state < 0: # already folded, do nothing
            if not self.vis:
                self.print_state("gripper_to_folded")
            return
        if self.gripper_state > 0: # closed
            self.gripper_state = -1 # folded
            self.drop_if_holding()
            if self.vis:
                self.visualiser.gripper_closed_to_folded()
            else:
                self.print_state("gripper_to_folded")
            # check for collisions
            self.check_for_collision(self.drive_pos - 1, self.lift_pos,
                                     more = True)
            self.check_for_collision(self.drive_pos + 1, self.lift_pos,
                                     more = True)
            self.check_for_collision(self.drive_pos - 2, self.lift_pos,
                                     more = True)
            self.check_for_collision(self.drive_pos + 2, self.lift_pos)
        elif self.gripper_state == 0: # open
            self.gripper_state = -1 # folded
            if self.vis:
                self.visualiser.gripper_open_to_folded()
            else:
                self.print_state("gripper_to_folded")
            # check for collisions
            self.check_for_collision(self.drive_pos - 1, self.lift_pos,
                                     more = True)
            self.check_for_collision(self.drive_pos + 1, self.lift_pos,
                                     more = True)
            self.check_for_collision(self.drive_pos - 2, self.lift_pos,
                                     more = True)
            self.check_for_collision(self.drive_pos + 2, self.lift_pos,
                                     more = True)

    # def __str__(self):
    #     return ("X: " + str(self.drive_pos) + " [0," + str(self.width) +
    #             "], Y: " + str(self.lift_pos) + " [0," + str(self.height) +
    #             "], G: " + str(self.gripper_state) + ", H: " +
    #             str(self.holding) + ", T: " + str(self.table))
