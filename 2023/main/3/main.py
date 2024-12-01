FILE='./data2'

def read_file_content(file_path:str) -> list[str]:
    with open(file_path, 'r') as file:
        for line in file:
            ls=line.strip().rstrip('\n')
            if not ls:
                continue
            yield ls

def is_symbol(c):
    v= c is not None and c!='.' and not c.isdigit()
    return v

def get_item(data,index):
    if not data or index<0 or index>=len(data):
        return None
    return data[index]

def extract_stars(ll,li,si,ei):
    stars=[]
    for i in [li-1,li,li+1]:
        if i<0 or i>=len(ll):
            continue
        line=ll[i] 
        for j in range(si,ei):
            item=get_item(line,j)
            if item=='*':
                stars.append(str(i)+'|'+str(j))
    return stars

def do_your_magic1():
    lines=list(read_file_content(FILE))
    
    numbers=[]
    nl=len(lines)
    s=0
    sd={}
        
    for i in range(nl):
        previsou_line=lines[i-1] if i>0 else None
        current_line=lines[i]
        next_line=lines[i+1] if nl>i+1 else None
        digit_start=-1
        has_symbol=False
        for j,c in enumerate(current_line):
            if c.isdigit():
                if digit_start==-1:
                    digit_start=j
                
                for sl in (previsou_line,current_line,next_line):
                    has_symbol=has_symbol or is_symbol(get_item(sl,j-1))
                    has_symbol=has_symbol or is_symbol(get_item(sl,j))
                    has_symbol=has_symbol or is_symbol(get_item(sl,j+1))
                
            if not c.isdigit() or j+1==len(current_line):
                extra=0
                if  c.isdigit() and j+1==len(current_line):
                    extra=1
                if digit_start!=-1:
                    if has_symbol:
                        d=int(current_line[digit_start:(j+extra)])
                        s+=d
                        stars=extract_stars(lines,i,digit_start-1,(j+extra)+1)
                        for star in stars:
                            if star not in sd:
                                sd[star]=[]
                            sd[star].append(d)
                    digit_start=-1
                    has_symbol=False
            
    s2=0
    for _,nums in sd.items():
        if len(nums)==2:
            s2+=(nums[0]*nums[1])
        
    print(s)
    print(s2)



do_your_magic1()

# correct: 527446
