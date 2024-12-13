import re
import sys
import os
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utils import utils

FILE='./data2'
def split_stone_once(stone :int):
    if stone==0:
        return [1]
    
    str_rp=str(stone)
    if len(str_rp)%2==0:
        middle=int(len(str_rp)/2)
        n1=int(str_rp[:middle])
        n2=int(str_rp[middle:])
        return [n1,n2]
    return [stone*2024]

cache={}
def split_stone_n_time(stone :int,n:int):
    one_time_parts=split_stone_once(stone)
    if n==1:
        return len(one_time_parts)
    key=(stone,n)
    if key in cache:
        return cache[key]
    s=0
    for p in one_time_parts:
        s+=split_stone_n_time(p,n-1)
    cache[key]=s
    return s

def do_your_magic1():
    s=0
    lines=list(utils.read_file_content(FILE))
    stones=[]
    for l in lines:
        stones=[int(p) for  p  in l.split(' ')]

    s=0
    for stone in stones:
        s+=split_stone_n_time(stone,75)
    
    print('done')
    print(s)
        
do_your_magic1()