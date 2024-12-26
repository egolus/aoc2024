from aocd import submit, get_data


def main():
    day = 25
    year = 2024
    data = get_data(day=day, year=year)

    test_data_a = {
            """#####
            .####
            .####
            .####
            .#.#.
            .#...
            .....

            #####
            ##.##
            .#.##
            ...##
            ...#.
            ...#.
            .....

            .....
            #....
            #....
            #...#
            #.#.#
            #.###
            #####

            .....
            .....
            #.#..
            ###..
            ###.#
            ###.#
            #####

            .....
            .....
            .....
            #....
            #.#..
            #.#.#
            #####""": 3,
    }
    test_data_b = {
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
    ans = 0
    keys = []
    locks = []

    for item in data.split("\n\n"):
        lines = [it.strip() for it in item.splitlines()]
        sy = len(lines)
        sx = len(lines[0])
        pins = []
        for x in range(sx):
            pins.append(sum(lines[y][x] == "#" for y in range(sy)))
        if lines[0][0] == "#":
            keys.append(tuple(pins))
        else:
            locks.append(tuple(pins))

    for key in keys:
        for lock in locks:
            for pk, pl in zip(key, lock):
                if pk+pl > 7:
                    break
            else:
                ans += 1

    return ans


def solve_b(data):
    pass


if __name__ == "__main__":
    main()
