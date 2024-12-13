import re
import sys
import os
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utils import utils

FILE='./data1'

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
        outline=set()
        for field in region:
            i,j=field
            for c in [(0,1),(1,0),(-1,0),(0,-1)]:
                n_i=i+c[0]
                n_j=j+c[1]
                if (n_i,n_j) not in region:
                    #sides+=1
                    outline.add((n_i,n_j))
        # part 2
        print(len(outline))
        sides=0
        outline_l=list(outline)
        horizontal=sorted(outline_l, key=lambda x: (x[1], x[0]))
        previous=None
        print('horizontal')
        print(horizontal)
        for f in horizontal:
            if previous is None or previous[1]!=f[1] or previous[0]+1!=f[0]:
                sides+=1
            previous=f
        vertical=sorted(outline_l, key=lambda x: (x[0], x[1]))
        previous=None
        print('vertical')
        print(vertical)
        for f in vertical:
            if previous is None or previous[0]!=f[0] or previous[1]+1!=f[1]:
                sides+=1
            previous=f
        print('sides: ',sides)
        s+=(len(region)*sides)
    print(len(regions))
    print('done')
    print(s)
        
do_your_magic1()