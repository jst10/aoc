import re
import sys
import os
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utils import utils

FILE='./data2'
class Galaxy:
    def __init__(self,x:int,y:int) -> None:
        self.x=x
        self.y=y

    def __repr__(self) -> str:
        return f'{self.x},{self.y}'

def distance(g1,g2):
    return abs(g2.y-g1.y)+abs(g2.x-g1.x)


def do_your_magic1():
    s=0
    lines=list(utils.read_file_content(FILE))
    galaxies=[]
    
    rows_with_galaxy={}
    columns_with_galaxy={}
    for i, l in enumerate(lines):
        for j,c in enumerate(l):
            if c=='#':
                rows_with_galaxy[i]=True
                columns_with_galaxy[j]=True

    extra_row=0
    extra_column=0
    for i, l in enumerate(lines):
        if i not in rows_with_galaxy:
            extra_row+=1000000-1
        extra_column=0
        for j,c in enumerate(l):
            if j not in columns_with_galaxy:
                extra_column+=1000000-1
                
            if c=='#':
                g=Galaxy(i+extra_row,j+extra_column)
                galaxies.append(g)
    s=0            
    for i in range(0,len(galaxies)):
        for j in range(i+1,len(galaxies)):
            g1=galaxies[i]
            g2=galaxies[j]
            d=distance(g1,g2)
            #print(f'{i}({g1})/{j}({g2})->{d}')
            s+=d
    print("done")
    print(s)
        
do_your_magic1()

#not ok 752936886232
# not ok 82000210