import enum
import re
import sys
import os
from collections import defaultdict
import heapq

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from utils import utils

FILE = "./data2"


D_UP = 0
D_RIGHT = 1
D_DOWN = 2
D_LEFT = 3
D_DXDY = {
    D_UP: (0, 1),
    D_RIGHT: (1, 0),
    D_DOWN: (0, -1),
    D_LEFT: (-1, 0),
}


START_D = D_RIGHT
R_C = 1000


class Node:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.src_node = None
        self.cost = 99999999999999
        self.extra_src_nodes = []

    def update_cost(self, src_node, cost):
        self.src_node = src_node
        self.cost = cost
        self.extra_src_nodes = []

    def add_extra_src_node(self, src_node):
        self.extra_src_nodes.append(src_node)

    def __repr__(self):
        return f"Node({self.x}, {self.y}): D{self.direction}; C: {self.cost}"

    def __eq__(self, other):
        if isinstance(other, Node):
            return (
                self.x == other.x
                and self.y == other.y
                and self.direction == other.direction
            )
        return False

    def __lt__(self, other):
        return self.cost < other.cost

    def __hash__(self):
        return hash((self.x, self.y, self.direction))


def find_cheapest_path(start_node, nodes):
    pq = []
    heapq.heappush(pq, start_node)
    visited = set()
    while pq:
        current_node = heapq.heappop(pq)
        # print(current_node)
        if current_node in visited:
            continue
        visited.add(current_node)
        for direction_offset in [-1, 0, 1]:
            direction = (current_node.direction + direction_offset) % 4
            extra_cost = 0 if direction == current_node.direction else R_C
            n_x = current_node.x + D_DXDY[direction][0]
            n_y = current_node.y + D_DXDY[direction][1]
            # print(n_x, n_y)
            if nodes[n_y][n_x] is None:
                continue

            neighbor_node = nodes[n_y][n_x][direction]
            # print(neighbor_node)
            neighbor_node_new_cost = current_node.cost + 1 + extra_cost
            if neighbor_node_new_cost < neighbor_node.cost:
                neighbor_node.update_cost(
                    src_node=current_node,
                    cost=neighbor_node_new_cost,
                )
                heapq.heappush(pq, neighbor_node)
            elif neighbor_node_new_cost == neighbor_node.cost:
                neighbor_node.add_extra_src_node(
                    src_node=current_node,
                )


def find_unique_nodes(unique_nodes, node):
    if node is None or node in unique_nodes:
        return
    find_unique_nodes(unique_nodes, node.src_node)
    for en in node.extra_src_nodes:
        find_unique_nodes(unique_nodes, en)
    unique_nodes.add(node)


def print_data(lines,nodes,unique_nodes):
    for y, r in enumerate(lines):
        line = ""
        for x, c in enumerate(r):
            if nodes[y][x] is None:
                line += "#"
                continue
            was_location_visited = False
            for d in range(0, 4):
                if nodes[y][x][d] in unique_nodes:
                    was_location_visited = True
                    break
            if was_location_visited:
                line += "O"
            else:
                line += "."
        print(line)

def do_your_magic1():
    s = 0
    lines = list(utils.read_file_content(FILE))
    my = len(lines)
    mx = len(lines[0])
    nodes = [[None] * mx for _ in range(my)]
    start_node = None
    end_nodes = None
    for y, r in enumerate(lines):
        for x, c in enumerate(r):
            if c == "#":
                continue
            nodes[y][x] = {
                D_UP: Node(x, y, D_UP),
                D_RIGHT: Node(x, y, D_RIGHT),
                D_DOWN: Node(x, y, D_DOWN),
                D_LEFT: Node(x, y, D_LEFT),
            }
            if c == ".":
                pass
            if c == "E":
                end_nodes = nodes[y][x]
            if c == "S":
                start_node = nodes[y][x][START_D]
                start_node.update_cost(src_node=None, cost=0)

    find_cheapest_path(start_node, nodes)

    print(start_node)
    print(end_nodes)

    unique_nodes = set()
    min_cost = min(n.cost for n in end_nodes.values())
    for end_node in end_nodes.values():
        if end_node.cost > min_cost:
            continue
        find_unique_nodes(unique_nodes, end_node)

    print("done")
    print(s)
    print(len(unique_nodes))
    unique_locations={(n.x,n.y) for n in unique_nodes}
    print(len(unique_locations))
    # print_data(lines,nodes,unique_nodes)
    


do_your_magic1()
