import time, random

def init(world) -> tuple:
    for i in range(len(world)):
        for j in range(len(world[0])):
            if world[i][j]==1:
                start = [i,j]
            if world[i][j]==2:
                end = [i,j]
    
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


def boundaries(pos:int, length_x:int, length_y:int) -> int:
    
    if pos[0]<0:
        pos[0] = 0
    if pos[1]<0:
        pos[1]=0
    if pos[0]>length_x-1:
        pos[0]=length_x-1
    if pos[1]>length_y-1:
        pos[1] = length_y-1

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

def bellman_equation(q_table:list, lr: float, reward:int, pos: int, next_pos, move: int):
    
    gamma = 0.9
    old_value = q_table[pos][move]
    max_value = max(q_table[next_pos])
    new_value = old_value + lr * (reward + gamma * max_value- old_value)
    q_table[pos][move] = new_value

def choose_move(pos: int, q_table: list, eps: float) -> int:
    if random.uniform(0,1) < eps:
        return random.choice([0,1,2,3])
    max_value = max(q_table[pos])
    index = q_table[pos].index(max_value)

    return index

def move(index: int, pos: int, moves:dict):
    
    pos[0] += moves[index][0]
    pos[1] += moves[index][1]

    return pos

def main():
    world = [[0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],]
    length = len(world)
    q_table = [[0.0, 0.0, 0.0, 0.0] for _ in range(length)]
    start, end = init(world)
    total_score = 0
    pos = start
    eps = 1.0
    eps_rate = 0.98
    eps_min = 0.01
    lr = 0.1
    moves = {
        0: [1,0],
        1: [-1,0],
        2: [0,1],
        3: [0,-1]
    }

    for epoch in range(50):
        pos = start
        total_score = 0
        step = 0
        while True:
            step +=1
            if epoch > 45:
                time.sleep(0.1)
                print_map(world,pos,end)
            idx = choose_move(pos, q_table, eps)            
            prev_pos = pos
            pos = move(idx, pos, moves)
            pos = boundaries(pos, len(world[0]), length)
            reward = rewards(pos,end,prev_pos)
            bellman_equation(q_table,lr,reward,prev_pos,pos,move)
            total_score+=reward
            
            if pos == end:
                break
            if step > 20:
                break
        eps *= eps_rate
        eps = max(eps_min, eps)

        if epoch>44:
            print(total_score)
    

if __name__ == "__main__": 
    main()