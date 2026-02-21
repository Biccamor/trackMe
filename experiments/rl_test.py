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

def print_map(world: list,  pos: int, end: int):
    print("----------------------------------------------")
    result = ""
    for i, el in enumerate(world): 
        if i==pos:
            result+="P"
        elif i == end:
            result += "M"
        else:
            result+="0"
    print(result)
    print("-----------------------------------------------")

def bellman_equation(learning_rate: float, eps: float, reward:int, pos: int):
    ...

def choose_move(pos: int, q_table: list, eps: float) -> int:
    if random.uniform(0,1) < eps:
        return random.choice([0,1])
    
    if q_table[pos][0] < q_table[pos][1]:
        return -1
    else:
        return 1

def main():
    world = [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,2,0,0,0,0,0]
    length = len(world)
    q_table = [[0.0, 0.0] for _ in range(length)]
    start, end = init(world)
    total_score = 0
    pos = start
    eps = 1.0
    eps_rate = 0.98
    eps_min = 0.01
    lr = 0.1

    for epoch in range(50):

        while True:

 
            print_map(world,pos,end)
            move = choose_move(pos, q_table, eps)            
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

            if pos == end:
                break

            if move == 'q':
                break
        
        eps *= eps_rate
        print(total_score)
    

if __name__ == "__main__": 
    main()