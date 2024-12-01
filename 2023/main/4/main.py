import re
import sys
import os
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utils import utils

FILE='./data2'

# Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
r1='Card\s*(\d*):(.*)'
class Card:
    def __init__(self,id:int,wining_nums:set,my_nums:set) -> None:
        self.id=id
        self.wining_nums=wining_nums
        self.my_nums=my_nums

    def get_points(self)->int:
        matches=self.get_matches()
        return pow(2,(matches-1))
    
    def get_matches(self)->int:
        matches=0
        for n in self.my_nums:
            if n in self.wining_nums:
                matches+=1
        if matches==0:
            return 0
        return matches

    
    @staticmethod
    def from_input(input:str):
        m1 = re.match(r1, input)
        if not m1:
            print("Invalid line:",m1)
            return
        id=int(m1.group(1))
        remainings=m1.group(2).split('|')
        
        processed=[]
        for r in remainings:
            nums=[]
            for n in r.strip().split(' '):
                n=n.strip()
                if n=='':
                    continue
                nums.append(int(n))
            processed.append(nums)
        wining_nums=processed[0]
        my_nums=processed[1]

        return Card(
            id=id,
            wining_nums=set(wining_nums),
            my_nums=set(my_nums)
            )


def do_your_magic1():
    s=0
    lines=list(utils.read_file_content(FILE))
    cardsCounter=defaultdict(int)
    for l in lines:
        c=Card.from_input(l)
        cardsCounter[c.id]+=1
        m=c.get_matches()
        for i in range(m):
            cardsCounter[c.id+(i+1)]+=cardsCounter[c.id]
        s+=cardsCounter[c.id]
    print(s)
        
do_your_magic1()