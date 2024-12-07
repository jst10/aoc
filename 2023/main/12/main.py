import re
import sys
import os
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utils import utils

FILE='./data1'

def count_posibilities_slow(text, patterns, c_sq=0):
    t_i=0
    p_i=0
    new_text=''
    for t_i, character in enumerate(text):
        
        if c_sq and p_i>=len(patterns):
            return []
        
        if character=='.':
            new_text+='.'
            if c_sq!=0:
                if c_sq!=patterns[p_i]:
                    return []
                p_i+=1
                c_sq=0
            
        elif character=='#':
            new_text+='#'
            c_sq+=1
        elif character=='?':
            if c_sq!=0:
                if c_sq!=patterns[p_i]:
                    # should be #
                    c_sq+=1
                    new_text+='#'
                else:
                    # should be .
                    p_i+=1
                    c_sq=0
                    new_text+='.'
            else:
                # case when is #
                p1=count_posibilities_slow(text[t_i+1:], patterns[p_i:],c_sq=1)
                p1=[new_text+p for p in p1]
                # case when is .
                p2=count_posibilities_slow(text[t_i+1:], patterns[p_i:],c_sq=0)
                p2=[new_text+p for p in p2]
                return p1+p2
    
    if p_i!=len(patterns):
        return []
    return [new_text]

def count_posibilities_fast(text, patterns):
    t_l=len(text)
    p_l=len(patterns)

#    2 3 4
#   .
#   #
#   .
def do_your_magic1():
    s=0
    lines=list(utils.read_file_content(FILE))
    for l in lines:
        parts=l.split(' ')
        text=parts[0]
        groups=[int(n) for n in parts[1].split(',')]
        
        unfoled_text=text
        unfoled_groups=list(groups)
        for i in range(0):
            unfoled_text+="?"+text
            unfoled_groups+=groups
        # adding dot at the end, so that don't need to iplement end logic
        unfoled_text+='.'
        posibilities=count_posibilities_slow(unfoled_text,unfoled_groups)
        #print(unfoled_text,': ',len(posibilities))
        #for p in posibilities:
        #    print(p)
        s+=len(posibilities)
        
    print('done')
    print(s)
        
do_your_magic1()
