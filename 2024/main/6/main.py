import re
import sys
import os
from collections import defaultdict
from enum import Enum
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utils import utils

class Direction(Enum):
    UP=1
    DOWN=2
    LEFT=3
    RIGHT=4

FILE='./data2'
class Point:

    def __init__(self, x:int, y:int) -> None:
        self.x=x
        self.y=y
    
    def in_area(self,mx,my)->bool:
        return 0 <= self.x < mx and 0 <= self.y < my

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def __repr__(self) -> str:
        return f'({self.x},{self.y})'

class Guard:
    def __init__(self,location, direction=Direction.UP) -> None:
        self.location=location
        self.direction=direction
    
    def clone(self):
        return Guard(location=self.location, direction=self.direction)
    
    def turn_right(self):
        if self.direction==Direction.UP:
            self.direction=Direction.RIGHT
        elif self.direction==Direction.RIGHT:
            self.direction=Direction.DOWN
        elif self.direction==Direction.DOWN:
            self.direction=Direction.LEFT
        elif self.direction==Direction.LEFT:
            self.direction=Direction.UP
        else:
            raise Exception('invalid direction')

    def get_next_location(self):
        if self.direction==Direction.UP:
            return Point(self.location.x,self.location.y-1)
        elif self.direction==Direction.RIGHT:
            return Point(self.location.x+1,self.location.y)
        elif self.direction==Direction.DOWN:
            return Point(self.location.x,self.location.y+1)
        elif self.direction==Direction.LEFT:
            return Point(self.location.x-1,self.location.y)
        else:
            raise Exception('invalid direction')
        
    def move_to_next_location(self):
        self.location=self.get_next_location()

class Line:
    def __init__(self,sp,ep) -> None:
        self.sp=sp
        self.ep=ep
    
    def is_horizontal(self):
        return self.sp.y==self.ep.y
    
def solution1(guard,obsticals,mx,my):
    s=0
    
    distinct_locations={}
    #distinct_locations=set
    c=0
    all_new_obsticals=set()
    while True:
        c+=1
        print(f'\r{c}/6220')
        if guard.location not in distinct_locations:
            distinct_locations[guard.location]=set()
        distinct_locations[guard.location].add(guard.direction)
        #print(guard.location)
        if guard.get_next_location() in obsticals:
            guard.turn_right()
            distinct_locations[guard.location].add(guard.direction)
        if not guard.get_next_location().in_area(mx,my):
            break
        
        new_obstical=guard.get_next_location()
        if new_obstical not in distinct_locations: 
            cl=guard.clone()
            cl_dl={}
            while True:
                if cl.location not in cl_dl:
                    cl_dl[cl.location]=set()
                cl_dl[cl.location].add(cl.direction)
                while cl.get_next_location() in obsticals or cl.get_next_location() == new_obstical:
                    cl.turn_right()
                    cl_dl[cl.location].add(cl.direction)
                if not cl.get_next_location().in_area(mx,my):
                    break
                cl.move_to_next_location()
                if cl.direction in distinct_locations.get(cl.location,set()) or cl.direction in cl_dl.get(cl.location,set()):
                    s+=1
                    all_new_obsticals.add(new_obstical)
                    break
                
                
        guard.move_to_next_location()
    print('done')
    print(len(distinct_locations))
    print(s)
    print(len(all_new_obsticals))

    
def do_your_magic1():
    lines=list(utils.read_file_content(FILE))
    my=len(lines)
    mx=len(lines[0])
    obsticals=set()
    guard=None
    for y,l in enumerate(lines):
        for x,c in enumerate(l):
            if c=='#':
                obsticals.add(Point(x,y))
            elif c=='^':
                guard=Guard(Point(x,y))
    if guard is None:
        raise Exception('guard not found')
    
    #solution1(guard=guard,obsticals=obsticals,mx=mx,my=my)
    solution1(guard=guard,obsticals=obsticals,mx=mx,my=my)
    #print(all_new_obsticals)
# 1. 3,6
# 2. 6,7
# 3. 7,7
# 4. 1,8 
# 5. 3,8
# 6. 7,9     
do_your_magic1()
