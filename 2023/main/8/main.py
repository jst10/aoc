import re
import sys
import os
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utils import utils

FILE='./data2'
r1='([\dA-Z]*)\s*=\s*\(([\dA-Z]*),\s*([\dA-Z]*)\)'

class Node():
    def __init__(self,id:str,left:str,right:str) -> None:
        self.id=id
        self.left=left
        self.right=right
        self.is_start_node=self.id[2]=='A'
        self.is_end_node=self.id[2]=='Z'
    
    @staticmethod
    def from_input(input:str):
        m1 = re.match(r1, input)
        if not m1:
            raise Exception('Invalid input:',input)
        return Node(
            id=m1.group(1),
            left=m1.group(2),
            right=m1.group(3),
        )

def compute_gcd(x, y):
   while(y):
       x, y = y, x % y
   return x

def lcm(x, y):
   lcm = (x*y)//compute_gcd(x,y)
   return lcm

def lcm_of_list(numbers):
    result = numbers[0]
    for num in numbers[1:]:
        result = lcm(result, num)
    return result

def do_your_magic1():
    s=0
    lines=list(utils.read_file_content(FILE))
    instructions=None
    nodes=[]
    for l in lines:
        if instructions is None:
            instructions=l
            continue
        n=Node.from_input(l)
        nodes.append(n)
    nodes_dict={n.id:n for n in nodes}
    
    active_nodes=[n for n in nodes if n.is_start_node]
    active_nodes_c=len(active_nodes)
    nums=[]
    for a in active_nodes:
        active_node=a
        count=0
        instruction_index=0
        while True:
            if active_node.is_end_node:
                break
            i=instructions[instruction_index]
            instruction_index+=1
            instruction_index%=len(instructions)
            count+=1
            if i=='L':
                active_node=nodes_dict[active_node.left]
            elif i=='R':
                active_node=nodes_dict[active_node.right]
            else:
                raise Exception('Invalid instruction: ', i)
        nums.append(count)
    
    print('done')
    print(nums)
    print(lcm_of_list(nums))
        
do_your_magic1()


# 13524038372771
# 13524038372771