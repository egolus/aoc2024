import sys
from aocd import submit, get_data


def main():
    day = 18
    year = 2024
    data = get_data(day=day, year=year)

    test_data_a = {
            """5,4
            4,2
            4,5
            3,0
            2,1
            6,3
            2,4
            1,5
            0,6
            3,3
            2,6
            5,1
            1,2
            5,5
            2,5
            6,5
            1,4
            0,4
            6,4
            1,1
            6,1
            1,0
            0,5
            1,6
            2,0""": 22,
    }
    test_data_b = {
            """5,4
            4,2
            4,5
            3,0
            2,1
            6,3
            2,4
            1,5
            0,6
            3,3
            2,6
            5,1
            1,2
            5,5
            2,5
            6,5
            1,4
            0,4
            6,4
            1,1
            6,1
            1,0
            0,5
            1,6
            2,0""": "6,1",

    }

    for i, (test, true) in enumerate(test_data_a.items()):
        result = solve_a(test, 6, 12)
        print(f"result {i}: {result}\n")
        assert result == true, f"{result} != {true}"

    result_a = solve_a(data)
    print(f"result a: {result_a}\n")
    submit(result_a, part="a", day=day, year=year)

    for i, (test, true) in enumerate(test_data_b.items()):
        result = solve_b(test, 6)
        print(f"result {i}: {result}\n")
        assert result == true, f"{result} != {true}"

    result_b = solve_b(data)
    print(f"result b: {result_b}\n")
    submit(result_b, part="b", day=day, year=year)


def getNeighbors(current, size):
    neighbors = []
    for y, x in (0, 1), (1, 0), (0, -1), (-1, 0):
        if (0 <= current[0] + y < size) and (0 <= (current[1] + x) < size):
            neighbors.append((current[0] + y, current[1] + x))
    return neighbors


def astar(grid, position, target, size, h):
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
        neighbors = getNeighbors(current, size)
        for neighbor in sorted(neighbors, key=h):
            if neighbor in grid:
                continue
            tentativeGscore = gScore[current] + 1
            if (neighbor not in gScore) or (tentativeGscore < gScore[neighbor]):
                cameFrom[neighbor] = current
                gScore[neighbor] = tentativeGscore
                fScore[neighbor] = tentativeGscore + h(neighbor)
                openSet.add(neighbor)

    if current == target:
        path = [current[:2]]
        while current in cameFrom.keys():
            current = cameFrom[current]
            path = [current] + path
        return path


def printGrid(grid, size, path=None):
    if path is None:
        path = []
    for y in range(size+1):
        for x in range(size+1):
            if (y, x) in path:
                print("O", end="")
            elif (y, x) in grid:
                print(hex(grid[(y, x)])[-1], end="")
            else:
                print(".", end="")
        print()


def solve_a(data, size=70, steps=1024):
    grid = {}
    i = 0
    for line in data.splitlines():
        x, y = [int(c) for c in line.split(",")]
        grid[(y, x)] = i
        i += 1
        if i == steps:
            break

    path = astar(
        grid, (0, 0), (size, size), size+1, lambda c: size-c[0]+size-c[1])
    return len(path)-1


def solve_b(data, size=70):
    grid = {}
    lines = data.splitlines()
    for i in range(len(lines)):
        line = lines[i]
        x, y = line.split(",")
        lines[i] = int(y), int(x)

    for i in range(len(lines)):
        grid[lines[i]] = i
        path = astar(
            grid, (0, 0), (size, size), size+1, lambda c: size-c[0]+size-c[1])
        if not path:
            return f"{lines[i][1]},{lines[i][0]}"


if __name__ == "__main__":
    main()
