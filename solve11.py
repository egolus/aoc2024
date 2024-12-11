import sys
import math
from collections import defaultdict
from aocd import submit, get_data

sys.setrecursionlimit(100_000)


def main():
    day = 11
    year = 2024
    data = get_data(day=day, year=year)

    test_data_a = {
            ("""0 1 10 99 999""",1): 7,
            ("""125 17""",6): 22,
            ("""125 17""",25): 55312,
    }
    test_data_b = {
            ("""0 1 10 99 999""",1): 7,
            ("""125 17""",6): 22,
            ("""125 17""",25): 55312,
    }

    for i, (test, true) in enumerate(test_data_a.items()):
        result = solve_a(*test)
        print(f"result {i}: {result}\n")
        assert result == true, f"{result} != {true}"

    result_a = solve_a(data)
    print(f"result a: {result_a}\n")
    submit(result_a, part="a", day=day, year=year)

    for i, (test, true) in enumerate(test_data_b.items()):
        result = solve_b(*test)
        print(f"result {i}: {result}\n")
        assert result == true, f"{result} != {true}"

    result_b = solve_b(data)
    print(f"result b: {result_b}\n")
    submit(result_b, part="b", day=day, year=year)


def solve_a(data, times=25):
    stones = []
    for s in data.split():
        stones.append(int(s))

    for i in range(times):
        for j in range(len(stones)-1, -1, -1):
            s = stones.pop(j)
            if s == 0:
                stones.insert(j,1)
            elif not (len(str(s)) % 2):
                s = str(s)
                s1 = s[:len(s)//2]
                s2 = s[len(s)//2:]
                stones.insert(j, int(s2))
                stones.insert(j, int(s1))
            else:
                stones.insert(j, s * 2024)

    return len(stones)


def solve_b(data, times=75):
    stones = defaultdict(int)
    for s in data.split():
        stones[int(s)] += 1

    for i in range(times):
        new = defaultdict(int)
        for k,v in stones.items():
            if k == 0:
                new[1] += v
            elif not (len(str(k)) % 2):
                s = str(k)
                s1 = s[:len(s)//2]
                s2 = s[len(s)//2:]
                new[int(s1)] += v
                new[int(s2)] += v
            else:
                new[k*2024] += v
        stones = new
    return sum(stones.values())


if __name__ == "__main__":
    main()
