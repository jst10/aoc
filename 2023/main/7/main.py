import re
import sys
import os
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utils import utils

FILE='./data2'

strength_map={
    'A':14, 
    'K':13, 
    'Q':12, 
    'J':1,#part 2 
    'T':10, 
    '9':9, 
    '8':8, 
    '7':7, 
    '6':6, 
    '5':5, 
    '4':4, 
    '3':3,  
    '2':2
}
class Hand:
    def __init__(self,cards:list,bid:int) -> None:
        self.cards=cards
        self.bid=bid
        self.cards_map=defaultdict(int)
        self.j_count=0
        for c in cards:
            self.cards_map[c]+=1
            if c=='J':
                self.j_count+=1
        self.score=self.calculate_score()
        
    
    def calculate_score(self):
        t=self.calculate_type()
        s=t
        for c in self.cards:
            s*=100
            s+=strength_map[c]
        return s
    def calculate_type(self)->int:
        t=0
        if self.is_five_of_kind():
            t=7
        elif self.is_four_of_kind():
            t=6
        elif self.is_full_house():
            t=5
        elif self.is_three_of_kind():
            t=4
        elif self.is_two_pair():
            t=3
        elif self.is_one_pair():
            t=2
        elif self.is_high_card():
            t=1
        else:
            raise Exception('invalid type')
        return t
    
    def is_five_of_kind(self):
        if self.j_count>0:
            return len(self.cards_map)<=2
        return len(self.cards_map)==1
        
    
    def is_four_of_kind(self):
        mc=0
        for c,count in self.cards_map.items():
            if c=='J':
                continue
            mc=count if count>mc else mc
        return (mc+self.j_count)==4
        
    def is_full_house(self):
        if self.j_count>0:
            return len(self.cards_map)==3
        else:
            return len(self.cards_map)==2
        
    def is_three_of_kind(self):
        mc=0
        for c,count in self.cards_map.items():
            if c=='J':
                continue
            mc=count if count>mc else mc
        return (mc+self.j_count)==3

    def is_two_pair(self):
        r2=0
        rs=0
        if self.j_count>=2:
            raise Exception('something is not ok: ',self.cards)
        for c,count in self.cards_map.items():
            if c=='J':
                continue
            if count==2:
                r2+=1
            if count==1:
                rs+=1
        return r2==2 or (r2==1 and self.j_count>0)

    def is_one_pair(self):
        r2=0
        rs=0
        for c,count in self.cards_map.items():
            if c=='J':
                continue
            if count==2:
                r2+=1
            if count==1:
                rs+=1
        return r2==1 or (r2==0 and self.j_count>0)
    def is_high_card(self):
        if self.j_count>0:
            raise Exception('not ok not ok')
        return len(self.cards_map)==5
        

    @staticmethod
    def from_input(input:str):
        p=input.strip().split(' ')
        bid=int(p[1].strip())
        cards=[]
        for c in p[0]:
            cards.append(c)
        return Hand(cards=cards,bid=bid)

def do_your_magic1():
    s=0
    hands=[]
    lines=list(utils.read_file_content(FILE))
    for l in lines:
        h=Hand.from_input(l)
        hands.append(h)
    hands.sort(key=lambda h: h.score, reverse=False)
    t=0
    for i,h in enumerate(hands):
        m=(i+1)*h.bid
        t+=m
        #print(i,': ',h.cards,'|',m," -> ",h.score) 
    print(t)
        
do_your_magic1()
# to high
250705934
250260487
249891215