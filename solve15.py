from aocd import submit, get_data
from collections import defaultdict


def main():
    day = 15
    year = 2024
    data = get_data(day=day, year=year)

    test_data_a = {
            """########
            #..O.O.#
            ##@.O..#
            #...O..#
            #.#.O..#
            #...O..#
            #......#
            ########

            <^^>>>vv<v>>v<<
            """: 2028,
            """##########
            #..O..O.O#
            #......O.#
            #.OO..O.O#
            #..O@..O.#
            #O#..O...#
            #O..O..O.#
            #.OO.O.OO#
            #....O...#
            ##########

            <vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
            vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
            ><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
            <<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
            ^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
            ^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
            >^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
            <><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
            ^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
            v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
            """: 10092,
    }
    test_data_b = {
            """##########
            #..O..O.O#
            #......O.#
            #.OO..O.O#
            #..O@..O.#
            #O#..O...#
            #O..O..O.#
            #.OO.O.OO#
            #....O...#
            ##########

            <vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
            vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
            ><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
            <<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
            ^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
            ^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
            >^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
            <><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
            ^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
            v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
            """: 9021,
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


def printGrid(grid, maxy, maxx):
    for y in range(maxy):
        for x in range(maxx):
            if (y, x) in grid:
                print(grid[y, x], end="")
            else:
                print(" ", end="")
        print()


def move(grid, position, m) -> [tuple, bool]:
    moves = ["<", "^", ">", "v"]
    changes = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    if m not in moves:
        return False
    change = changes[moves.index(m)]
    if (position[0]+change[0], position[1]+change[1]) not in grid:
        grid[position[0]+change[0], position[1]+change[1]] = grid.pop(position)
        return (position[0]+change[0], position[1]+change[1])
    if grid[position[0]+change[0], position[1]+change[1]] == "#":
        return False
    if move(grid, (position[0]+change[0], position[1]+change[1]), m):
        grid[position[0]+change[0], position[1]+change[1]] = grid.pop(position)
        return (position[0]+change[0], position[1]+change[1])
    return False


def solve_a(data):
    ans = 0
    grid = {}
    G, M = data.split("\n\n")

    robot = None
    for y, line in enumerate(G.splitlines()):
        for x, c in enumerate(line.strip()):
            if c in ["#", "O", "@"]:
                grid[y, x] = c
                if c == "@":
                    robot = (y, x)
    maxy = y+1
    maxx = x+1

    for m in M.strip():
        if m == "\n":
            continue
        update = move(grid, robot, m)
        if update:
            robot = update

    for y in range(maxy):
        for x in range(maxx):
            if grid.get((y, x)) == "O":
                ans += 100*y+x

    return ans


def move_b(grid, position, m) -> [set, False]:
    moves = ["<", "^", ">", "v"]
    changes = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    if m not in moves:
        return False
    change = changes[moves.index(m)]
    if (position[0]+change[0], position[1]+change[1]) not in grid:
        return {((position[0]+change[0], position[1]+change[1]), grid[position])}
    if grid[position[0]+change[0], position[1]+change[1]] == "#":
        return False
    if m in ["<", ">"]:
        updates = move_b(grid, (position[0]+change[0], position[1]+change[1]), m)
        if updates:
            updates.add(
                ((position[0]+change[0], position[1]+change[1]), grid[position]))
            return updates
        return False
    else:
        if grid[position[0]+change[0], position[1]+change[1]] == "[":
            lup = move_b(grid, (position[0]+change[0], position[1]+change[1]), m)
            rup = move_b(grid, (position[0]+change[0], position[1]+1+change[1]), m)
            if lup and rup:
                updates = lup.union(rup)
                updates.add((
                    (position[0]+change[0], position[1]+change[1]),
                    grid[position]))
                return updates
            else:
                return False
        elif grid[position[0]+change[0], position[1]+change[1]] == "]":
            lup = move_b(grid, (position[0]+change[0], position[1]-1+change[1]), m)
            rup = move_b(grid, (position[0]+change[0], position[1]+change[1]), m)
            if lup and rup:
                updates = lup.union(rup)
                updates.add((
                    (position[0]+change[0], position[1]+change[1]),
                    grid[position]))
                return updates
            else:
                return False
    return False


def solve_b(data):
    moves = ["<", "^", ">", "v"]
    oldpositions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    ans = 0
    grid = {}
    G, M = data.split("\n\n")

    robot = None
    for y, line in enumerate(G.splitlines()):
        for x, c in enumerate(line.strip()):
            # if c in ["#", "O", "@"]:
            if c == "#":
                grid[y, x*2] = "#"
                grid[y, x*2+1] = "#"
            elif c == "O":
                grid[y, x*2] = "["
                grid[y, x*2+1] = "]"
            elif c == "@":
                grid[y, x*2] = "@"
                robot = (y, x*2)
    maxy = y+1
    maxx = x*2+1

    for m in M.strip():
        if m == "\n":
            continue
        updates = move_b(grid, robot, m)
        if updates:
            for (pos, _) in updates:
                oldpos = (pos[0]+oldpositions[moves.index(m)][0],
                          pos[1]+oldpositions[moves.index(m)][1])
                grid.pop(oldpos)
            for (pos, c) in updates:
                grid[pos] = c
                if c == "@":
                    robot = pos

    for y in range(maxy):
        for x in range(maxx):
            if grid.get((y, x)) == "[":
                ans += 100*y+x

    return ans



if __name__ == "__main__":
    main()
