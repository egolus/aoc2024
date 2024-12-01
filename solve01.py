from aocd import submit, get_data


def main():
    day = 1
    year = 2024
    data = get_data(day=day, year=year)

    test_data_a = {
        """3   4
           4   3
           2   5
           1   3
           3   9
           3   3""": 11,
    }
    test_data_b = {
        """3   4
           4   3
           2   5
           1   3
           3   9
           3   3""": 31,
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
    aa = []
    bb = []
    for line in data.splitlines():
        a, b = line.strip().split()
        aa.append(int(a))
        bb.append(int(b))
    aa = sorted(aa)
    bb = sorted(bb)
    diffs = [abs(a-b) for a, b in zip(aa, bb)]
    return sum(diffs)


def solve_b(data):
    res = 0
    aa = []
    bb = []
    for line in data.splitlines():
        a, b = line.strip().split()
        aa.append(int(a))
        bb.append(int(b))
    for a in aa:
        res += sum(b for b in bb if b == a)
    return res


if __name__ == "__main__":
    main()
