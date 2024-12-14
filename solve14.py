from collections import defaultdict
from aocd import submit, get_data

def main():
    day = 14
    year = 2024
    data = get_data(day=day, year=year)

    test_data_a = {
            """p=0,4 v=3,-3
            p=6,3 v=-1,-3
            p=10,3 v=-1,2
            p=2,0 v=2,-1
            p=0,0 v=1,3
            p=3,0 v=-2,-2
            p=7,6 v=-1,-3
            p=3,0 v=-1,-2
            p=9,3 v=2,3
            p=7,3 v=-1,2
            p=2,4 v=2,-3
            p=9,5 v=-3,-3""": 12,
    }
    test_data_b = {
    }

    for i, (test, true) in enumerate(test_data_a.items()):
        result = solve_a(test, (11, 7))
        print(f"result {i}: {result}\n")
        assert result == true, f"{result} != {true}"

    result_a = solve_a(data)
    print(f"result a: {result_a}\n")
    submit(result_a, part="a", day=day, year=year)

    for i, (test, true) in enumerate(test_data_b.items()):
        result = solve_b(test, (11, 7))
        print(f"result {i}: {result}\n")
        assert result == true, f"{result} != {true}"

    result_b = solve_b(data)
    print(f"result b: {result_b}\n")
    submit(result_b, part="b", day=day, year=year)


def solve_a(data, space=None):
    if space is None:
        space = (101, 103)

    res = 1
    robots = []

    for line in data.splitlines():
        p = [int(x) for x in line.split()[0].split("=")[1].split(",")]
        v = [int(x) for x in line.split()[1].split("=")[1].split(",")]
        robots.append((p, v))

    for i in range(100):
        for r, robot in enumerate(robots):
            p, v = robot
            p[0] = ((p[0] + v[0]) % space[0])
            p[1] = ((p[1] + v[1]) % space[1])

    quads = {0: 0, 1: 0, 2: 0, 3: 0}
    for robot in sorted(robots):
        if ((0 <= robot[0][0] < (space[0] // 2))
                and
                (0 <= robot[0][1] < ((space[1] // 2)))):
            quads[0] += 1
        if (((space[0] // 2 + 1) <= robot[0][0] < space[0])
                and
                (0 <= robot[0][1] < ((space[1] // 2)))):
            quads[1] += 1
        if ((0 <= robot[0][0] < (space[0] // 2))
                and
                (((space[1] // 2 + 1)) <= robot[0][1] < space[1])):
            quads[2] += 1
        if (((space[0] // 2 + 1) <= robot[0][0] < space[0])
                and
                (((space[1] // 2 + 1)) <= robot[0][1] < space[1])):
            quads[3] += 1

    for quad in quads.values():
        res *= quad

    return res


def solve_b(data, space=None):
    if space is None:
        space = (101, 103)

    robots = []

    for line in data.splitlines():
        p = [int(x) for x in line.split()[0].split("=")[1].split(",")]
        v = [int(x) for x in line.split()[1].split("=")[1].split(",")]
        robots.append((p, v))

    for i in range(8260):
        grid = set()
        for r, robot in enumerate(robots):
            p, v = robot
            p[0] = ((p[0] + v[0]) % space[0])
            p[1] = ((p[1] + v[1]) % space[1])
            grid.add((p[0], p[1]))

        if all((38, 30+j) in grid for j in range(29)):
            return i+1


if __name__ == "__main__":
    main()
