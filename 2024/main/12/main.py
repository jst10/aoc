import re
import sys
import os
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utils import utils

FILE='./data2'

def get_value(data,i,j):
    if i<0 or j<0 or i>=len(data) or j>=len(data[0]):
        return None
    return data[i][j]

def find_region(data,processed_fields:set,field:tuple):
    if field in processed_fields:
        return None
    region=[field]
    processed_fields.add(field)
    i,j=field
    c_v=get_value(data,i,j)
    for c in [(0,1),(1,0),(-1,0),(0,-1)]:
        n_i=i+c[0]
        n_j=j+c[1]
        n_v=get_value(data,n_i,n_j)
        if c_v==n_v:
            r=find_region(data,processed_fields,(n_i,n_j))
            if r is not None:
                region.extend(r)
    return region


def do_your_magic1():
    s=0
    lines=list(utils.read_file_content(FILE))
    data=[l for l in lines]
    
    h=len(data)
    w=len(data[0])
    processed_fields=set()
    regions=[]

    for i in range(h):
        for j in range(w):
            region=find_region(data,processed_fields,(i,j))
            if region is not None:
                regions.append(region)
    
    s=0
    for region in regions:
        sides=0
        horizontal=[]
        vertical=[]
        for field in region:
            i,j=field

            for d in [-1,1]:
                if (i,j+d) not in region:
                    vertical.append((i,j+d/10))
                if (i+d,j) not in region:
                    horizontal.append((i+d/10,j))
        # part 2
        sides=0
        previous=None
        horizontal_sorted=sorted(list(horizontal), key=lambda x: (x[0], x[1]))
        for f in horizontal_sorted:
            if previous is None or previous[0]!=f[0] or previous[1]+1!=f[1]:
                sides+=1
            previous=f
        previous=None
        
        vertical_sorted=sorted(list(vertical), key=lambda x: (x[1], x[0]))
        for f in vertical_sorted:
            if previous is None or previous[1]!=f[1] or previous[0]+1!=f[0]:
                sides+=1
            previous=f
        s+=(len(region)*sides)
    print(len(regions))
    print('done')
    print(s)
        
do_your_magic1()


# 838988