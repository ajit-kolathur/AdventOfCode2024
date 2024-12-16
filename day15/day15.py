import sys
import time
import copy

DIRECTIONS = [
    (0, 1, "right"),     # horizontal right
    (0, -1, "left"),     # horizontal left
    (1, 0, "down"),      # vertical down
    (-1, 0, "up"),       # vertical up
    (1, 1, "diagonal-down-right"),     # diagonal down-right
    (-1, -1, "diagonal-up-left"),      # diagonal up-left
    (1, -1, "diagonal-down-left"),     # diagonal down-left
    (-1, 1, "diagonal-up-right")       # diagonal up-right
]

def read_map_and_instructions(file_name, variation):
    map_lines = []
    instruction_lines = []

    with open(file_name) as file:
        still_map_lines = True
        for line in file:
            if line == '\n':
                still_map_lines = False
                continue
            if still_map_lines:
                map_lines.append(line)
            else:
                instruction_lines.append(line)
    if variation:
        map_lines = [line.replace("#", "##").replace("O", "[]").replace(".", "..").replace("@", "@.") for line in map_lines]
    grid = [list(line.rstrip()) for line in map_lines]
    instructions = []
    for line in instruction_lines:
        for entry in list(line.rstrip()):
            instructions.append(entry)
    return grid, instructions

def find_robot(grid):
    x = None
    y = None
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == '@':
                return x, y

def get_direction_from_instruction(instruction):
    match instruction:
        case '^':
            return 3
        case 'v':
            return 2
        case '<':
            return 1
        case '>':
            return 0

def move_if_possible(grid, x, y, direction):
    candidate_x = x +DIRECTIONS[direction][0]
    candidate_y = y +DIRECTIONS[direction][1]

    if grid[candidate_x][candidate_y] == '#':
        return None, None

    if grid[candidate_x][candidate_y] == 'O':
        return_x, return_y = move_if_possible(grid, candidate_x, candidate_y, direction)
        if not return_x or not return_y:
            return None, None
        
    temp = grid[x][y]
    grid[x][y] = '.'
    grid[candidate_x][candidate_y] = temp
    return candidate_x, candidate_y

def reset_grid(grid, copy_grid):
    grid.clear()
    for line in copy_grid:
        grid.append(line)

def move_if_possible_v2(grid, x, y, direction):
    candidate_x = x +DIRECTIONS[direction][0]
    candidate_y = y +DIRECTIONS[direction][1]

    if grid[candidate_x][candidate_y] == '#':
        return None, None

    if grid[candidate_x][candidate_y] == '[' or grid[candidate_x][candidate_y] == ']':
        ## If pushing from the left or right
        if direction <= 1: 
            return_x, return_y = move_if_possible_v2(grid, candidate_x, candidate_y, direction)
            if not return_x or not return_y:
                return None, None
        ## If pushing from the top or bottom
        if direction > 1:
            copy_grid = copy.deepcopy(grid)

            # if pushing '[' also push ']' on right side
            if grid[candidate_x][candidate_y] == '[':
                return_x_1, return_y_1 = move_if_possible_v2(grid, candidate_x, candidate_y, direction)
                return_x_2, return_y_2 = move_if_possible_v2(grid, candidate_x, candidate_y+1, direction)
            # if pushing ']' also push '[' on left side
            if grid[candidate_x][candidate_y] == ']':
                return_x_1, return_y_1 = move_if_possible_v2(grid, candidate_x, candidate_y, direction)
                return_x_2, return_y_2 = move_if_possible_v2(grid, candidate_x, candidate_y-1, direction)
            
            if not return_x_1 or not return_y_1 or not return_x_2 or not return_y_2:
                reset_grid(grid, copy_grid)
                return None, None
        
    temp = grid[x][y]
    grid[x][y] = '.'
    grid[candidate_x][candidate_y] = temp
    return candidate_x, candidate_y

def apply_instructions_on_grid(grid, instructions, func):
    bot_x, bot_y = find_robot(grid)

    for i in range(len(instructions)):
        instruction = instructions[i]
        # print(f"instruction: {i}, {instruction}")
        debug_print(grid)
        direction = get_direction_from_instruction(instruction)
        new_bot_x, new_bot_y = func(grid, bot_x, bot_y, direction)
        if new_bot_x and new_bot_y:
            bot_x, bot_y = new_bot_x, new_bot_y
        time.sleep(0.1)
        clear_screen(grid)
    return grid

def debug_print(grid):
    for line in grid:
        line = [str(ele) for ele in line]
        print(''.join(line))

def clear_screen(grid):
    for i in range(len(grid) + 1):
        sys.stdout.write("\033[F")  # Move cursor up one line
        sys.stdout.write("\033[K") 

def sum_all_gps_coordinates(grid):
    gps_sum = 0
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == 'O':
                gps_sum += 100*x + y
    return gps_sum

def sum_all_gps_coordinates_v2(grid):
    gps_sum = 0
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == '[':
                gps_sum += 100*x + y
    return gps_sum

def main():
    grid, instructions = read_map_and_instructions("./day15/input", variation=True)
    # Part 1 solution
    # new_grid = apply_instructions_on_grid(grid, instructions, move_if_possible)
    # debug_print(new_grid)
    # gps_sum = sum_all_gps_coordinates(new_grid)
    # print(gps_sum)
    # Part 2 solution
    new_grid = apply_instructions_on_grid(grid, instructions, move_if_possible_v2)
    # debug_print(new_grid)
    gps_sum = sum_all_gps_coordinates_v2(new_grid)
    print(gps_sum)

if __name__ == "__main__":
    main()