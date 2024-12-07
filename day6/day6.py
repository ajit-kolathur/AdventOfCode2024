import copy

direction = [(-1,0), (0,1), (1,0), (0,-1)] # Up, Right, Down, Left

def find_next_pos(cord_x, cord_y, head):
    return (cord_x + direction[head][0], cord_y + direction[head][1])

def find_new_heading(head):
    return (head + 1) % 4

def will_end_up_looping(grid, init_x, init_y, init_head):
    visited_states = set()
    while (0 <= (find_next_pos(init_x, init_y, init_head)[0]) < len(grid)) and (0 <= (find_next_pos(init_x, init_y, init_head)[1]) < len(grid[0])):
        visited_states.add((init_x, init_y, init_head))
        tup = find_next_pos(init_x, init_y, init_head)
        new_pos_x = tup[0]
        new_pos_y = tup[1]

        if (new_pos_x,new_pos_y,init_head) in visited_states:
            return True


        if grid[new_pos_x][new_pos_y] == "#":
            init_head = find_new_heading(init_head)
            continue
        else:
            init_x = new_pos_x
            init_y = new_pos_y
    return False


def main():
    with open("./day6/input") as file:
        grid = [list(line.rstrip()) for line in file]
        init_grid = copy.deepcopy(grid)

    # (X,Y) --> X
    #  |
    #  v
    #  Y

    # Find starting position
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == '^':
                pos_x = x
                pos_y = y
                grid[x][y] = 'X'
            
    heading = 0
    valid_spots = 1
    loop_creating_obstacles = set()
    seen_states = set()

    start_x = pos_x
    start_y = pos_y
    start_heading = 0

    visited_position = set()

    while (0 <= (find_next_pos(pos_x, pos_y, heading)[0]) < len(grid)) and (0 <= (find_next_pos(pos_x, pos_y, heading)[1]) < len(grid[0])):
        seen_states.add((pos_x, pos_y, heading))
        # Debugger
        # print("---------------------------")
        # for line in grid:
        #     print(line)
        tup = find_next_pos(pos_x, pos_y, heading)
        new_x = tup[0]
        new_y = tup[1]

        if grid[new_x][new_y] == "#":
            heading = find_new_heading(heading)
            continue
        else:
            pos_x = new_x
            pos_y = new_y
            if grid[pos_x][pos_y] != 'X':
                grid[pos_x][pos_y] = 'X'
                valid_spots += 1
                visited_position.add((pos_x, pos_y))

    print(valid_spots) # Part 1

    loop_creating_obstacles = 0
    for spots in visited_position:
        temp_grid = copy.deepcopy(init_grid)
        temp_grid[spots[0]][spots[1]] = '#'
        if will_end_up_looping(temp_grid, start_x, start_y, start_heading):
            loop_creating_obstacles += 1

    print(loop_creating_obstacles) # Part 2
if __name__ == "__main__":
    main()