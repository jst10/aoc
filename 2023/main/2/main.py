import re

FILE='./data2'

# Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
r1='Game\s*(\d*):(.*)'
r2='[^\d]*((\d+)\s+([a-z]+))[^a-z]*'
class Game:
    def __init__(self,id:int,reveals:list[dict]) -> None:
        self.id=id
        self.reveals=reveals
    
    def can_be_played_with_boxes(self,boxes:{})->bool:
        for r in self.reveals:
            for color, count in r.items():
                if color not in boxes:
                    return False
                if boxes[color]<count:
                    return False
        return True
    
    def power(self)->int:
        min_values={}
        for r in self.reveals:
            for color, count in r.items():
                current_count=min_values.get(color,0)
                if current_count<count:
                    min_values[color]=count
        power=1
        for _,count in min_values.items():
            power*=count
        return power

    @staticmethod
    def from_input(input:str):
        m1 = re.match(r1, input)
        if not m1:
            print("Invalid line:",m1)
            return
        id=int(m1.group(1))
        remaining=m1.group(2)
        reveals=[]
        for r in remaining.split(';'):
            reveal={}
            for o in r.split(','):
                m2= re.match(r2,o)
                if not m2:
                    print("Invalid entry:")
                    print(o," <- ",r," <- ",input)
                    continue
                count=int(m2.group(2))
                color=m2.group(3)
                reveal[color]=count
            reveals.append(reveal)
        return Game(id=id,reveals=reveals)



def read_file_content(file_path:str) -> list[str]:
    with open(file_path, 'r') as file:
        for line in file:
            ls=line.strip().rstrip('\n')
            if not ls:
                continue
            yield ls

def do_your_magic1():
    lines=read_file_content(FILE)
    boxes={
        "red":12,
        "green":13,
        "blue":14,
    }
    s=0
    p_sum=0
    for l in lines:
        g=Game.from_input(l)
        if g.can_be_played_with_boxes(boxes):
            s+=g.id    
        p=g.power()
        p_sum+=p

    
    print(s)
    print(p_sum)
         
    

do_your_magic1()
