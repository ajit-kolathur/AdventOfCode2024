import copy
from termcolor import colored

def find_all_trail_heads(grid):
    trail_heads = set()
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == 0:
                trail_heads.add((x,y))
    return trail_heads

def find_trails_to_nine(grid, x, y, path_so_far=[]):
    current_value = grid[x][y]
    next_value = current_value + 1

    # create copy of path to not mutate shared state
    up_path = copy.deepcopy(path_so_far)
    up_path.append((x,y))
    down_path = copy.deepcopy(path_so_far)
    down_path.append((x,y))
    left_path = copy.deepcopy(path_so_far)
    left_path.append((x,y))
    right_path = copy.deepcopy(path_so_far)
    right_path.append((x,y))

    if current_value == 9:
        return [up_path]

    valid_paths = []
    # search up
    if (0 <= (x-1) < len(grid)) and (grid[x-1][y] == next_value):
        valid_paths.extend(find_trails_to_nine(grid, x-1, y, up_path))
    # search down
    if (0 <= (x+1) < len(grid)) and (grid[x+1][y] == next_value):
        valid_paths.extend(find_trails_to_nine(grid, x+1, y, down_path))
    
    # search left
    if (0 <= (y-1) < len(grid[0])) and (grid[x][y-1] == next_value):
        valid_paths.extend(find_trails_to_nine(grid, x, y-1, left_path))
    # search right
    if (0 <= (y+1) < len(grid[0])) and (grid[x][y+1] == next_value):
        valid_paths.extend(find_trails_to_nine(grid, x, y+1, right_path))

    return valid_paths

def get_trail_head_score(paths):
    trail_tails = set()

    for path in paths:
        trail_tails.add(path[-1])
    return len(trail_tails)

def print_debug_paths(grid, paths):
    # Debugging
    for path in paths:
        clone_grid = copy.deepcopy(grid)
        for entry in path:
            clone_grid[entry[0]][entry[1]] = 'X'
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                print_val = grid[x][y]
                if clone_grid[x][y] == 'X':
                    print_val = colored(print_val, 'red')
                print(print_val, end='')
            print("\n", end='')
                
        print("------------------------------------")

def find_all_valid_trails(grid, trail_heads):
    part1_total_score = 0
    part2_total_score = 0
    for trail_head in trail_heads:
        paths = find_trails_to_nine(grid, trail_head[0], trail_head[1])
        # debug
        # print_debug_paths(grid, paths)
        part1_total_score += get_trail_head_score(paths)
        part2_total_score += len(paths)
    return part1_total_score, part2_total_score

def main():
    with open("./day10/input") as file:
        grid = [[int(element) if element != '.' else ' ' for element in list(line.rstrip())] for line in file]
    
    # Find the different trail heads
    trail_heads = find_all_trail_heads(grid)
    
    part1_total_score, part2_total_score = find_all_valid_trails(grid, trail_heads)
    print(part1_total_score)
    print(part2_total_score)

if __name__ == "__main__":
    main()
