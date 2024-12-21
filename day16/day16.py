import copy
import heapq
from sortedcontainers import SortedSet

DIRECTIONS = [
    (0, 1, ">"),     # horizontal right
    (1, 0, "v"),      # vertical down
    (0, -1, "<"),     # horizontal left
    (-1, 0, "^"),       # vertical up
]

def get_race_map(file_name):
    with open(file_name) as file:
        lines = [line.rstrip() for line in file]
    return [list(line) for line in lines]

def find_start_and_end(grid):
    start = None
    end = None

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == 'S':
                start = (x,y)
            if grid[x][y] == 'E':
                end = (x,y)
    return start, end

def debug_print(grid):
    for line in grid:
        line = [str(ele) for ele in line]
        print(''.join(line))

class Point:
    def __init__(self, x, y, heading, distance, intermediates=[]):
        self.x = x
        self.y = y
        self.heading = heading
        self.distance = distance
        self.intermediates = intermediates

    def __lt__(self, other):
        return self._cmp_key() < other._cmp_key()
    
    def __gt__(self, other):
        return self._cmp_key() > other._cmp_key()
    
    def __eq__(self, other):
        return self._cmp_key() == other._cmp_key()

    def __ne__(self, other):
        return self._cmp_key() != other._cmp_key()

    def __hash__(self):
        return hash(self._cmp_key())
    
    def _cmp_key(self):
        return (self.distance, self.x, self.y, self.heading)

def get_all_valid_points(grid):
    unvisted = SortedSet()
    lookup = {}
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == 'S':
                points = [Point(x, y, 0, 0), Point(x, y, 1, 1000), Point(x, y, 2, 2000), Point(x, y, 3, 1000)]
            else:
                points = [Point(x, y, 0, float('inf')), Point(x, y, 1, float('inf')), Point(x, y, 2, float('inf')), Point(x, y, 3, float('inf'))]

            for point in points:
                lookup[(point.x, point.y, point.heading)] = point
                unvisted.add(point)
    return unvisted, lookup
                       

def get_lowest_path_score_dijkstra(grid, end):
    unvisted, lookup = get_all_valid_points(grid)
    min_distance = float('inf')
    visited_points = set()
    visited_points.add((end[0], end[1]))

    while len(unvisted) > 0:
        point = unvisted.pop(0)

        # When we have reached the end point, we dont really care about other later distances, return
        if point.x == end[0] and point.y == end[1]:
            visited_points.update(point.intermediates)
            min_distance = min(min_distance, point.distance)

        # All hope is lost since the univisted node likely has no path to get there
        if point.distance == float('inf'):
            break
        
        # Now lets start with actual work, update cost to get to 
        # There are three direction you can go, straight, left, right, update distances for each of them.

        # maintain heading
        next_point = Point(point.x + DIRECTIONS[point.heading][0], point.y + DIRECTIONS[point.heading][1], point.heading, point.distance + 1, point.intermediates + [(point.x, point.y)])
        # check what the current distance for that path and heading is
        if (0<= next_point.x < len(grid)) and (0<= next_point.y < len(grid[0])) and (grid[next_point.x][next_point.y] == '.' or grid[next_point.x][next_point.y] == 'S' or grid[next_point.x][next_point.y] == 'E'):
            existing_entry = lookup[(next_point.x, next_point.y, next_point.heading)]
            if existing_entry.distance > next_point.distance:
                unvisted.discard(existing_entry)
                del lookup[(next_point.x, next_point.y, next_point.heading)]
                unvisted.add(next_point)
                lookup[(next_point.x, next_point.y, next_point.heading)] = next_point
        
        # turn left
        anti_heading = (point.heading - 1)%4
        next_point = Point(point.x + DIRECTIONS[anti_heading][0], point.y + DIRECTIONS[anti_heading][1], anti_heading, point.distance + 1001, point.intermediates + [(point.x, point.y)])
        # check what the current distance for that path and heading is
        if (0<= next_point.x < len(grid)) and (0<= next_point.y < len(grid[0])) and (grid[next_point.x][next_point.y] == '.' or grid[next_point.x][next_point.y] == 'S' or grid[next_point.x][next_point.y] == 'E'):
            existing_entry = lookup[(next_point.x, next_point.y, next_point.heading)]
            if existing_entry.distance > next_point.distance:
                unvisted.discard(existing_entry)
                del lookup[(next_point.x, next_point.y, next_point.heading)]
                unvisted.add(next_point)
                lookup[(next_point.x, next_point.y, next_point.heading)] = next_point
        # turn right
        clock_heading = (point.heading + 1)%4
        next_point = Point(point.x + DIRECTIONS[clock_heading][0], point.y + DIRECTIONS[clock_heading][1], clock_heading, point.distance + 1001, point.intermediates + [(point.x, point.y)])
        # check what the current distance for that path and heading is
        if (0<= next_point.x < len(grid)) and (0<= next_point.y < len(grid[0])) and (grid[next_point.x][next_point.y] == '.' or grid[next_point.x][next_point.y] == 'S' or grid[next_point.x][next_point.y] == 'E'):
            existing_entry = lookup[(next_point.x, next_point.y, next_point.heading)]
            if existing_entry.distance > next_point.distance:
                unvisted.discard(existing_entry)
                del lookup[(next_point.x, next_point.y, next_point.heading)]
                unvisted.add(next_point)
                lookup[(next_point.x, next_point.y, next_point.heading)] = next_point

    return min_distance, visited_points

def find_lowest_scoring_path(grid):
    _, end = find_start_and_end(grid)
    return get_lowest_path_score_dijkstra(grid, end)

def main():
    race_map = get_race_map('./day16/test1')
    
    # Part 1
    # find lowest scoring path
    score, visited = find_lowest_scoring_path(race_map)
    print(score)

    # Part 2
    # retrace the path start to finish
    print(len(visited))
    for point in visited:
        race_map[point[0]][point[1]] = 'O'
    debug_print(race_map)

if __name__ == "__main__":
    main()