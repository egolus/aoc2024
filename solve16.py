from aocd import submit, get_data
from collections import defaultdict, deque
import sys
from pprint import pprint

sys.setrecursionlimit(1_000_000_000)


def main():
    day = 16
    year = 2024
    data = get_data(day=day, year=year)

    test_data_a = {
            """###############
            #.......#....E#
            #.#.###.#.###.#
            #.....#.#...#.#
            #.###.#####.#.#
            #.#.#.......#.#
            #.#.#####.###.#
            #...........#.#
            ###.#.#####.#.#
            #...#.....#.#.#
            #.#.#.###.#.#.#
            #.....#...#.#.#
            #.###.#.#.#.#.#
            #S..#.....#...#
            ###############""": 7036,
    }
    test_data_b = {
            """###############
            #.......#....E#
            #.#.###.#.###.#
            #.....#.#...#.#
            #.###.#####.#.#
            #.#.#.......#.#
            #.#.#####.###.#
            #...........#.#
            ###.#.#####.#.#
            #...#.....#.#.#
            #.#.#.###.#.#.#
            #.....#...#.#.#
            #.###.#.#.#.#.#
            #S..#.....#...#
            ###############""": 45,
            """#################
            #...#...#...#..E#
            #.#.#.#.#.#.#.#.#
            #.#.#.#...#...#.#
            #.#.#.#.###.#.#.#
            #...#.#.#.....#.#
            #.#.#.#.#.#####.#
            #.#...#.#.#.....#
            #.#.#####.#.###.#
            #.#.#.......#...#
            #.#.###.#####.###
            #.#.#...#.....#.#
            #.#.#.#####.###.#
            #.#.#.........#.#
            #.#.#.#########.#
            #S#.............#
            #################""": 64,
    }

    for i, (test, true) in enumerate(test_data_a.items()):
        result = solve_a(test)
        print(f"result {i}: {result}\n")
        assert result == true, f"{result} != {true}"

    result_a = solve_a(data)
    print(f"result a: {result_a}\n")
    submit(result_a, part="a", day=day, year=year)

    for i, (test, true) in enumerate(test_data_b.items()):
        result = solve_b(test)
        print(f"result {i}: {result}\n")
        assert result == true, f"{result} != {true}"

    result_b = solve_b(data)
    print(f"result b: {result_b}\n")
    submit(result_b, part="b", day=day, year=year)


def getNeighbors(grid, p):
    """
    p = (y, x, direction)
    """
    directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
    positions = []
    for d in directions:
        y = p[0]+d[0]
        x = p[1]+d[1]
        if (y, x) in grid:
            if d == p[2]:
                positions.append((y, x, d, 1))
            else:
                positions.append((y, x, d, 1001))
    return positions


def astar(grid, position, target) -> (int, list):
    start = position
    openSet = {start}
    cameFrom = {}
    gScore = {}
    gScore[start] = 0
    fScore = {}
    fScore[start] = 0

    while openSet:
        current = min(openSet, key=lambda a: fScore.get(a, sys.maxsize))
        if current[:2] == target:
            break
        openSet.remove(current)
        neighbors = getNeighbors(grid, current)
        for *neighbor, score in sorted(neighbors, key=lambda x: grid.get(x[3], sys.maxsize)):
            neighbor = tuple(neighbor)
            tentativeGScore = gScore[current] + score
            if (neighbor not in gScore) or (tentativeGScore < gScore[neighbor]):
                cameFrom[neighbor] = current
                gScore[neighbor] = tentativeGScore
                fScore[neighbor] = tentativeGScore
                openSet.add(neighbor)

    score = gScore[current]
    if current[:2] == target:
        path = [current[:2]]
        while current in cameFrom.keys():
            current = cameFrom[current]
            path = [current[:2]] + path
        return score, path
    return None, None


def floodastar(grid, position, target) -> (int, list):
    start = position
    openSet = {start}
    cameFrom = defaultdict(list)
    gScore = {}
    gScore[start] = 0
    fScore = {}
    fScore[start] = 0
    best = None
    tiles = set()

    while openSet:
        current = min(openSet, key=lambda a: fScore.get(a, sys.maxsize))
        if current[:2] == target:
            if gScore[current] == best or best is None:
                best = gScore[current]

        openSet.remove(current)
        neighbors = getNeighbors(grid, current)
        for *neighbor, score in sorted(neighbors, key=lambda x: grid.get(x[3], sys.maxsize)):
            neighbor = tuple(neighbor)
            tentativeGScore = gScore[current] + score
            if (not best or gScore[current] < best) and \
                    ((neighbor not in gScore) or (tentativeGScore == gScore[neighbor])):
                cameFrom[neighbor].append(current)
                gScore[neighbor] = tentativeGScore
                fScore[neighbor] = tentativeGScore
                openSet.add(neighbor)
            elif (not best or gScore[current] < best) and \
                    ((tentativeGScore < gScore[neighbor])):
                cameFrom[neighbor] = [current]
                gScore[neighbor] = tentativeGScore
                fScore[neighbor] = tentativeGScore
                openSet.add(neighbor)

    if best:
        todo = deque()
        for direction in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            todo.append((*target, direction))
        while todo:
            c = todo.popleft()
            tiles.add(tuple(c[:2]))
            if c in cameFrom:
                for d in cameFrom[c]:
                    todo.append(d)
    return tiles


def solve_a(data):
    grid = {}
    start = None
    end = None
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line.strip()):
            if c != "#":
                grid[(y, x)] = c
            if c == "S":
                start = (y, x, (0, 1))
            if c == "E":
                end = (y, x)

    score, path = astar(grid, start, end)
    return score


def solve_b(data):
    grid = {}
    start = None
    end = None
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line.strip()):
            if c != "#":
                grid[(y, x)] = c
            if c == "S":
                start = (y, x, (0, 1))
            if c == "E":
                end = (y, x)

    tiles = floodastar(grid, start, end)
    return len(tiles)


if __name__ == "__main__":
    main()
