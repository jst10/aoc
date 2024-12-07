import re
import sys
import os
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utils import utils

FILE='./data2'
STATE_SEARCH_MUL=0
STATE_SEARCH_FIRST_NUMBER=1
#STATE_SEARCH_COMMA=2
STATE_SEARCH_SECOND_NUMBER=3
#STATE_SEARCH_END=4
#mul(11,8)

def do_your_magic1():
    s=0
    lines=list(utils.read_file_content(FILE))
    state=STATE_SEARCH_MUL
    dodont=None
    for l in lines:
        ll=len(l)
        i=0
        first_digit=''
        second_digit=''
        while i< ll:
            #print(l[i:i+4])
            if l[i:i+4]=='do()':
                dodont=True
            elif l[i:i+7]=='don\'t()':
                dodont=False

            
            if state==STATE_SEARCH_MUL:
                if l[i:i+4]=='mul(':
                    state=STATE_SEARCH_FIRST_NUMBER
                    first_digit=''
                    second_digit=''
                    i+=4
                else:
                    i+=1
            elif state==STATE_SEARCH_FIRST_NUMBER:
                if l[i].isdigit():
                    first_digit+=l[i]
                    if len(first_digit)>3:
                        state=STATE_SEARCH_MUL
                elif l[i]==',' and len(first_digit)>0:
                    state=STATE_SEARCH_SECOND_NUMBER
                else:
                    state=STATE_SEARCH_MUL
                i+=1
            elif state==STATE_SEARCH_SECOND_NUMBER:
                if l[i].isdigit():
                    second_digit+=l[i]
                    if len(second_digit)>3:
                        state=STATE_SEARCH_MUL
                elif l[i]==')' and len(second_digit)>0:
                    if dodont is None or dodont is True:
                        #print('found: ',first_digit,second_digit)
                        s+=int(first_digit)*int(second_digit)
                    state=STATE_SEARCH_MUL
                else:
                    state=STATE_SEARCH_MUL
                i+=1
            
        


        pass
    print('done')
    print(s)
        
do_your_magic1()