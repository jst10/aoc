from collections import defaultdict
import re
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from utils import utils


FILE = "./data2"

r_button_a = r"Button A: X\+(\d*), Y\+(\d*)"
r_button_b = r"Button B: X\+(\d*), Y\+(\d*)"
r_prize = r"Prize: X=(\d*), Y=(\d*)"


def parse_data(line, regex):
    m = re.match(regex, line)
    if not m:
        raise Exception("not a match: ", line, regex)
    x = int(m.group(1).strip())
    y = int(m.group(2).strip())
    return (x, y)


COST_A = 3
COST_B = 1


# A: 3 tokens
# B: 1 token
# Button A: X+94, Y+34
# Button B: X+22, Y+67
# Prize: X=8400, Y=5400
def get_cost(button_a, button_b, prize):
    a_p_x = prize[0] / button_a[0]
    a_p_y = prize[1] / button_a[1]
    a_m_p = max(a_p_x, a_p_y)

    b_p_x = prize[0] / button_b[0]
    b_p_y = prize[1] / button_b[1]
    b_m_p = max(b_p_x, b_p_y)

    c_a = a_m_p * COST_A
    c_b = b_m_p * COST_B

    price = 0
    if c_a < c_b:
        price = find_cost_h(button_a, COST_A, button_b, COST_B, prize)
    else:
        price = find_cost_h(button_b, COST_B, button_a, COST_A, prize)
    return price


def get_cost2(button_a, button_b, prize):

    # button_a[0]*press_a+button_b[0]*press_b=prize[0]
    # button_a[0]*press_a=prize[0]-button_b[0]*press_b
    # press_a=(prize[0]-button_b[0]*press_b)/button_a[0]

    # button_a[1]*press_a+button_b[1]*press_b=prize[1]
    # button_a[1]*((prize[0]-button_b[0]*press_b)/button_a[0])+button_b[1]*press_b=prize[1]
    # button_a[1]*prize[0]-button_a[1]*button_b[0]*press_b+button_b[1]*press_b*button_a[0]=prize[1]*button_a[0]
    # button_b[1]*press_b*button_a[0]-button_a[1]*button_b[0]*press_b+=prize[1]*button_a[0]-button_a[1]*prize[0]
    # press_b(button_b[1]*button_a[0]-button_a[1]*button_b[0])=prize[1]*button_a[0]-button_a[1]*prize[0]
    # press_b=(prize[1]*button_a[0]-button_a[1]*prize[0])/((button_b[1]*button_a[0]-button_a[1]*button_b[0]))
    press_b = (prize[1] * button_a[0] - button_a[1] * prize[0]) / (
        (button_b[1] * button_a[0] - button_a[1] * button_b[0])
    )
    press_a = (prize[0] - button_b[0] * press_b) / button_a[0]

    if press_a == int(press_a) and press_b == int(press_b):
        return press_a * COST_A + press_b * COST_B
    return None


def find_cost_h(primary_button, primary_cost, secondary_button, secondary_cost, prize):
    pb_p_x = prize[0] / primary_button[0]
    pb_p_y = prize[1] / primary_button[1]
    pb_m_p = int(max(pb_p_x, pb_p_y)) + 1

    for i in range(pb_m_p, -1, -1):
        rx = prize[0] - primary_button[0] * i
        ry = prize[1] - primary_button[1] * i
        if rx < 0 or ry < 0:
            continue
        if rx % secondary_button[0] != 0 or ry % secondary_button[1] != 0:
            continue
        s_cx = rx / secondary_button[0]
        s_cy = ry / secondary_button[1]
        if s_cx != s_cy:
            continue
        # print('i,primary_cost,s_cx,secondary_cost')
        # print(i,primary_cost,s_cx,secondary_cost)
        price = i * primary_cost + s_cx * secondary_cost
        return price
    return None


def do_your_magic1():
    s = 0
    lines = list(utils.read_file_content(FILE))
    for i in range(0, len(lines), 3):
        button_a = parse_data(lines[i], r_button_a)
        button_b = parse_data(lines[i + 1], r_button_b)
        prize = parse_data(lines[i + 2], r_prize)
        prize=(prize[0]+10000000000000,prize[1]+10000000000000)
        cost = get_cost2(button_a, button_b, prize)
        if cost:
            s += cost
    print("done")

    print(s)


do_your_magic1()
