import time, random

def init(world) -> tuple:
    for i in range(len(world)):
        if world[i]==1:
            start = i
        if world[i]==2:
            end = i
    
    return (start, end)


def rewards(pos: int,end: int,  prev_pos: int) -> int:
    
    if pos == end:
        return 100

    elif abs(end-pos) > abs(end-prev_pos):
        return -10

    elif abs(end-pos) < abs(end-prev_pos):
        return 10

    elif pos == prev_pos:
        return -30 


def boundaries(pos, length) -> int:
    
    if pos<0:
        pos = 0

    if pos>length-1:
        pos = length-1

    return pos 

def main():
    world = [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,2,0,0,0,0,0]
    length = len(world)
    start, end = init(world)
    total_score = 0
    pos = start

    while True:
        move = input("key: ")
        if move == 'a':
            prev_pos = pos
            pos -= 1
            pos = boundaries(pos, length)
            total_score+=rewards(pos,end,prev_pos)

        elif move == 'd':
            prev_pos = pos
            pos+=1
            pos = boundaries(pos,length)                          
            total_score+=rewards(pos,end,prev_pos)
        print(total_score)
        if move == 'q':
            break

if __name__ == "__main__": 
    main()