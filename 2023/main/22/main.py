import re
import sys
import os
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utils import utils

FILE='./data2'

class Point3d():
    def __init__(self,x:int,y:int,z:int) -> None:
        self.x=x
        self.y=y
        self.z=z
    def move_down(self):
        self.z-=1
    def move_up(self):
        self.z+=1
    def move_left(self):
        self.x-=1
    def move_right(self):
        self.x+=1
    def move_backward(self):
        self.y-=1
    def move_forward(self):
        self.y+=1
    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __eq__(self, other):
        if isinstance(other, Point3d):
            return self.x == other.x and self.y == other.y and self.z == other.z
        return False


    def __repr__(self) -> str:
        return f'({self.x},{self.y},{self.z})'

class Brick():
    def __init__(self,id,sp,ep) -> None:
        self.id=id
        self.sp=sp
        self.ep=ep
        self.below_bricks=set()
        self.above_bricks=set()

    @property
    def min_z(self):
        return min(self.sp.z,self.ep.z)
    @property
    def max_z(self):
        return max(self.sp.z,self.ep.z)
    def move_down(self):
        self.sp.move_down()
        self.ep.move_down()
    
    def is_on_ground(self):
        return self.min_z==0
    
    def is_vertical(self):
        return self.min_z!=self.max_z
    
    def occupied_points(self):
        points=[]
        for i in range(self.sp.x,self.ep.x+1):
            for j in range(self.sp.y,self.ep.y+1):
                for k in range(self.sp.z,self.ep.z+1):
                    points.append(Point3d(i,j,k))
        return points
    
    def points_above(self):
        if self.is_vertical():
            return [Point3d(self.sp.x,self.sp.y,self.max_z+1)]
        else:
            op=self.occupied_points()
            for p in op:
                p.move_up()
            return op
        
    def points_below(self):
        if self.is_vertical():
            return [Point3d(self.sp.x,self.sp.y,self.min_z-1)]
        else:
            op=self.occupied_points()
            for p in op:
                p.move_down()
            return op


    def __repr__(self) -> str:
        #return f'{self.id} SP: {self.sp}; EP: {self.ep}'
        return f'{self.id} '
    
    def __hash__(self):
        return hash((self.id))

    def __eq__(self, other):
        if isinstance(other, Point3d):
            return self.id == other.id
        return False

    @staticmethod
    def from_input(id,line):
        r1='(\d*),(\d*),(\d*)~(\d*),(\d*),(\d*)'
        m1 = re.match(r1, line)
        if not m1:
            raise Exception('invalid input')
        sp=Point3d(int(m1.group(1)),int(m1.group(2)),int(m1.group(3)))
        ep=Point3d(int(m1.group(4)),int(m1.group(5)),int(m1.group(6)))

        # sanity check on input data, that are what I expect to be
        n_same=0
        if sp.x==ep.x:
            n_same+=1
        if sp.y==ep.y:
            n_same+=1
        if sp.z==ep.z:
            n_same+=1
        if n_same<2:
            raise Exception(f'Brick is diagonaly SP:{sp} EP {ep} ',n_same)

        return Brick(id,sp,ep)
        

    def set_below_brick(self,b):
        self.below_bricks.add(b)
    def set_above_brick(self,b):
        self.above_bricks.add(b)

def has_anything_under(taken_area, brick):
    pb=brick.points_below()
    for p in pb:
        if p in taken_area:
            return True
    return False


def count_above_that_will_fall(db,bricks)->int:
    number_of_supporting_bricks = {}
    for b in bricks:
        number_of_supporting_bricks[b]=len(b.below_bricks)
    q = [db]
    
    count = -1
    while len(q) > 0:
        count += 1
        b = q.pop()
        #print(b,len(b.above_bricks),len(b.below_bricks))
        for ab in b.above_bricks:
            number_of_supporting_bricks[ab] -= 1
            if number_of_supporting_bricks[ab] == 0:
                q.append(ab)
    return count


def do_your_magic1():
    s=0
    lines=list(utils.read_file_content(FILE))
    bricks=[]
    # read brickes from file
    for l in lines:
        b=Brick.from_input(len(bricks),l)
        bricks.append(b)

    # let the gravity to its things
    bricks=sorted(bricks,key=lambda x:x.min_z,reverse=False)
    taken_area={}
    for b in bricks:
        while not b.is_on_ground() and not has_anything_under(taken_area,b):
            b.move_down()
        op=b.occupied_points()
        for p in op:
            taken_area[p]=b
    
    # build a relationships
    for b in bricks:
        for p in b.points_below():
            if p in taken_area:
                b.set_below_brick(taken_area[p])
        for p in b.points_above():
            if p in taken_area:
                b.set_above_brick(taken_area[p])
                
    p1s=0
    for b in bricks:
        can_be_removed=True
        for ba in b.above_bricks:
            if len(ba.below_bricks)==1:
                can_be_removed=False
        if can_be_removed:
            p1s+=1

     # count
    print("counting")
    p2s=0
    for b in bricks:
        #print(b,len(b.below_bricks),len(b.above_bricks))
        p2s+=count_above_that_will_fall(b,bricks)
    
    print('done')
    print(p1s)
    print(p2s)
        
do_your_magic1()

# 448 legit for p1
# 57770 legit for p2
