import re
import sys
import os
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utils import utils

FILE='./data2'

def get_frist_invalid_level(levels:list):
    negative = None
    for i in range(1,len(levels)):
        diff=levels[i]-levels[i-1]
        if negative is not None:
            if negative and diff>0:
                return i
            if not negative and diff<0:
                return i
        else:
            negative=diff<0
            
        if diff==0 or abs(diff)>3:
            return i
    return -1

def do_your_magic1():
    s=0
    lines=list(utils.read_file_content(FILE))
    for l in lines:
        nums=[int(n) for n in l.split(' ')]
        ii1=get_frist_invalid_level(nums)
        ii2=get_frist_invalid_level(nums[1:])
        if ii1==-1 or ii2==-1:
            s+=1
            continue
        # remove ii1
        # remove ii1-1
        ii3=get_frist_invalid_level(nums[0:ii1]+nums[ii1+1:])
        ii4=get_frist_invalid_level(nums[0:ii1-1]+nums[ii1:])
        if ii3==-1 or ii4==-1:
            s+=1
            continue
        
    print('done')
    print(s)
        
do_your_magic1()