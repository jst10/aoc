import re
import sys
import os
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utils import utils

FILE='./data2'
class Sequence:
    def __init__(self,numbers=[]) -> None:
        self.numbers=numbers

    def prediction(self)->int:
        return Sequence.prediction_r(self.numbers)
    
    @staticmethod
    def prediction_r(numbers:list[int])->int:
        if Sequence.are_zeros(numbers):
            return 0
        diffs=Sequence.get_diffs(numbers)
        # Part 1 forward
        # p=Sequence.prediction_r(diffs)
        # return numbers[-1]+p
        # Part 2 backward
        p=Sequence.prediction_r(diffs)
        return numbers[0]-p
        

    @staticmethod
    def get_diffs(numbers:list[int])->list[int]:
        diffs=[]
        
        for i in range(1,len(numbers)):
            diffs.append(numbers[i]-numbers[i-1])
        return diffs
    
    @staticmethod
    def are_zeros(numbers:list[int]):
        return all(item == 0 for item in numbers)
    @staticmethod
    def from_input(input:str):
        numbers_str=input.strip().split(' ')
        numbers=[int(n)for n in numbers_str]
        return Sequence(numbers=numbers)
def do_your_magic1():
    s=0
    lines=list(utils.read_file_content(FILE))
    
    for l in lines:
        sequence=Sequence.from_input(l)
        s+=sequence.prediction()
    print('done')
    print(s)
        
do_your_magic1()