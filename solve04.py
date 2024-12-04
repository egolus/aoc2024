from aocd import submit, get_data
from collections import defaultdict


def main():
    day = 4
    year = 2024
    data = get_data(day=day, year=year)

    test_data_a = {
            """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX""": 18,
    }
    test_data_b = {
            """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX""": 9,
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
    sol = 0
    grid = {}
    gridmap = set()

    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            grid[(y,x)] = c

    maxy = y
    maxx = x

    print(f"{maxx=}, {maxy=}")

    for y in range(maxy+1):
        for x in range(maxx+1):
            # vertical
            if y + 3 <= maxy:
                word = "".join([grid[(y+yy,x)] for yy in range(4)])
                if word == "XMAS" or word == "SAMX":
                    for yy in range(4):
                        gridmap.add((y+yy,x))
                    sol += 1

            # horizontal
            if x + 3 <= maxx:
                word = "".join([grid[(y,x+xx)] for xx in range(4)])
                if word == "XMAS" or word == "SAMX":
                    for xx in range(4):
                        gridmap.add((y,x+xx))
                    sol += 1

            # diagonal left
            if x - 3 >= 0 and y + 3 <= maxy:
                word = "".join([grid[(y+xx,x-xx)] for xx in range(4)])
                if word == "XMAS" or word == "SAMX":
                    for xx in range(4):
                        gridmap.add((y+xx,x-xx))
                    sol += 1

            # diagonal right
            if x + 3 <= maxx and y + 3 <= maxy:
                word = "".join([grid[(y+xx,x+xx)] for xx in range(4)])
                if word == "XMAS" or word == "SAMX":
                    for xx in range(4):
                        gridmap.add((y+xx,x+xx))
                    sol += 1

    for y in range(maxy+1):
        for x in range(maxx+1):
            if (y,x) in gridmap:
                print(grid[(y,x)], end="")
            else:
                print(".", end="")
        print()

    return sol


    return sol


def solve_b(data):
    sol = 0
    grid = {}
    gridmap = set()

    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            grid[(y,x)] = c

    maxy = y
    maxx = x

    print(f"{maxx=}, {maxy=}")

    for y in range(maxy+1):
        for x in range(maxx+1):
            if x + 2 <= maxx and y + 2 <= maxy:
                word1 = "".join([grid[(y+xx,x+xx)] for xx in range(3)])
                word2 = "".join([grid[(y+xx,x+2-xx)] for xx in range(3)])
                if      (word1 == "MAS" or word1 == "SAM") and \
                        (word2 == "MAS" or word2 == "SAM"):
                    sol += 1
    return sol


if __name__ == "__main__":
    main()
