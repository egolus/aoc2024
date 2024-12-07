from aocd import submit, get_data
from itertools import product


def main():
    day = 7
    year = 2024
    data = get_data(day=day, year=year)

    test_data_a = {
            """190: 10 19
            3267: 81 40 27
            83: 17 5
            156: 15 6
            7290: 6 8 6 15
            161011: 16 10 13
            192: 17 8 14
            21037: 9 7 18 13
            292: 11 6 16 20""": 3749,
    }
    test_data_b = {
            """190: 10 19
            3267: 81 40 27
            83: 17 5
            156: 15 6
            7290: 6 8 6 15
            161011: 16 10 13
            192: 17 8 14
            21037: 9 7 18 13
            292: 11 6 16 20""": 11387,
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
    lines = data.splitlines()
    for line in lines:
        res, ops = line.split(": ")
        res = int(res)
        ops = [int(op) for op in ops.split()]

        for _set in product(list("+*"), repeat=len(ops)-1):
            test = ops[0]
            for x,y in zip(_set, ops[1:]):
                if x == "+":
                    test += y
                else:
                    test *= y
            if test == res:
                sol += res
                break

    return sol


def solve_b(data):
    sol = 0
    lines = data.splitlines()
    for line in lines:
        res, ops = line.split(": ")
        res = int(res)
        ops = [int(op) for op in ops.split()]

        for _set in product(list("+*|"), repeat=len(ops)-1):
            test = ops[0]
            for x,y in zip(_set, ops[1:]):
                if x == "+":
                    test += y
                elif x == "*":
                    test *= y
                elif x == "|":
                    test = int(str(test) + str(y))
            if test == res:
                sol += res
                break

    return sol



if __name__ == "__main__":
    main()
