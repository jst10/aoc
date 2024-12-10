import re
import sys
import os
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utils import utils

FILE='./data2'

class Anthena:
    def __init__(self,f,x,y) -> None:
        self.f=f
        self.x=x
        self.y=y
    def __repr__(self) -> str:
        return f'{self.f}({self.x},{self.y})'

def do_your_magic1():
    s=0
    lines=list(utils.read_file_content(FILE))
    my=len(lines)
    mx=len(lines[0])
    anthenas_by_frequency=defaultdict(list)
    for y,l in enumerate(lines):
        for x,c in enumerate(l):
            if c=='.':
                continue
            anthenas_by_frequency[c].append(Anthena(c,x,y))
    
    #print(anthenas_by_frequency)
    antinodes=set()
    for f, athenas in anthenas_by_frequency.items():
        na=len(athenas)
        for i in range(na):
            for j in range(i+1,na):
                a1=athenas[i]
                a2=athenas[j]
                
                dx=a1.x-a2.x
                dy=a1.y-a2.y
                an1=(a1.x,a1.y)
                an2=(a2.x,a2.y)
                out_of_grid=False
                while not out_of_grid:
                    was_added=False   
                    if 0<=an1[0]<mx and 0<=an1[1]<my:
                        was_added=True
                        antinodes.add(an1)
                    if 0<=an2[0]<mx and 0<=an2[1]<my:
                        was_added=True
                        antinodes.add(an2)
                    an1=(an1[0]+dx,an1[1]+dy)
                    an2=(an2[0]-dx,an2[1]-dy)
                    out_of_grid=not was_added
    #for y in range(my):
    #    l=''
    #    for x in range(mx):
    #        if (x,y) in antinodes:
    #            l+='#'
    #        else:
    #            l+='.'
    #    print(l)
    print('done')
    print(s)
    print(len(antinodes))
        
do_your_magic1()

# 300 not ok
# 283 not ok