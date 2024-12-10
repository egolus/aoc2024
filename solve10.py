from aocd import submit, get_data
from collections import Counter


def main():
    day = 10
    year = 2024
    data = get_data(day=day, year=year)

    test_data_a = {
            """0123
            1234
            8765
            9876""": 1,
            """89010123
            78121874
            87430965
            96549874
            45678903
            32019012
            01329801
            10456732""": 36,
    }
    test_data_b = {
            """89010123
            78121874
            87430965
            96549874
            45678903
            32019012
            01329801
            10456732""": 81,
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


def walk(grid, pos, maxy, maxx, found=None, seen=None):
    if found == None:
        found = set()
    if seen == None:
        seen = set()

    seen.add(pos)
    for direction in [(-1,0), (0,1), (1,0), (0,-1)]:
        if (pos[0]+direction[0], pos[1]+direction[1]) in seen:
            continue
        if not ((-1 < (pos[0]+direction[0]) < maxy) and (-1 < (pos[1]+direction[1]) < maxx)):
            continue
        if grid[(pos[0]+direction[0], pos[1]+direction[1])] == grid[pos] + 1:
            if grid[(pos[0]+direction[0], pos[1]+direction[1])] == 9:
                if (pos[0]+direction[0], pos[1]+direction[1]) not in found:
                    found.add((pos[0]+direction[0], pos[1]+direction[1]))
            ifound, iseen = walk(
                                grid,
                                (pos[0]+direction[0], pos[1]+direction[1]),
                                maxy, maxx, found, seen)
            found = found.union(ifound)
            seen = seen.union(iseen)
    return (found, seen)


def solve_a(data):
    res = 0
    grid = {}

    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line.strip()):
            grid[(y,x)] = int(c)
    maxy = y + 1
    maxx = x + 1

    for pos, height in grid.items():
        if height == 0:
            found, _ = walk(grid, pos, maxy, maxx)
            res += len(found)
    return res


def walk_b(grid, pos, path, maxy, maxx, paths=None):
    if paths == None:
        paths = set()

    for direction in [(-1,0), (0,1), (1,0), (0,-1)]:
        if not ((-1 < (pos[0]+direction[0]) < maxy) and (-1 < (pos[1]+direction[1]) < maxx)):
            continue
        if grid[(pos[0]+direction[0], pos[1]+direction[1])] == grid[pos] + 1:
            path.append(pos)
            if grid[(pos[0]+direction[0], pos[1]+direction[1])] == 9:
                paths.add(tuple(path))
            ipahts = walk_b(
                        grid,
                        (pos[0]+direction[0], pos[1]+direction[1]),
                        path,
                        maxy, maxx, paths)
            if ipahts:
                paths.union(ipahts)
    return paths


def solve_b(data):
    res = 0
    grid = {}

    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line.strip()):
            grid[(y,x)] = int(c)
    maxy = y + 1
    maxx = x + 1

    for pos, height in grid.items():
        if height == 0:
            paths = walk_b(grid, pos, [], maxy, maxx)
            res += len(paths)
    return res


if __name__ == "__main__":
    main()


