import re
from collections import namedtuple

Machine = namedtuple('Machine', ['prize', 'a', 'b'])
Button = namedtuple('Button', ['cost', 'x', 'y'])
Prize = namedtuple('Prize', ['x', 'y'])

button_regex = r"(Button (?P<id>[A-Z]): X\+(?P<x>\d+), Y\+(?P<y>\d+))"
prize_regex = r"(Prize: X=(?P<x>\d+), Y=(?P<y>\d+))"
cost_a = 3
cost_b = 1

def read_input(file_name, offset):
    machines = []
    with open(file_name) as file:
        lines = file.read().split("\n")
    
    button_a = None
    button_b = None
    prize = None

    for i in range(len(lines)):
        line = lines[i]
        if (i%4 == 0) or (i%4 == 1):
            match = re.match(button_regex, line)
            id = match.group("id")
            x = match.group("x")
            y = match.group("y")
            if i%4 == 0:
                button_a = Button(id, int(x), int(y))
            if i%4 == 1:
                button_b = Button(id, int(x), int(y))
        if i%4 == 2:
            match = re.match(prize_regex, line)
            x = match.group("x")
            y = match.group("y")
            if offset:
                prize = Prize(10000000000000+int(x), 10000000000000+int(y))
            else:
                prize = Prize(int(x), int(y))
        if i%4 == 3:
            machines.append(Machine(prize, button_a, button_b))
    return machines

def dp_solution(button_a, button_b, x, y, memory):
    if (x,y) in memory:
        return memory[(x,y)]

    if x < 0 or y < 0:
        memory[(x, y)] = None
        return memory[(x, y)]
    if (x - button_a.x) == 0 and (y - button_a.y) == 0:
        temp = find_min_tokens_to_win(button_a, button_b, x - button_b.x, y - button_b.y, memory)
        if temp:
            memory[(x, y)] = min(cost_a, temp + cost_b)
        else:
            memory[(x, y)] =  cost_a
        return memory[(x, y)]
    if (x - button_b.x) == 0 and (y - button_b.y) == 0:
        temp = find_min_tokens_to_win(button_a, button_b, x - button_a.x, y - button_a.y, memory)
        if temp:
            memory[(x, y)] = min(cost_b, temp + cost_a)
        else:
            memory[(x, y)] =  cost_b
        return memory[(x, y)]
    
    # min tokens for a certain co-ordinate is min
    # between one a earlier and one b earlier
    min_by_a = find_min_tokens_to_win(button_a, button_b, x - button_a.x, y - button_a.y, memory)
    min_by_b = find_min_tokens_to_win(button_a, button_b, x - button_b.x, y - button_b.y, memory)

    if min_by_a and min_by_b:
        memory[(x, y)] = min(cost_a + min_by_a, cost_b + min_by_b)
        return memory[(x, y)]
    if min_by_a:
        memory[(x, y)] = cost_a + min_by_a
        return memory[(x, y)]
    if min_by_b:
        memory[(x, y)] = cost_b + min_by_b
        return memory[(x, y)]

    memory[(x, y)] = None
    return memory[(x, y)]
    

def math_solution(machine):
    # ButtonA = (ByPrizeX - BxPrizeY)/(AxBy - AyBx)
    # ButtonB = (AyPrizeX - AxPrizeY)/(AyBx - AxBy)
    button_a = (machine.prize.x*machine.b.y-machine.prize.y*machine.b.x)/(machine.a.x*machine.b.y-machine.a.y*machine.b.x)
    button_b = (machine.prize.x*machine.a.y-machine.prize.y*machine.a.x)/(machine.a.y*machine.b.x-machine.a.x*machine.b.y)

    return button_a*cost_a + button_b*cost_b

def main():
    machines = read_input("./day13/input", offset=True)
    # Part 1
    total_cost = 0
    for machine in machines:
        # memory = {}
        # cost = dp_solution(machine.a, machine.b, machine.prize.x, machine.prize,y, memory)
        cost = math_solution(machine)
        if cost and cost.is_integer():
            total_cost += cost
    print(total_cost)

if __name__ == "__main__":
    main()