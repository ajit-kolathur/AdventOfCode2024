import re
from collections import namedtuple
from PIL import Image
import numpy as np

Robot = namedtuple('Robot', ['px', 'py', 'vx', 'vy'])
robot_regex = r"p=(?P<px>[\-]*\d+),(?P<py>[\-]*\d+) v=(?P<vx>[\-]*\d+),(?P<vy>[\-]*\d+)"

def read_file(file_name):
    robots = []
    with open(file_name) as file:
        lines = [line for line in file]

    for line in lines:
        match = re.match(robot_regex, line)
        px = int(match.group("px"))
        py = int(match.group("py"))
        vx = int(match.group("vx"))
        vy = int(match.group("vy"))

        robots.append(Robot(px, py, vx, vy))
    return robots

def simulate_robots(robots, max_x, max_y, iter):
    grid = [(['.'] * max_x) for i in range(max_y)]

    for robot in robots:
        next_x = (robot.px + iter*robot.vx)%max_x
        next_y = (robot.py + iter*robot.vy)%max_y
        
        if grid[next_y][next_x] == '.':
            grid[next_y][next_x] = 1
        else:
            grid[next_y][next_x] += 1

    return grid

def debug_print(grid, file=None):
    for line in grid:
        line = [str(ele) for ele in line]
        if not file:
            print(''.join(line))
        else:
            file.write(''.join(line))
            file.write("\n")

def get_bots_per_quadrant(grid):
    q1 = 0
    q2 = 0
    q3 = 0
    q4 = 0

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if x < len(grid[0])//2 and y < len(grid)//2 and grid[y][x] != '.':
                q1 += grid[y][x]
            if x < len(grid[0])//2 and y > len(grid)//2 and grid[y][x] != '.':
                q2 += grid[y][x]
            if x > len(grid[0])//2 and y < len(grid)//2 and grid[y][x] != '.':
                q3 += grid[y][x]
            if x > len(grid[0])//2 and y > len(grid)//2 and grid[y][x] != '.':
                q4 += grid[y][x]
    return q1, q2, q3, q4

def clean_up(grid):
    cleaned_up = []
    for line in grid:
        cleaned_up_line = [ 0 if element == '.' else element for element in line]
        cleaned_up.append(cleaned_up_line)
    return cleaned_up

def main():
    # Test
    robots = read_file("./day14/test")
    grid = simulate_robots(robots, 11, 7, 100)
    q1,q2,q3,q4 = get_bots_per_quadrant(grid)
    # debug_print(grid)
    print(q1*q2*q3*q4)

    # Input Part1
    robots = read_file("./day14/input")
    scores = []

    for i in range(10000):
        grid = simulate_robots(robots, 101, 103, i)
        q1,q2,q3,q4 = get_bots_per_quadrant(grid)
        scores.append(q1*q2*q3*q4)
    print(scores.index(min(scores)))

    # Part2
    cleaned_up_grid = clean_up(simulate_robots(robots, 101, 103, 7774))
    my_array = np.array(cleaned_up_grid)
    im = Image.fromarray(my_array.astype('uint8')*255)
    im.save('./day14/output.jpg')

if __name__ == "__main__":
    main()