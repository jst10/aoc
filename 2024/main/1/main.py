import re
import sys
import os
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utils import utils

FILE='./data2'

def do_your_magic1():
    s=0
    lines=list(utils.read_file_content(FILE))
    list1=[]
    list2=[]
    for l in lines:
        p=l.split('   ')
        list1.append(int(p[0].strip()))
        list2.append(int(p[1].strip()))
    list1.sort()
    list2.sort()
    
    # part 1
    for i in range(0,len(list1)):
        s+=abs(list1[i]-list2[i])

    # part 2
    counted=defaultdict(int)
    s2=0
    for n in list2:
        counted[n]+=1
    for n in list1:
        s2+=(n*counted[n])
        

    print('done')
    print(s)
    print(s2)
        
do_your_magic1()