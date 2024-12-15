import re
import sys
import os
import time
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from utils import utils

# FILE = "./data1"
# SIZE = (11, 7)
FILE = "./data2"
#  wide, height
SIZE = (101, 103)


r_robot = r"p=(\d*),(\d*) v=(\-?\d*),(\-?\d*)"


class Robot:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def move(self, times, size):
        self.x += self.vx * times
        self.x %= size[0]
        self.y += self.vy * times
        self.y %= size[1]

    def get_quadrant(self, size):
        hw = int(size[0] / 2)
        hh = int(size[1] / 2)
        # print('hw,hh')
        # print(hw,hh)
        if self.x == hw or self.y == hh:
            return None

        if self.x < hw:
            if self.y < hh:
                return 0
            else:
                return 1
        else:
            if self.y < hh:
                return 2
            else:
                return 3

    @staticmethod
    def from_input(line):
        m = re.match(r_robot, line)
        if not m:
            raise Exception("not a match: ", line, r_robot)
        return Robot(
            x=int(m.group(1).strip()),
            y=int(m.group(2).strip()),
            vx=int(m.group(3).strip()),
            vy=int(m.group(4).strip()),
        )


def plot(robots, size):
    taken_places = set()
    for r in robots:
        taken_places.add((r.x, r.y))

    for y in range(size[1]):
        line = ""
        for x in range(size[0]):
            if (x, y) in taken_places:
                line += "#"
            else:
                line += "."
        print(line)


def do_your_magic1():
    size = SIZE
    lines = list(utils.read_file_content(FILE))
    robots = []

    for line in lines:
        robots.append(Robot.from_input(line))

    q_count = {0: 0, 1: 0, 2: 0, 3: 0}
    # for r in robots:
    #     r.move(100, size)
    #     q = r.get_quadrant(size)
    #     if q is not None:
    #         q_count[q] += 1
    # part 2
    
    for i in range(0, 100000):
        unique_palces = set()
        legit=True
        for r in robots:
            r.move(1, size)
            place = (r.x, r.y)
            # assumption that on real picture all robots are on own place, since quadrant method didn't work (checking if picture is simetrical)
            if place in unique_palces:
                legit = False
            unique_palces.add(place)
        if legit:
            print("iteration:", i+1)
            plot(robots, size)
            break
    
    s = 1
    for key, value in q_count.items():
        print(f"Q{key}: {value}")
        s *= value

    print("done")
    print(s)


do_your_magic1()

#  7131 is too low