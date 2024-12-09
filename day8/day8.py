import copy

def is_valid_coordinate(x, y, max_x, max_y):
    if (0 <= x < max_x) and (0 <= y < max_y):
        return True
    return False

def get_antinodes_for_pair(a, b, max_x, max_y, func):
    return func(a, b, max_x, max_y)

def part1_func(a, b, max_x, max_y):
    diff_x = b[0] - a[0]
    diff_y = b[1] - a[1]

    antinode_1_x = b[0] + diff_x
    antinode_1_y = b[1] + diff_y
    antinode_2_x = a[0] - diff_x
    antinode_2_y = a[1] - diff_y

    antinodes = []

    if is_valid_coordinate(antinode_1_x, antinode_1_y, max_x, max_y):
        antinodes.append((antinode_1_x, antinode_1_y))
    if is_valid_coordinate(antinode_2_x, antinode_2_y, max_x, max_y):
        antinodes.append((antinode_2_x, antinode_2_y))

    return antinodes

def part2_func(a, b, max_x, max_y):
    diff_x = b[0] - a[0]
    diff_y = b[1] - a[1]

    temp_diff_a_x = a[0]
    temp_diff_a_y = a[1]
    temp_diff_b_x = b[0]
    temp_diff_b_y = b[1]
    
    antinodes = []
    while is_valid_coordinate(temp_diff_b_x + diff_x, temp_diff_b_y + diff_y, max_x, max_y):
        antinodes.append((temp_diff_b_x + diff_x, temp_diff_b_y + diff_y))
        temp_diff_b_x += diff_x
        temp_diff_b_y += diff_y

    while is_valid_coordinate(temp_diff_a_x - diff_x, temp_diff_a_y - diff_y, max_x, max_y):
        antinodes.append((temp_diff_a_x - diff_x, temp_diff_a_y - diff_y))
        temp_diff_a_x -= diff_x
        temp_diff_a_y -= diff_y

    return antinodes
        
def main():
    with open("./day8/input") as file:
        grid = [list(line.rstrip()) for line in file]
        clone_grid = copy.deepcopy(grid)

    # Traverse the grid to find all co-ordinate tuples of a character
    antennas = {}
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] != '.':
                antenna_type = grid[x][y]
                if antenna_type not in antennas:
                    antennas[antenna_type] = []
                antennas[antenna_type].append((x,y))

    # Now iterate on pairs and calculate antinodes
    antinodes_part1 = set()
    antinodes_part2 = set()

    for antenna_type, coordinates in antennas.items():
        for i in range(len(coordinates)):
            a = coordinates[i]
            if len(coordinates) > 1:
                antinodes_part2.add(a)
            for j in range(i+1, len(coordinates)):
                b = coordinates[j]

                part1_antinode_candidates = get_antinodes_for_pair(a, b, len(grid), len(grid[0]), part1_func)
                antinodes_part1.update(part1_antinode_candidates)

                part2_antinode_candidates = get_antinodes_for_pair(a, b, len(grid), len(grid[0]), part2_func)
                antinodes_part2.update(part2_antinode_candidates)

                for coord in part2_antinode_candidates:
                    if clone_grid[coord[0]][coord[1]] == '.':
                        clone_grid[coord[0]][coord[1]] = '#'

    print(len(antinodes_part1)) # Part 1
    print(len(antinodes_part2)) # Part 2

    # for line in clone_grid:
    #     print(''.join(line))

if __name__ == "__main__":
    main()
