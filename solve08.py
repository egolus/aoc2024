from aocd import submit, get_data
from collections import defaultdict


def main():
    day = 8
    year = 2024
    data = get_data(day=day, year=year)

    test_data_a = {
            """..........
            ..........
            ..........
            ....a.....
            ..........
            .....a....
            ..........
            ..........
            ..........
            ..........""": 2,
            """............
            ........0...
            .....0......
            .......0....
            ....0.......
            ......A.....
            ............
            ............
            ........A...
            .........A..
            ............
            ............""": 14,
    }
    test_data_b = {
            """T....#....
            ...T......
            .T....#...
            .........#
            ..#.......
            ..........
            ...#......
            ..........
            ....#.....
            ..........""": 9,
            """##....#....#
            .#.#....0...
            ..#.#0....#.
            ..##...0....
            ....0....#..
            .#...#A....#
            ...#..#.....
            #....#.#....
            ..#.....A...
            ....#....A..
            .#........#.
            ...#......##""": 34,
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
    grid = defaultdict(set)
    nodes = set()
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line.strip()):
            if c != ".":
                grid[c].add((y,x))
    maxy = y
    maxx = x
    for c in grid:
        antennas = list(grid[c])
        for i in antennas[:-1]:
            for j in antennas[1:]:
                yy = (i[0]-j[0])
                xx = (i[1]-j[1])
                node = (i[0]+yy,i[1]+xx)
                if node != i and node != j:
                    nodes.add(node)
                node = (j[0]-yy,j[1]-xx)
                if node != i and node != j:
                    nodes.add(node)

    return len(list(n for n in nodes if 0<=n[0]<=maxy and 0<=n[1]<=maxx))


def solve_b(data):
    sol = 0
    grid = defaultdict(set)
    nodes = set()
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line.strip()):
            if c != "." and c != "#":
                grid[c].add((y,x))
    maxy = y
    maxx = x
    for c in grid:
        antennas = list(grid[c])
        for i in antennas:
            nodes.add(i)
            for j in antennas:
                if i == j:
                    continue
                yy = (i[0]-j[0])
                xx = (i[1]-j[1])
                n = [i[0]+yy,i[1]+xx]
                while 0<=n[0]<=maxy and 0<=n[1]<=maxx:
                    nodes.add(tuple(n))
                    n[0] += yy
                    n[1] += xx

                n = [j[0]-yy,j[1]-xx]
                while 0<=n[0]<=maxy and 0<=n[1]<=maxx:
                    nodes.add(tuple(n))
                    n[0] -= yy
                    n[1] -= xx

    return len(list(n for n in nodes if 0<=n[0]<=maxy and 0<=n[1]<=maxx))


if __name__ == "__main__":
    main()
