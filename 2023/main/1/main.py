FILE='./data1'
FILE='./data1'
NUMBERS={
'1':1,'one':1,
'2':2,'two':2,
'3':3,'three':3,
'4':4,'four':4,
'5':5,'five':5,
'6':6,'six':6,
'7':7,'seven':7,
'8':8,'eight':8,
'9':9,'nine':9,
'0':0,'zero':0,
}


def read_file_content(file_path:str) -> list[str]:
    with open(file_path, 'r') as file:
        for line in file:
            ls=line.strip().rstrip('\n')
            if not ls:
                continue
            yield ls

def extract_number_from_line(line:str)->int:
    first_digit=None
    last_digit=None
    for c in line:
        if not c.isdigit():
            continue
        if first_digit is None:
            first_digit=c
        last_digit=c

    number=f'{first_digit}{last_digit}'
    return int(number)

def extract_number_from_line2(line:str)->int:
    first_index=99999999999
    first_digit=None
    last_index=-1
    last_digit=None
    for key in NUMBERS.keys():
        key_first_index = line.find(key)
        key_last_index = line.rfind(key)
        if key_first_index==-1:
            continue
        if key_first_index<first_index:
            first_index=key_first_index
            first_digit=str(NUMBERS[key])
        if key_last_index>last_index:
            last_index=key_last_index
            last_digit=str(NUMBERS[key])
    number=f'{first_digit}{last_digit}'
    return int(number)

   

def do_your_magic1():
    lines=read_file_content(FILE)
    s=0
    for l in lines:
        n=extract_number_from_line2(l)
        s+=n
    print('Total sum is: ', s)



do_your_magic1()

