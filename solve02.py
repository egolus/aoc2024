from functools import reduce
from operator import mul
from aocd import submit, get_data


def main():
    day = 2
    year = 2024
    data = get_data(day=day, year=year)

    test_data_a = {
            """7 6 4 2 1
               1 2 7 8 9
               9 7 6 2 1
               1 3 2 4 5
               8 6 4 4 1
               1 3 6 7 9""": 2,
    }
    test_data_b = {
            """7 6 4 2 1
               1 2 7 8 9
               9 7 6 2 1
               1 3 2 4 5
               8 6 4 4 1
               1 3 6 7 9""": 4,
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
    lines = data.splitlines()
    for line in lines:
        safe = True
        inc = 0
        levels = line.split()
        x = int(levels[0])
        for y in levels[1:]:
            y = int(y)
            if y > x and inc < 0:
                safe = False
                break
            elif y < x and inc > 0:
                safe = False
                break
            if abs(y-x) < 1 or abs(y-x) > 3:
                safe = False
                break
            if y-x > 0:
                inc = 1
            else:
                inc = -1
            x = y
        if safe:
            res += 1
    return res


def solve_b(data):
    res = 0
    lines = data.splitlines()
    for line in lines:
        levels = line.split()
        if do(levels):
            res += 1
    return res

def do(levels, again=True):
    inc = 0
    x = int(levels[0])
    for pos, y in enumerate(levels[1:]):
        y = int(y)
        if y > x and inc < 0:
            if pos > 0 and again:
                if do(levels[:pos-1] + levels[pos:], False):
                    return True
            if again:
                if do(levels[:pos] + levels[pos+1:], False):
                    return True
                return do(levels[:pos+1] + levels[pos+2:], False)
            return False
        elif y < x and inc > 0:
            if pos > 0 and again:
                if do(levels[:pos-1] + levels[pos:], False):
                    return True
            if again:
                if do(levels[:pos] + levels[pos+1:], False):
                    return True
                return do(levels[:pos+1] + levels[pos+2:], False)
            return False
        if abs(y-x) < 1 or abs(y-x) > 3:
            if again:
                if do(levels[:pos] + levels[pos+1:], False):
                    return True
                return do(levels[:pos+1] + levels[pos+2:], False)
            return False
        if inc == 0:
            if y-x > 0:
                inc = 1
            else:
                inc = -1
        x = y
    return True


if __name__ == "__main__":
    main()
