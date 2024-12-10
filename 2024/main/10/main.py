import re
import sys
import os
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utils import utils

FILE='./data2'

def get_number_of_trailheads(map_data,location):
    r, c=location
    c_h=map_data[r][c]
    
    if c_h==9:
        return [[location]]
    # left
    sub_paths=[]
    if c>0 and map_data[r][c-1]==c_h+1:
        p=get_number_of_trailheads(map_data,(r,c-1))
        sub_paths.extend(p)
     # righ
    if c+1<len(map_data[0]) and map_data[r][c+1]==c_h+1:
        p=get_number_of_trailheads(map_data,(r,c+1))
        sub_paths.extend(p)
    # up
    if r>0 and map_data[r-1][c]==c_h+1:
        p=get_number_of_trailheads(map_data,(r-1,c))
        sub_paths.extend(p)
    # down
    if r+1<len(map_data) and map_data[r+1][c]==c_h+1:
        p=get_number_of_trailheads(map_data,(r+1,c))
        sub_paths.extend(p)
    whole_paths=[]
    for sp in sub_paths:
        tmp=[location]
        tmp.extend(sp)
        whole_paths.append(tmp)
    return whole_paths


def do_your_magic1():
    lines=list(utils.read_file_content(FILE))
    map_data=[]
    start_locations=[]
    for i,l in enumerate(lines):
        one_row_data=[]
        for j,c in enumerate(l):
            one_row_data.append(int(c))
            if one_row_data[-1]==0:
                start_locations.append((i,j))
        map_data.append(one_row_data)
    #print(map_data)
    s1=0
    s2=0
    for start_location in start_locations:
        #print(start_location)
        ends=set()
        paths=get_number_of_trailheads(map_data, start_location)
        for p in paths:
            ends.add(p[-1])
            #print(p)
        s1+=len(ends)
        s2+=len(paths)
        #break;
    print('done')
    print(s1)
    print(s2)
    
        
do_your_magic1()