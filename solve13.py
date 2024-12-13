import sys
import math
from aocd import submit, get_data
from collections import Counter
from copy import copy


def main():
    day = 13
    year = 2024
    data = get_data(day=day, year=year)

    test_data_a = {
            """Button A: X+94, Y+34
            Button B: X+22, Y+67
            Prize: X=8400, Y=5400

            Button A: X+26, Y+66
            Button B: X+67, Y+21
            Prize: X=12748, Y=12176

            Button A: X+17, Y+86
            Button B: X+84, Y+37
            Prize: X=7870, Y=6450

            Button A: X+69, Y+23
            Button B: X+27, Y+71
            Prize: X=18641, Y=10279""": 480,
    }
    test_data_b = {
            """Button A: X+94, Y+34
            Button B: X+22, Y+67
            Prize: X=8400, Y=5400

            Button A: X+26, Y+66
            Button B: X+67, Y+21
            Prize: X=12748, Y=12176

            Button A: X+17, Y+86
            Button B: X+84, Y+37
            Prize: X=7870, Y=6450

            Button A: X+69, Y+23
            Button B: X+27, Y+71
            Prize: X=18641, Y=10279""": 875318608908,
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
    for group in data.split("\n\n"):
        mintokens = sys.maxsize
        lines = group.splitlines()
        A = [int(t.split("+")[1]) for t in lines[0].split(":")[1].split(", ")]
        B = [int(t.split("+")[1]) for t in lines[1].split(":")[1].split(", ")]
        prize = [int(t.split("=")[1])
                 for t in lines[2].split(":")[1].split(", ")]

        for i in range(100):
            # print(i)
            x = A[0] * i
            y = A[1] * i
            if (((prize[0]-x) % B[0] == 0) and
                    ((prize[1]-y) % B[1] == 0)):
                if ((prize[0]-x)//B[0] == (prize[1]-y)//B[1]):
                    mintokens = min(mintokens, i*3 + (prize[1]-y)//B[1])
        if mintokens < sys.maxsize:
            ans += mintokens
    return ans


def insert(A, B, prize):
    # A[0] , B[0], prize[0]
    # A[1] , B[1], prize[1]

    # B[0] * A[1] / fac - B[1] * A[0] / fac = prize[0] * A[1] / fac - prize[1] * A[0] / fac
    # b * (B[0] * A[1] - B[1] * A[0]) = prize[0] * A[1] - prize[1] * A[0]
    b = (prize[0] * A[1] - prize[1] * A[0]) / (B[0] * A[1] - B[1] * A[0])

    # A[0] x + B[0] y = prize[0]
    # A[0] x + B[0] b = prize[0]
    # A[0] x = prize[0] - B[0] b
    # x = (prize[0] - B[0] * b) / A[0]
    a = (prize[0] - B[0] * b) / A[0]
    return (a, b)


def solve_b(data):
    ans = 0
    for group in data.split("\n\n"):
        lines = group.splitlines()
        A = [int(t.split("+")[1]) for t in lines[0].split(":")[1].split(", ")]
        B = [int(t.split("+")[1]) for t in lines[1].split(":")[1].split(", ")]
        prize = [int(t.split("=")[1])
                 for t in lines[2].split(":")[1].split(", ")]
        prize = [p + 10000000000000 for p in prize]

        a, b = insert(A, B, prize)
        if (a.is_integer() and b.is_integer()):
            ans += int(a)*3 + int(b)

    return ans

if __name__ == "__main__":
    main()
