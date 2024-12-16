import re
import sys
import os
from collections import defaultdict
import copy
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from utils import utils

FILE = "./data2"
COMMANDS = {
    "<": (-1, 0),
    ">": (+1, 0),
    "v": (0, +1),
    "^": (0, -1),
}


def execute_command(data, r_x, r_y, c):
    dx, dy = COMMANDS[c]

    new_x = r_x + dx
    new_y = r_y + dy
    if data[new_y][new_x] == ".":
        return data, new_x, new_y
    if data[new_y][new_x] == "#":
        return data, r_x, r_y

    data_copy = copy.deepcopy(data)
    were_boxes_pushed = push_boxes(data_copy, new_x, new_y, dx, dy)

    if were_boxes_pushed:
        return data_copy, new_x, new_y
    return data, r_x, r_y


def push_boxes(data, box_x, box_y, dx, dy) -> bool:
    # not a box/was already moved
    if data[box_y][box_x] == ".":
        return True
    if data[box_y][box_x] == "#":
        return False

    # new_x = box_x + dx
    # new_y = box_y + dy

    if dx == 0:
        if data[box_y][box_x] == "[":
            xchange = 1
        elif data[box_y][box_x] == "]":
            xchange = -1
        else:
            raise Exception("invalid symbol")
        were_boxes_pushed1 = push_boxes(data, box_x, box_y + dy, dx, dy)
        were_boxes_pushed2 = push_boxes(data, box_x + xchange, box_y + dy, dx, dy)
        if not were_boxes_pushed1 or not were_boxes_pushed2:
            return False
        data[box_y + dy][box_x] = data[box_y][box_x]
        data[box_y][box_x] = "."
        data[box_y + dy][box_x + xchange] = data[box_y][box_x + xchange]
        data[box_y][box_x + xchange] = "."
        return True
    else:
        if data[box_y][box_x] not in ["[", "]"]:
            raise Exception("invalid symbol")
        were_boxes_pushed = push_boxes(data, box_x + dx, box_y, dx, dy)
        if not were_boxes_pushed:
            return False
        data[box_y][box_x + dx] = data[box_y][box_x]
        data[box_y][box_x] = "."
        return True

    return False


def print_map(data, r_x, r_y):
    for i, r in enumerate(data):
        line = ""
        for j, c in enumerate(r):
            if i == r_y and j == r_x:
                line += "@"
            else:
                line += c
        print(line)


def do_your_magic1():
    s = 0
    lines = list(utils.read_file_content(FILE))
    data = []
    first_line = lines[0]
    loading_command = False
    commands = ""
    r_x = -1
    r_y = -1
    for i in range(1, len(lines)):
        line = lines[i]
        if line == first_line:
            loading_command = True
            continue

        if not loading_command:
            row = []
            for j, c in enumerate(line):
                if c in ["#", "."]:
                    row.append(c)
                    row.append(c)
                if c == "O":
                    row.append("[")
                    row.append("]")

                if c == "@":
                    r_x = j*2
                    r_y = i
                    c = "."
                    row.append(".")
                    row.append(".")
            data.append(row)

        if loading_command:
            commands += line
    data.insert(0, [c for c in first_line] * 2)
    data.append([c for c in first_line] * 2)

    print_map(data, r_x, r_y)

    for i, c in enumerate(commands):
        data, r_x, r_y = execute_command(data, r_x, r_y, c)
        # if i<20:
        #     print("Command: ", c)
        #     print_map(data, r_x, r_y)
        #     time.sleep(2)

    print_map(data, r_x, r_y)
    s = 0
    for i, r in enumerate(data):
        for j, c in enumerate(r):
            if c == "[":
                s += i * 100 + j

    print("done")
    print(s)


do_your_magic1()
