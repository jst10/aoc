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
    rules=set()
    updates=[]
    for l in lines:
        if '|' in l:
            #p=l.split('|')
            #rules.append(int(p[0]),int(p[1]))
            rules.add(l)
        else:
            updates.append([int(n) for n in l.split(',')])
    s=0
    for u in updates:
        #print(u)
        is_ok=True
        i=0
        while i < len(u):
            for j in range(i+1, len(u)):
                r=f'{u[i]}|{u[j]}' 
                if r not in rules:
                    is_ok=False
                    tmp=u[i]
                    u[i]=u[j]
                    u[j]=tmp
                    i-=1
                    break
               
            i+=1
        if not is_ok:
            s+=u[int(len(u)/2)]
    print('done')
    print(s)
        
do_your_magic1()