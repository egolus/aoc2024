import sys
from aocd import submit, get_data


def main():
    day = 20
    year = 2024
    data = get_data(day=day, year=year)

    test_data_a = {
            ("""###############
            #...#...#.....#
            #.#.#.#.#.###.#
            #S#...#.#.#...#
            #######.#.#.###
            #######.#.#...#
            #######.#.###.#
            ###..E#...#...#
            ###.#######.###
            #...###...#...#
            #.#####.#.###.#
            #.#...#.#.#...#
            #.#.#.#.#.#.###
            #...#...#...###
            ###############""", 20): 5,
    }
    test_data_b = {
            ("""###############
            #...#...#.....#
            #.#.#.#.#.###.#
            #S#...#.#.#...#
            #######.#.#.###
            #######.#.#...#
            #######.#.###.#
            ###..E#...#...#
            ###.#######.###
            #...###...#...#
            #.#####.#.###.#
            #.#...#.#.#...#
            #.#.#.#.#.#.###
            #...#...#...###
            ###############""", 50): 32+31+29+39+25+23+20+19+12+14+12+22+4+3,
    }

    # for i, (test, true) in enumerate(test_data_a.items()):
        # result = solve_a(*test)
        # print(f"result {i}: {result}\n")
        # assert result == true, f"{result} != {true}"

    # result_a = solve_a(data)
    # print(f"result a: {result_a}\n")
    # submit(result_a, part="a", day=day, year=year)

    for i, (test, true) in enumerate(test_data_b.items()):
        result = solve_b(*test)
        print(f"result {i}: {result}\n")
        assert result == true, f"{result} != {true}"

    result_b = solve_b(data)
    print(f"result b: {result_b}\n")
    submit(result_b, part="b", day=day, year=year)


def getNeighbors(grid, position):
    return [(d[0]+position[0], d[1]+position[1])
            for d in ((0, 1), (1, 0), (0, -1), (-1, 0))
            if grid.get((d[0]+position[0], d[1]+position[1]), None) in (".", "E")]


def astar(grid, position, target, h):
    """
    a* from position to target

    neighbor = (y, x)
    """
    start = position
    openSet = {start}
    cameFrom = {}
    gScore = {}
    gScore[start] = 0
    fScore = {}
    fScore[start] = h(start)

    while openSet:
        current = min(openSet, key=lambda a: fScore.get(a, sys.maxsize))
        if current == target:
            break
        openSet.remove(current)
        neighbors = getNeighbors(grid, current)
        for neighbor in sorted(neighbors, key=h):
            tentativeGScore = gScore[current] + 1
            if (neighbor not in gScore) or (tentativeGScore < gScore[neighbor]):
                cameFrom[neighbor] = current
                gScore[neighbor] = tentativeGScore
                fScore[neighbor] = tentativeGScore + h(neighbor)
                openSet.add(neighbor)

    # pprint(cameFrom)
    if current == target:
        path = [current]
        while current in cameFrom.keys():
            current = cameFrom[current]
            path = [current] + path
        path.pop(0)
        return path


def printGrid(grid, path, maxy, maxx):
    for y in range(maxy):
        for x in range(maxx):
            if (y, x) in path:
                print(".", end="")
            elif (y, x) in grid:
                print(grid[(y, x)], end="")
        print()


def solve_a(data, minsave=100):
    ans = 0
    grid = {}
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line.strip()):
            grid[(y, x)] = c
            if c == "S":
                start = (y, x)
            elif c == "E":
                end = (y, x)
    maxy = y+1
    maxx = x+1
    base = astar(grid, start, end, lambda p: abs(p[0]-end[0])+abs(p[1]-end[1]))
    printGrid(grid, base, maxy, maxx)
    print("base:", len(base))
    input()

    for y in range(1, maxy-1):
        print(f"{y=}", end="\r")
        for x in range(1, maxx-1):
            ngrid = grid.copy()
            if grid.get((y, x), None) == "#":
                ngrid[(y, x)] = "."
                after = astar(ngrid, start, end,
                              lambda p: abs(p[0]-end[0])+abs(p[1]-end[1]))
                if len(base) - len(after) >= minsave:
                    # printGrid(grid, after, maxy, maxx)
                    # input()
                    ans += 1

    return ans


def solve_b(data, minsave=100):
    ans = 0
    grid = {}
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line.strip()):
            grid[(y, x)] = c
            if c == "S":
                start = (y, x)
            elif c == "E":
                end = (y, x)
    maxy = y+1
    maxx = x+1
    base = astar(grid, start, end, lambda p: abs(p[0]-end[0])+abs(p[1]-end[1]))
    base = [start]+base
    printGrid(grid, base, maxy, maxx)
    print("base:", len(base))

    for i, s in enumerate(base):
        for j, t in enumerate(base[i+minsave:], start=1):
            moves = abs(s[0]-t[0]) + abs(s[1]-t[1])
            if moves <= 20 and j-moves > 0:
                ans += 1
    return ans


if __name__ == "__main__":
    main()
