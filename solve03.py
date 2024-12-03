from aocd import submit, get_data

import re


def main():
    day = 3
    year = 2024
    data = get_data(day=day, year=year)

    test_data_a = {
            """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))""": 161,
    }
    test_data_b = {
            """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))""": 48,
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
    r = r"mul\((\d+),(\d+)\)"

    for (x, y) in (re.findall(r, data)):
        sol += int(x) * int(y)
    return sol



def solve_b(data):
    sol = 0

    r = r"mul\((\d+),(\d+)\)"

    for part in data.split("do()"):
        part = part.split("don't()")[0]
        for (x, y) in (re.findall(r, part)):
            sol += int(x) * int(y)

    return sol


if __name__ == "__main__":
    main()
