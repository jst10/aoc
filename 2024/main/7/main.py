import re
import sys
import os
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utils import utils

FILE='./data2'
def can_be_calculated(test_result,numbers):
    if len(numbers)==1:
        return test_result==numbers[0]
    t1=test_result-numbers[0]
    c1=can_be_calculated(t1,numbers[1:])
    t2=test_result/numbers[0]
    c2=can_be_calculated(t2,numbers[1:])
    

    return c1 or c2
    # 3267 = 81 + 40 * 27
    # c = a + b
    # c = a * b
def get_all_solutions(numbers,max_limit):
        if numbers[0]>max_limit:
             return set()
        if len(numbers)==1:
            return set([numbers[0]])
        r=set()
        cn1=[n for n in numbers[1:]]
        cn1[0]=numbers[0]+numbers[1]
        r1=get_all_solutions(cn1,max_limit)
        cn2=[n for n in numbers[1:]]
        cn2[0]=numbers[0]*numbers[1]
        r2=get_all_solutions(cn2,max_limit)
        cn3=[n for n in numbers[1:]]
        cn3[0]=int(str(numbers[0])+str(numbers[1]))
        r3=get_all_solutions(cn3,max_limit)
        return r.union(r1).union(r2).union(r3)
def do_your_magic1():
    s=0
    lines=list(utils.read_file_content(FILE))
    for i,l in enumerate(lines):
        parts=l.split(':')
        test_result=int(parts[0].strip())
        numbers=[int(n.strip()) for n in parts[1].strip().split(' ')]
        #numbers.reverse()
        r=get_all_solutions(numbers,test_result)
        print(i)
        if test_result in r:
        #if can_be_calculated(test_result,numbers):
            s+=test_result
    print('done')
    print(s)
        
do_your_magic1()