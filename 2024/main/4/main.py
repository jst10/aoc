import re
import sys
import os
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utils import utils

FILE='./data2'

def is_match1(data,i,j,delta_i,delta_j):
    # searching for XMAS
    word=''
    for c in range(0,4):
        word+=data[i][j]
        i+=delta_i
        j+=delta_j
        if i<0 or j<0 or i>=len(data) or j>=len(data[0]):
            break
    return word=='XMAS'

def is_match2(data,i,j,delta_i,delta_j):
    # searching for MAS
    word=''
    for c in range(0,3):
        if i<0 or j<0 or i>=len(data) or j>=len(data[0]):
            break
        word+=data[i][j]
        i+=delta_i
        j+=delta_j
        if i<0 or j<0 or i>=len(data) or j>=len(data[0]):
            break
    return word=='MAS'

def do_your_magic1():
    s=0
    lines=list(utils.read_file_content(FILE))
    data=[]
    for l in lines:
        ld=[]
        for c in l:
            ld.append(c)
        data.append(ld)

    n_r=len(data)
    n_c=len(data[0])
    s=0
    for i in range(0,n_r):
        for j in range(0,n_c):
            # \
            m1=is_match2(data,i-1,j-1,1,1)
            m2=is_match2(data,i+1,j+1,-1,-1)

            # /
            m3= is_match2(data,i-1,j+1,1,-1) 
            m4= is_match2(data,i+1,j-1,-1,1) 

            s+=1 if ((m1 or m2) and (m3 or m4)) else 0

    print('done')
    print(s)
        
do_your_magic1()