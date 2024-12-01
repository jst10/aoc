import re
import sys
import os
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utils import utils

FILE='./data2'
class Point:
    def __init__(self,x,y) -> None:
        self.x=x
        self.y=y
    
    def are_the_same(self,p2):
        return self.x==p2.x and self.y==p2.y
    
    def key(self):
        return f'{self.x}|{self.y}'
    def __repr__(self) -> str:
        return f'({self.x}, {self.y})'
    
class Field:
    def __init__(self,location:Point,c:str) -> None:
        self.location=location
        self.c=c
    
    def get_next_point(self,first_point):
        if self.is_ground():
            return None
        points=self.get_touching_points()
        found=False
        next_points=[]
        for p in points:
            if p.are_the_same(first_point):
                found=True
                continue
            next_points.append(p)
        if not found:
            return None
        
        if len(next_points)>1:
            raise Exception('next popint wss caled on sart, not ok')
        return next_points[0]

    def get_touching_points(self):
        if self.c=='|':
            return [
                Point(self.location.x,self.location.y-1),
                Point(self.location.x,self.location.y+1)
            ]
        elif self.c=='-':
            return [
                Point(self.location.x-1,self.location.y),
                Point(self.location.x+1,self.location.y)
            ]
        elif self.c=='L':
            return [
                Point(self.location.x,self.location.y-1),
                Point(self.location.x+1,self.location.y)
            ]
        elif self.c=='J':
            return [
                Point(self.location.x,self.location.y-1),
                Point(self.location.x-1,self.location.y)
            ]
        elif self.c=='7':
            return [
                Point(self.location.x-1,self.location.y),
                Point(self.location.x,self.location.y+1)
            ]
        elif self.c=='F':
            return [
                Point(self.location.x+1,self.location.y),
                Point(self.location.x,self.location.y+1)
            ]
        elif self.c=='S':
            return [
                Point(self.location.x+1,self.location.y),
                Point(self.location.x,self.location.y+1),
                Point(self.location.x-1,self.location.y),
                Point(self.location.x,self.location.y-1)
            ]
        else:
            return None
    
    def is_pipe(self)->bool:
        # start is included
        return self.c in ['|','-','L','J','7','F','S']
    
    def is_start(self)->bool:
        return self.c=='S'
    
    def is_ground(self)->bool:
        return self.c=='.'

def is_point_inside_loop(p, points):
    n = len(points)
    count = 0
    for i in range(n):
        p1 = points[i]
        p2 = points[(i + 1) % n]
        if p1.y == p2.y:
            continue
        if min(p1.y, p2.y) < p.y <= max(p1.y, p2.y):
            x_intersect = p1.x + (p.y - p1.y) * (p2.x - p1.x) / (p2.y - p1.y)
            if p.x < x_intersect:
                count += 1
    return count % 2 == 1


def find_points_in_close_loop(points:list[Point]):
    x_min = min(p.x for p in points)
    x_max = max(p.x for p in points)
    y_min = min(p.y for p in points)
    y_max = max(p.y for p in points)

    inside_points = []
    points_set={p.key() for p in points}
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            p=Point(x=x,y=y)
            if p.key() in points_set:
                continue
            if is_point_inside_loop(p, points):
                inside_points.append(p)
    return inside_points
    
def do_your_magic1():
    s=0
    lines=list(utils.read_file_content(FILE))
    fields=defaultdict(dict)
    h=len(lines)
    w=len(lines[0])
    sp=None
    for i,l in enumerate(lines):
        for j,c in enumerate(l):
            location=Point(x=j,y=i)
            f=Field(location=location,c=c)
            fields[location.x][location.y]=f
            if f.is_start():
                sp=location
    if sp is None:
        raise Exception('start point not found')
    print('Start point: ',sp)
    steps=0
    all_points=[]
    for ch in [(0,1),(0,-1),(1,0),(-1,0)]:
        lp=sp
        print('Change: ', ch)
        np=Point(x=sp.x+ch[0],y=sp.y+ch[1])
        checked_points=set()
        found=False
        steps=0
        all_points=[]
        while True:
            steps+=1
            all_points.append(np)
            key=str(np.x)+'|'+str(np.y)
            if key in checked_points:
                break
            checked_points.add(key)
            if not 0<=np.x<w or not 0<=np.y<h:
                break
            af=fields[np.x][np.y]

            if af is None or af.is_ground():
                break
            if af.is_start():
                found=True
                print('found it this is great')
                break
            np=af.get_next_point(first_point=lp)
            #print(lp,'->',af.location,af.c,'->',np)
            lp=af.location
            if np is None:
                break
        if found: 
            break
    print("Steps: ",steps)
    print("Half steps: ",steps/2)
    print(len(all_points))
    inside_points=find_points_in_close_loop(all_points)
    print("Inside points: ",len(inside_points))
   
        
do_your_magic1()