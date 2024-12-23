from aocd import submit, get_data
import sys
from collections import defaultdict
from copy import copy
from pprint import pprint

sys.setrecursionlimit(10_000)


def main():

    day = 23
    year = 2024
    data = get_data(day=day, year=year)

    test_data_a = {
            """kh-tc
            qp-kh
            de-cg
            ka-co
            yn-aq
            qp-ub
            cg-tb
            vc-aq
            tb-ka
            wh-tc
            yn-cg
            kh-ub
            ta-co
            de-co
            tc-td
            tb-wq
            wh-td
            ta-ka
            td-qp
            aq-cg
            wq-ub
            ub-vc
            de-ta
            wq-aq
            wq-vc
            wh-yn
            ka-de
            kh-ta
            co-tc
            wh-qp
            tb-vc
            td-yn""": 7
    }
    test_data_b = {
            """kh-tc
            qp-kh
            de-cg
            ka-co
            yn-aq
            qp-ub
            cg-tb
            vc-aq
            tb-ka
            wh-tc
            yn-cg
            kh-ub
            ta-co
            de-co
            tc-td
            tb-wq
            wh-td
            ta-ka
            td-qp
            aq-cg
            wq-ub
            ub-vc
            de-ta
            wq-aq
            wq-vc
            wh-yn
            ka-de
            kh-ta
            co-tc
            wh-qp
            tb-vc
            td-yn""": "co,de,ka,ta"

    }
    # for i, (test, true) in enumerate(test_data_a.items()):
        # result = solve_a(test)
        # print(f"result {i}: {result}\n")
        # assert result == true, f"{result} != {true}"

    # result_a = solve_a(data)
    # print(f"result a: {result_a}\n")
    # submit(result_a, part="a", day=day, year=year)

    for i, (test, true) in enumerate(test_data_b.items()):
        result = solve_b(test)
        print(f"result {i}: {result}\n")
        assert result == true, f"{result} != {true}"

    result_b = solve_b(data)
    print(f"result b: {result_b}\n")
    submit(result_b, part="b", day=day, year=year)


def solve_a(data):
    pcs = defaultdict(list)
    conn = set()

    for line in data.splitlines():
        p1, p2 = line.strip().split("-")
        pcs[p1].append(p2)
        pcs[p2].append(p1)

    pprint(pcs)
    for p in pcs:
        for i, other in enumerate(pcs[p]):
            for j, o2 in enumerate(pcs[p][i:]):
                if o2 in pcs[other]:
                    conn.add(tuple(sorted((p, other, o2))))

    return len(list(c for c in conn if any(cc.startswith("t") for cc in c)))


def getlst(pcs, tocheck, lst):
    # print(f"getlst, {tocheck}, {lst}")
    # input()
    longest = lst
    if len(tocheck) == 1:
        if all(pp in pcs[tocheck[0]] for pp in lst):
            return lst + [tocheck[0]]
        return lst
    for i, p in enumerate(tocheck):
        for j, o in enumerate(tocheck[i+1:]):
            if all(pp in pcs[o] for pp in lst + [p]):
                new = getlst(pcs, tocheck[i+j+1:], lst + [p])
                if len(new) > len(longest):
                    longest = new
    return longest


def solve_b(data):
    pcs = defaultdict(list)

    for line in data.splitlines():
        p1, p2 = line.strip().split("-")
        pcs[p1].append(p2)
        pcs[p2].append(p1)

    pprint(pcs)

    longest = []
    for p in pcs:
        new = getlst(pcs, pcs[p], [p])
        if len(new) > len(longest):
            longest = new

    print(sorted(longest))
    return ",".join(sorted(longest))


if __name__ == "__main__":
    main()
