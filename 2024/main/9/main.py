import re
import sys
import os
from collections import defaultdict
from queue import PriorityQueue
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utils import utils
import heapq

FILE='./data2'

def solution1(file_system):
    i=0
    j=len(file_system)-1        

    while True:
        if i>j:
            break
        if file_system[i]!=-1:
            i+=1
            continue
        if file_system[j]==-1:
            j-=1
            continue
        file_system[i]=file_system[j]
        file_system[j]=-1
        i+=1
        j-=1
def solution2(file_system, free_spaces):
    j=len(file_system)-1        

    while j>0:
        if file_system[j]==-1:
            j-=1
            continue
        size=1
        while file_system[j-size]==file_system[j]:
            size+=1
        #print(file_system[j-size],'<->',file_system[j])
        #print(file_system[j-size]!=file_system[j])
        available_slots={}
        for i in range(size,10):
            if not free_spaces[i].empty():
                min_index=free_spaces[i].queue[0]
                available_slots[min_index]=i
        if not available_slots:
            j-=size
            continue

        first_slot_index=min(available_slots.keys())
        if first_slot_index>j:
            j-=size
            continue
        size_of_first_slot=available_slots[first_slot_index]
        free_spaces[size_of_first_slot].get()

        for i in range(0,size):
            file_system[first_slot_index+i]=file_system[j-i]
            file_system[j-i]=-1
        remaining_size_free_slot=size_of_first_slot-size
        if remaining_size_free_slot:
            free_spaces[remaining_size_free_slot].put(first_slot_index+size)
        j-=size

def do_your_magic1():
    s=0
    lines=list(utils.read_file_content(FILE))
    file_system=[]
    
    free_spaces=[PriorityQueue() for _ in range(10)]
    for l in lines:
        file_id=0
        for i in range(0,len(l),2):
            file_system+=[file_id]*int(l[i])
            if (i+1)<len(l) and int(l[i+1])>0:
                free_space_size=int(l[i+1])
                free_spaces[free_space_size].put(len(file_system))
                file_system+=[-1]*int(l[i+1])
            file_id+=1
    
    #solution1(file_system)
    solution2(file_system,free_spaces)
    s=0
    for i in range(0,len(file_system)):
        if file_system[i]==-1:
            continue
        s+=i*file_system[i]
    print('done')
    print(s)
        
do_your_magic1()