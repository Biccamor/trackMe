import time, random

world = [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,2,0,0,0,0,0]

for i in world:
    if i==1:
        start = i
    if i==2:
        end = i

def rewards(pos: int,end: int,  prev_pos: int) -> int:
    
    if pos == end:
        score+=100

    elif abs(end-pos) > abs(end-prev_pos):
        score -= 10

    elif abs(end-pos) < abs(end-prev_pos):
        score += 10

    elif pos == prev_pos:
        score -= 30 
    return score


def main():
     
    ...
          
        

if __name__ == "__main__": 
    main()