from copy import copy
from collections import defaultdict
from aocd import submit, get_data


def main():
    day = 6
    year = 2024
    data = get_data(day=day, year=year)

    test_data_a = {
            """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...""": 41,
    }
    test_data_b = {
            """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...""": 6,
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


def solve_a(data):
    res = 0
    grid = set()
    visited = set()
    dirchange = {}
    dirnames   = ["^",    ">",   "v",   "<"]
    directions = [(-1,0), (0,1), (1,0), (0,-1)]

    pos = None
    direction = 0

    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            if c == "#":
                grid.add((y,x))
            elif c == "^":
                pos = (y,x)
                visited.add((y,x))

    maxx = x
    maxy = y

    while not ((pos[0] > maxy) or (pos[0] < 0) or (pos[1] > maxx) or (pos[1] < 0)):
        if (pos[0] + directions[direction][0], pos[1] + directions[direction][1]) in grid:
            dirchange[pos] = direction
            direction = (direction + 1) % len(directions)
        else:
            pos = (pos[0] + directions[direction][0], pos[1] + directions[direction][1])
            visited.add(pos)

    for y in range(maxy+1):
        for x in range(maxx+1):
            if (y,x) in grid:
                print("#", end="")
            elif (y,x) in dirchange:
                print(dirnames[dirchange[(y,x)]], end="")
            elif (y,x) in visited:
                print("X", end="")
            else:
                print(".", end="")
        print()

    return len(visited)-1


def solve(grid, directions, pos, direction, maxy, maxx, maxcount):
    grid = copy(grid)
    visited = set()
    directions = copy(directions)
    pos = copy(pos)
    direction = copy(direction)

    dirchange = defaultdict(list)

    while not ((pos[0] > maxy) or (pos[0] < 0) or (pos[1] > maxx) or (pos[1] < 0)):
        if (pos[0] + directions[direction][0], pos[1] + directions[direction][1]) in grid:
            if pos in dirchange and direction in dirchange[(pos)]:
                return (True, None)
            dirchange[pos].append(direction)
            direction = (direction + 1) % len(directions)
        else:
            pos = (pos[0] + directions[direction][0], pos[1] + directions[direction][1])
            visited.add(pos)
    return (False, visited)


def solve_b(data):
    res = 0
    grid = set()
    visited = set()
    directions = [(-1,0), (0,1), (1,0), (0,-1)]

    pos = None
    direction = 0

    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            if c == "#":
                grid.add((y,x))
            elif c == "^":
                pos = (y,x)
                visited.add((y,x))

    maxx = x
    maxy = y

    _, visited = solve(grid, directions, pos, direction, maxy, maxx, maxy*maxx)

    for y in range(maxy+1):
        for x in range(maxx+1):
            if (y,x) in visited and (y,x) != pos:
                grid.add((y,x))
                if solve(grid, directions, pos, direction, maxy, maxx, len(visited))[0]:
                    res += 1
                grid.remove((y,x))

    return res



if __name__ == "__main__":
    main()
