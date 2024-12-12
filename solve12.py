from collections import defaultdict
from aocd import submit, get_data
from pprint import pprint


def main():
    day = 12
    year = 2024
    data = get_data(day=day, year=year)

    test_data_a = {
        """AAAA
        BBCD
        BBCC
        EEEC""": 140,
        """OOOOO
        OXOXO
        OOOOO
        OXOXO
        OOOOO""": 772,
        """RRRRIICCFF
        RRRRIICCCF
        VVRRRCCFFF
        VVRCCCJFFF
        VVVVCJJCFE
        VVIVCCJJEE
        VVIIICJJEE
        MIIIIIJJEE
        MIIISIJEEE
        MMMISSJEEE""": 1930,
    }
    test_data_b = {
        """AAAA
        BBCD
        BBCC
        EEEC""": 80,
        """OOOOO
        OXOXO
        OOOOO
        OXOXO
        OOOOO""": 436,
        """EEEEE
        EXXXX
        EEEEE
        EXXXX
        EEEEE""": 236,
        """AAAAAA
        AAABBA
        AAABBA
        ABBAAA
        ABBAAA
        AAAAAA""": 368,
        """RRRRIICCFF
        RRRRIICCCF
        VVRRRCCFFF
        VVRCCCJFFF
        VVVVCJJCFE
        VVIVCCJJEE
        VVIIICJJEE
        MIIIIIJJEE
        MIIISIJEEE
        MMMISSJEEE""": 1206,
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
    grid = {}
    plots = set()
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line.strip()):
            if c != ".":
                grid[(y,x)] = c
                plots.add(c)

    maxy = y+1
    maxx = x+1

    regions = defaultdict(list)
    for plot in plots:
        while True:
            found=False
            for y in range(maxy):
                for x in range(maxx):
                    if grid.get((y,x)) == plot:
                        found = True
                        grid.pop((y,x))
                        break
                if found:
                    break
            if found:
                for r in regions[plot]:
                    if  (y-1,x) in r or (y,x-1) in r:
                        r.append((y,x))
                        break
                else:
                    regions[plot].append([(y,x)])
            else:
                break

    for plot in sorted(plots):
        for i in range(len(regions[plot])-1,0,-1):
            region = regions[plot][i]
            for j in range(i-1,-1,-1):
                other = regions[plot][j]
                if region == other:
                    continue
                merge = False
                for p in region:
                    for direction in [(0,1),(1,0),(-1,0),(0,-1)]:
                        if (direction[0]+p[0], direction[1]+p[1]) in other:
                            merge = True
                            break
                    if merge:
                        break
                if merge:
                    for p in region:
                        other.append(p)
                    regions[plot].pop(i)
                    break
        for region in regions[plot]:
            fence = []
            for point in region:
                for direction in [(0,1),(1,0),(-1,0),(0,-1)]:
                    if (direction[0]+point[0], direction[1]+point[1]) not in region:
                        fence.append((direction[0]+point[0], direction[1]+point[1]))
            res += len(region) * len(fence)

    return res


def solve_b(data):
    res = 0
    grid = {}
    plots = set()
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line.strip()):
            if c != ".":
                grid[(y,x)] = c
                plots.add(c)

    maxy = y+1
    maxx = x+1

    regions = defaultdict(list)
    for plot in plots:
        while True:
            found=False
            for y in range(maxy):
                for x in range(maxx):
                    if grid.get((y,x)) == plot:
                        found = True
                        grid.pop((y,x))
                        break
                if found:
                    break
            if found:
                for r in regions[plot]:
                    if  (y-1,x) in r or (y,x-1) in r:
                        r.append((y,x))
                        break
                else:
                    regions[plot].append([(y,x)])
            else:
                break

    for plot in sorted(plots):
        for i in range(len(regions[plot])-1,0,-1):
            region = regions[plot][i]
            for j in range(i-1,-1,-1):
                other = regions[plot][j]
                if region == other:
                    continue
                merge = False
                for p in region:
                    for direction in [(0,1),(1,0),(-1,0),(0,-1)]:
                        if (direction[0]+p[0], direction[1]+p[1]) in other:
                            merge = True
                            break
                    if merge:
                        break
                if merge:
                    for p in region:
                        other.append(p)
                    regions[plot].pop(i)
                    break
        for region in regions[plot]:
            fence = defaultdict(list)
            for point in region:
                for direction in [(0,1),(1,0),(-1,0),(0,-1)]:
                    if (direction[0]+point[0], direction[1]+point[1]) not in region:
                        fence[(direction[0]+point[0], direction[1]+point[1])].append(direction)
            for point in fence:
                for direction in fence[point]:
                    # right -> remove up/down
                    if direction == (0,1):

                        # up
                        move = 1
                        while True:
                            other = (point[0]-move,point[1])
                            if other in fence and direction in fence[other]:
                                fence[other].remove(direction)
                            else:
                                break
                            move += 1

                        # down
                        move = 1
                        while True:
                            other = (point[0]+move,point[1])
                            if other in fence and direction in fence[other]:
                                fence[other].remove(direction)
                            else:
                                break
                            move += 1

                    # left -> remove up/down
                    elif direction == (0,-1):

                        # up
                        move = 1
                        while True:
                            other = (point[0]-move,point[1])
                            if other in fence and direction in fence[other]:
                                fence[other].remove(direction)
                            else:
                                break
                            move += 1

                        # down
                        move = 1
                        while True:
                            other = (point[0]+move,point[1])
                            if other in fence and direction in fence[other]:
                                fence[other].remove(direction)
                            else:
                                break
                            move += 1

                    # top -> remove left/right
                    if direction == (-1,0):

                        # left
                        move = 1
                        while True:
                            other = (point[0],point[1]-move)
                            if other in fence and direction in fence[other]:
                                fence[other].remove(direction)
                            else:
                                break
                            move += 1

                        # down
                        move = 1
                        while True:
                            other = (point[0],point[1]+move)
                            if other in fence and direction in fence[other]:
                                fence[other].remove(direction)
                            else:
                                break
                            move += 1

                    # bottom -> remove left/right
                    elif direction == (1,0):

                        # left
                        move = 1
                        while True:
                            other = (point[0],point[1]-move)
                            if other in fence and direction in fence[other]:
                                fence[other].remove(direction)
                            else:
                                break
                            move += 1

                        # down
                        move = 1
                        while True:
                            other = (point[0],point[1]+move)
                            if other in fence and direction in fence[other]:
                                fence[other].remove(direction)
                            else:
                                break
                            move += 1
            res += len(region) * sum(len(x) for x in fence.values())

    return res


if __name__ == "__main__":
    main()
