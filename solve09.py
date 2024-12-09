from aocd import submit, get_data


def main():
    day = 9
    year = 2024
    data = get_data(day=day, year=year)

    test_data_a = {
            """2333133121414131402""": 1928,
    }
    test_data_b = {
            """2333133121414131402""": 2858,
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
    files = []
    n = 0
    isFile = True
    for c in data:
        c = int(c)
        if isFile:
            files += [n] * c
        else:
            files += ["."] * c
            n += 1
        isFile = not isFile

    i = 0
    while files:
        c = files.pop(0)
        if c != ".":
            res += i * int(c)
        else:
            while files:
                c = files.pop()
                if c != ".":
                    res += i * int(c)
                    break
                else:
                    continue
        i += 1

    for i, c in enumerate(files):
        if c == ".":
            break
        res += i * int(c)
    return res


def solve_b(data):
    res = 0
    files = []
    n = 0
    isFile = True
    for c in data:
        c = int(c)
        if isFile:
            files.append((n, c))
            n += 1
        else:
            if c:
                files.append((".", c))
        isFile = not isFile

    visited = set()
    i = len(files)-1
    while True:
        if i == 0:
            break
        c, n = files[i]

        if c == ".":
            i -= 1
            continue
        if c in visited:
            i -= 1
            continue
        for j in range(i):
            o, m = files[j]
            if o != ".":
                continue
            if m >= n:
                visited.add(c)
                files.pop(i)
                files.insert(i, (".", n))
                files.pop(j)
                if m > n:
                    files.insert(j, (o, m-n))
                    i += 1
                files.insert(j, (c, n))
                break
        i -= 1

    i = 0
    for c, n in files:
        for j in range(n):
            if c != ".":
                res += i * int(c)
            i += 1
    return res


if __name__ == "__main__":
    main()
