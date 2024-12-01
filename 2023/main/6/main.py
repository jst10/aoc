# Time:      7  15   30
# Distance:  9  40  200
 
RACES={
7:9,
15:40,
30:200,
}
RACES={
    71530:940200
}
# Time:        46     80     78     66
# Distance:   214   1177   1402   1024
RACES2={
46:214,
80:1177,
78:1402,
66:1024,
}
RACES={
    46807866:214117714021024
}


def calculates_ways_to_beat(duration:int,best_distance:int)->int:
    # v=t*a
    # d=t*v
    w=0
    for i in range(1,duration):
        d=(duration-i)*i
        if d>best_distance:
            w+=1
    return w

def do_your_magic1():
    r=1
    for duration,best_distance in RACES.items():
        ways_to_beat=calculates_ways_to_beat(
            duration=duration,
            best_distance=best_distance,
        )
        r*=ways_to_beat
    print('done')
    print(r)
        
        
do_your_magic1()