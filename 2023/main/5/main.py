import re
import sys
import os
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utils import utils

FILE='./data2'

different_maps=[
    'seed-to-soil map:',
    'soil-to-fertilizer map:',
    'fertilizer-to-water map:',
    'water-to-light map:',
    'light-to-temperature map:',
    'temperature-to-humidity map:',
    'humidity-to-location map:',
]

def parse_seeds_from_line(line)->list[int]:
    r1='seeds:\s*(.*)'
    m1 = re.match(r1, line)
    if not m1:
        print("Invalid line:",m1)
        return
    numbers=[int(n) for n in m1.group(1).strip().split(' ')]
    return numbers

class Rule():
    def __init__(self,src,dst,rng):
        self.src=src
        self.dst=dst
        self.rng=rng
    
    def merge(self, other)->bool:
        if self.src<=other.src and self.src+self.rng>=other.src+other.rng:
            if self.map_src(other.src)==other.map_src(other.src):
                return True
        elif other.src<=self.src and other.src+other.rng>=self.src+self.rng:
            if self.map_src(self.src)==other.map_src(self.src):
                self.src=other.src
                self.dst=other.dst
                self.rng=other.rng
                return True
        return False
    
    def map_src(self,src:int):
        if src>=self.src and src<(self.src+self.rng):
            return self.dst+(src-self.src)
        return None
    
    def __repr__(self):
        return f'{self.src}->{self.dst} {self.rng}x'
    
class Mapper:
    def __init__(self):
        self.rules=[]
    
    def add_rule(self,src:int,dst:int,rng:int):
        r=Rule(src=src,dst=dst,rng=rng)
        self.rules.append(r)
    
    def set_rules(self,rules:list):
        self.rules=rules
    

    def map_src_to_dst(self,src:int)->int:
        for r in self.rules:
            dst=r.map_src(src)
            if dst!=None:
                return dst
        return src
    
    def map_rule(self,mr)->list:
        # assuming that sort by src was already done before call
        rules=[]
        stSrc=mr.src
        stDst=mr.dst
        stRemaining=mr.rng
        for r in self.rules:
            if stDst<r.src:
                until=min(stDst+stRemaining,r.src)
                rng=until-stDst
                rules.append(Rule(
                src=stSrc,
                dst=stDst,
                rng=rng
                ))
                stSrc+=rng
                stDst+=rng
                stRemaining-=rng
            if stDst>=r.src and stDst<r.src+r.rng:
                offset=stDst-r.src
                untilStDst=min(stDst+stRemaining,r.src+r.rng)
                rng=untilStDst-stDst
                rules.append(Rule(
                    src=stSrc,
                    dst=r.dst+offset,
                    rng=rng
                    ))
                stSrc+=rng
                stDst+=rng
                stRemaining-=rng
            if stRemaining==0:
                break
        if stRemaining>0:
            rules.append(Rule(
                src=stSrc,
                dst=stDst,
                rng=stRemaining
            ))
        return rules
    
    def sort_rules_by_dst(self):
        self.rules=sorted(self.rules, key=lambda r: r.dst, reverse=False)
        
    def sort_rules_by_src(self):
        self.rules=sorted(self.rules, key=lambda r: r.src, reverse=False)


    def merge_rules_together(self):
        self.sort_rules_by_dst()
        new_rules=[]
        last_rule=None
        for r in self.rules:
            if last_rule==None or not last_rule.merge(r):
                last_rule=r
                new_rules.append(r)
    
        self.rules=new_rules

def parse_seeds_from_line2(line)->Mapper:
    numbers=parse_seeds_from_line(line)
    m=Mapper()
    for i in range(0,len(numbers),2):
        id=numbers[i]
        rng=numbers[i+1]
        m.add_rule(src=id,dst=id,rng=rng)
    return m
def parse_map_data(lines,i):
    count=0
    m=Mapper()
    # since I don't have empty lines and don't want to use regex
    # I am just cheking if line contains map, so that I know it is over
    while (i+count)<len(lines) and 'map' not in lines[i+count]:
        l=lines[i+count]
        count+=1
        numbers= [int(n) for n in l.strip().split(' ')]
        dst=numbers[0]
        src=numbers[1]
        rng=numbers[2]
        m.add_rule(src=src,dst=dst,rng=rng)
    return m, count


def p1(seed_ids:list[int],mappers:dict[str,Mapper])->tuple[int, int]:
    seed_to_location={seed_id:seed_id for seed_id in seed_ids}
    for map_name in different_maps:
        mapper=mappers[map_name]
        for seed_id in seed_ids:
            seed_to_location[seed_id]=mapper.map_src_to_dst(seed_to_location[seed_id])
        #if seed_id==13:
        #    print(seed_id,'->',seed_to_location[seed_id])
            
    min_location=None
    seed_min_location=None
    for seed_id, location in seed_to_location.items():
        if min_location is None or min_location>location:
            min_location=location
            seed_min_location=seed_id
    return seed_min_location, min_location

def p2(start_mapper:Mapper,mappers:dict[str,Mapper])->tuple[int, int]:
    start_mapper.sort_rules_by_dst()
    active_mapper=start_mapper
    for map_name in different_maps:
        m=mappers[map_name]
        all_new_rules=[]
        m.sort_rules_by_src()

        
        for r in active_mapper.rules:
            new_rules=m.map_rule(r)
            all_new_rules.extend(new_rules)
            #print('r: ',r,' -> ',new_rules)
            
        new_mapper=Mapper()
        new_mapper.set_rules(all_new_rules)
        new_mapper.merge_rules_together()
        new_mapper.sort_rules_by_dst()
        active_mapper=new_mapper
    active_mapper.sort_rules_by_dst()
    first=new_mapper.rules[0]
    return first.src, first.dst


def do_your_magic1():
    s=0
    lines=list(utils.read_file_content(FILE))
    i=0
    seed_ids=[]
    mappers={}
    while i<len(lines):
        l=lines[i].strip()
        i+=1
        if l=='':
            continue
        
        if l.startswith('seeds:'):
            seed_ids=parse_seeds_from_line(l)
            start_mapper=parse_seeds_from_line2(l)
        else:
            processed_line=False
            for map_name in different_maps:
                if l.startswith(map_name):
                    mapper,processed_lines=parse_map_data(lines,i)
                    mappers[map_name]=mapper
                    i+=processed_lines
                    processed_line=True
                    break;
            if not processed_line:
                raise Exception('Invalid line', l)
    seed_min_location,min_location=p1(seed_ids=seed_ids,mappers=mappers)
    print('done1')
    print(seed_min_location)
    print(min_location)
    seed_min_location,min_location=p2(start_mapper=start_mapper,mappers=mappers)
    print('done2')
    print(seed_min_location)
    print(min_location)
        
do_your_magic1()