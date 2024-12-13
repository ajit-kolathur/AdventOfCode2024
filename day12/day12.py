from collections import namedtuple

Region = namedtuple('Region', ['plant', 'points', 'area', 'perimeter', 'sides'])
Point = namedtuple('Point', ['x', 'y'])
PointDirections = namedtuple('PointDirections', ['point', 'direction'])

DIRECTIONS = [
    (-1, 0, "up"),       # vertical up
    (0, 1, "right"),     # horizontal right
    (1, 0, "down"),      # vertical down
    (0, -1, "left"),     # horizontal left
]

def discover_region(grid, point):
    plant = grid[point.x][point.y]
    points = set()
    perimeter = 0

    points_left_to_explore = [point]

    while len(points_left_to_explore) > 0:
        point_to_explore = points_left_to_explore.pop(0)
        if point_to_explore in points:
            continue
        points.add(point_to_explore)
        x = point_to_explore.x
        y = point_to_explore.y
        # Can I go up?
        if (0 <= (x - 1) < len(grid)) and grid[x-1][y] == plant:
            if Point(x-1, y) not in points:
                points_left_to_explore.append(Point(x-1, y))
        else:
            if Point(x-1, y) not in points:
                perimeter += 1
        # Can I go down?
        if (0 <= (x + 1) < len(grid)) and grid[x+1][y] == plant:
            if Point(x+1, y) not in points:
                points_left_to_explore.append(Point(x+1, y))
        else:
            if Point(x+1, y) not in points:
                perimeter += 1
        # Can I go left?
        if (0 <= (y - 1) < len(grid[0])) and grid[x][y-1] == plant:
            if Point(x, y-1) not in points:
                points_left_to_explore.append(Point(x, y-1))
        else:
            if Point(x, y-1) not in points:
                perimeter += 1
        # Can I go right?
        if (0 <= (y + 1) < len(grid[0])) and grid[x][y+1] == plant:
            if Point(x, y+1) not in points:
                points_left_to_explore.append(Point(x, y+1))
        else:
            if Point(x, y+1) not in points:
                perimeter += 1
    return Region(plant, points, len(points), perimeter, count_number_of_corners(grid, points, plant))

def find_all_points_in_grid(grid):
    all_points = set()
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            all_points.add(Point(x,y))
    return all_points

def find_all_regions_in_grid(grid):
    regions = []
    all_unexplored_points = find_all_points_in_grid(grid)
    
    while len(all_unexplored_points) > 0:
        point = next(iter(all_unexplored_points))
        region = discover_region(grid, point)
        all_unexplored_points = all_unexplored_points.difference(region.points)
        regions.append(region)
    return regions

def is_adjacent_point_outside_region(grid, point, direction, plant):
    adj_point_x = point.x + DIRECTIONS[direction][0]
    adj_point_y = point.y + DIRECTIONS[direction][1]

    if (0 <= (adj_point_x) < len(grid)) and (0 <= (adj_point_y) <len(grid[0])) and grid[adj_point_x][adj_point_y] == plant:
        return False
    else:
        return True

def count_number_of_corners(grid, points, plant):
    corners = 0
    for point in points:
        # check if is an inward corner
        # ie 2 consecutive directions are outside the grid or another plan
        if (is_adjacent_point_outside_region(grid, point, 0, plant) and is_adjacent_point_outside_region(grid, point, 1, plant)):
            corners += 1
        if (is_adjacent_point_outside_region(grid, point, 1, plant) and is_adjacent_point_outside_region(grid, point, 2, plant)):
            corners += 1
        if (is_adjacent_point_outside_region(grid, point, 2, plant) and is_adjacent_point_outside_region(grid, point, 3, plant)):
            corners += 1
        if (is_adjacent_point_outside_region(grid, point, 3, plant) and is_adjacent_point_outside_region(grid, point, 0, plant)):
            corners += 1
        # check if is an outward corner
        # ie same side of 2 consecutive adjacent squares are outside region and are the same plant
        left_point = Point(point.x + DIRECTIONS[3][0], point.y + DIRECTIONS[3][1])
        right_point = Point(point.x + DIRECTIONS[1][0], point.y + DIRECTIONS[1][1])
        up_point = Point(point.x + DIRECTIONS[0][0], point.y + DIRECTIONS[0][1])
        down_point = Point(point.x + DIRECTIONS[2][0], point.y + DIRECTIONS[2][1])

        if ((left_point in points) and (down_point in points) and is_adjacent_point_outside_region(grid, left_point, 2, plant) and is_adjacent_point_outside_region(grid, down_point, 3, plant)):
            corners += 1
        if ((left_point in points) and (up_point in points) and is_adjacent_point_outside_region(grid, left_point, 0, plant) and is_adjacent_point_outside_region(grid, up_point, 3, plant)):
            corners += 1
        if ((right_point in points) and (up_point in points) and is_adjacent_point_outside_region(grid, right_point, 0, plant) and is_adjacent_point_outside_region(grid, up_point, 1, plant)):
            corners += 1
        if ((right_point in points) and (down_point in points) and is_adjacent_point_outside_region(grid, right_point, 2, plant) and is_adjacent_point_outside_region(grid, down_point, 1, plant)):
            corners += 1
    return corners

def calculate_fencing_cost(regions):
    cost1 = 0
    cost2 = 0
    for region in regions:
        cost1 += region.perimeter * region.area
        cost2 += region.sides * region.area
    return cost1, cost2


def main():
    with open("./day12/input") as file:
        grid = [list(line.rstrip()) for line in file]
    
    # Part 1
    regions = find_all_regions_in_grid(grid)
    part1, part2 = calculate_fencing_cost(regions)
    
    print(part1)
    print(part2)

if __name__ == "__main__":
    main()
