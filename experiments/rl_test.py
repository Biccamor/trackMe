import time, random

def init(world) -> tuple:
    for i in range(len(world)):
        for j in range(len(world[0])):
            if world[i][j]==1:
                start = [i,j]
            if world[i][j]==2:
                end = [i,j]
    
    return (start, end)

def manhattan_dist(pos: list, prev_pos: list, end: list) -> tuple:

    prev_dist = abs(prev_pos[0]-end[0]) + abs(prev_pos[1]-end[1])
    dist = abs(pos[0]-end[0]) + abs(pos[1]-end[1])

    return (prev_dist, dist)

def rewards(pos: list,end: list,  prev_pos: list) -> int:
    
    prev_dist, dist = manhattan_dist(pos,prev_pos,end)

    if pos[0] == end[0] and pos[1]==end[1]:
        return 100

    elif prev_dist < dist:
        return -15

    elif dist < prev_dist:
        return 10

    elif pos[0]==prev_pos[0] and pos[1]==prev_pos[1]:
        return -30

    elif dist == prev_dist:
        return -10
     

def boundaries(pos:int, length_x:int, length_y:int) -> int:
    
    if pos[0]<0:
        pos[0] = 0
    if pos[1]<0:
        pos[1]=0
    if pos[0]>length_y-1:
        pos[0]=length_y-1
    if pos[1]>length_x-1:
        pos[1] = length_x-1

    return pos 

def print_map(world: list,  pos: int, end: int):
    print("----------------------------------------------")
    result = ""
    for i, el in enumerate(world):
        for j, el in enumerate(world[0]): 
            if [i,j]==pos:
                result+="P"
            elif [i,j] == end:
                result += "M"
            else:
                result+="0"
        result += "\n"
    print(result)
    print("-----------------------------------------------")

def flatten_pos(pos:list, width: int) -> int:
    return pos[1] + pos[0]*width  # pos[0] to y a pos[1] to x 

def bellman_equation(q_table:list, lr: float, reward:int, pos: int, next_pos, move: int, width: int):
    pos  = flatten_pos(pos=pos, width=width)
    next_pos = flatten_pos(next_pos, width)
    
    gamma = 0.9
    old_value = q_table[pos][move]
    max_value = max(q_table[next_pos])
    new_value = old_value + lr * (reward + gamma * max_value- old_value)
    q_table[pos][move] = new_value

def choose_move(pos: int, q_table: list, eps: float, width: int) -> int:
    pos = flatten_pos(pos, width)
    
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
    q_table = [[0.0, 0.0, 0.0, 0.0] for _ in range(length*len(world[0]))]
    start, end = init(world)
    total_score = 0
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

    for epoch in range(120):
        pos = start.copy()
        total_score = 0
        step = 0
        while True:
            step +=1
            if epoch > 118:
                time.sleep(0.1)
                print_map(world,pos,end)

            idx = choose_move(pos, q_table, eps, len(world[0]))            
            prev_pos = pos.copy()
            pos = move(idx, pos, moves)
            pos = boundaries(pos, len(world[0]), length)
            reward = rewards(pos,end,prev_pos)
            bellman_equation(q_table,lr,reward,prev_pos,pos,idx, len(world[0]))
            total_score+=reward
            
            if pos == end:
                break
            if step > 100:
                break
        eps *= eps_rate
        eps = max(eps_min, eps)

        if epoch>118:
            print(total_score)
    

if __name__ == "__main__": 
    main()