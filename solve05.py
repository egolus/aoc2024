from sys import maxsize
from aocd import submit, get_data


def main():
    day = 5
    year = 2024
    data = get_data(day=day, year=year)

    test_data_a = {
            """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47""": 143,
    }
    test_data_b = {
            """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47""": 123,
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
    sol = []

    sections = data.split("\n\n")
    ordering = {}
    for x in sections[0].splitlines():
        a, b = x.split("|")
        if a in ordering:
            ordering[a].append(b)
        else:
            ordering[a] = [b]

    updates = [tuple(x.split(",")) for x in sections[1].splitlines()]

    for update in updates:
        ordered = True
        for i, x in enumerate(update):
            if x in ordering:
                for y in update[i+1:]:
                    if not y in ordering[x]:
                        ordered = False
            else:
                for y in update[i+1:]:
                    for xx, yy in ordering.items():
                        if y == xx and x in yy:
                            ordered = False
        if ordered:
            sol.append(update[len(update)//2])
        else:
            pass

    return sum(int(x) for x in sol)


def solve_b(data):
    sol = []

    sections = data.split("\n\n")
    ordering = {}
    for x in sections[0].splitlines():
        a, b = x.split("|")
        if a in ordering:
            ordering[a].append(b)
        else:
            ordering[a] = [b]

    updates = [x.split(",") for x in sections[1].splitlines()]

    for update in updates:
        new = []
        ordered = True
        for i, x in enumerate(update):
            if x in ordering:
                for y in update[i+1:]:
                    if not y in ordering[x]:
                        ordered = False
                        break
            else:
                for y in update[i+1:]:
                    for xx, yy in ordering.items():
                        if y == xx and x in yy:
                            ordered = False
        if ordered:
            pass
        else:
            while update:
                for i, x in enumerate(update):
                    if x in ordering:
                        for y in update:
                            if y == x:
                                pass
                            elif y not in ordering[x]:
                                break
                            elif y in ordering and x in ordering[y]:
                                break
                        else:
                            update.pop(i)
                            new.append(x)
                            break
                else:
                    new.append(update.pop(0))
            sol.append(new[len(new)//2])
    return sum(int(x) for x in sol)



if __name__ == "__main__":
    main()
