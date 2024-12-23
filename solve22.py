from collections import defaultdict
from aocd import submit, get_data
from pprint import pprint


def main():
    day = 22
    year = 2024
    data = get_data(day=day, year=year)

    test_data_a = {
            ("""123""", 10): 5908254,
            ("""1
            10
            100
            2024""",): 37327623,
    }
    test_data_b = {
            ("""123""", 10): 6,
            ("""1
            2
            3
            2024""",): 23,
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


def solve_a(data, times=2000):
    ans = 0
    for line in data.splitlines():
        line = int(line)

        s = line
        for i in range(times):
            # multiply
            r = s * 64
            # mix
            s = s ^ r
            # prune
            s %= 16777216

            # divide
            r = s // 32
            # mix
            s = s ^ r
            # prune
            s %= 16777216

            # multiply
            r = s * 2048
            # mix 
            s = s ^ r
            # prune
            s %= 16777216

        print(f"{line}: {s}")
        ans += s
    return ans


def solve_b(data, times=2000):
    occs = defaultdict(dict)
    seqs = set()
    for line in data.splitlines():
        line = int(line)
        s = line

        old = []
        for i in range(times):
            old.append(s % 10)
            seq = [old[j] - old[j-1] for j in range(1, len(old))]
            seq = tuple(seq)
            if len(old) > 4:
                old.pop(0)
                if seq not in occs[line]:
                    occs[line][seq] = s % 10
                    seqs.add(seq)

            s = (s ^ s * 64) % 16777216
            s = (s ^ s // 32) % 16777216
            s = s ^ s * 2048 % 16777216

            # print(old % 10, s % 10, (s % 10)-(old % 10))

    ans = 0
    for seq in seqs:
        ans = max(ans, sum(v.get(seq, 0) for v in occs.values()))

    return ans


if __name__ == "__main__":
    main()
