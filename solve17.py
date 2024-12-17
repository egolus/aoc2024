from aocd import submit, get_data
import sys


def main():
    day = 17
    year = 2024
    data = get_data(day=day, year=year)

    test_data_a = {
            """Register C: 9

            Program: 2,6""": "",
            """Register A: 10

            Program: 5,0,5,1,5,4""": "0,1,2",
            """Register A: 2024

            Program: 0,1,5,4,3,0""": "4,2,5,6,7,7,7,7,3,1,0",
            """Register B: 29

            Program: 1,7""": "",
            """Register B: 2024
            Register C: 43690

            Program: 4,0""": "",

            """Register A: 729
            Register B: 0
            Register C: 0

            Program: 0,1,5,4,3,0""": "4,6,3,5,6,3,5,2,1,0",
    }
    test_data_b = {
            """Register A: 2024
            Register B: 0
            Register C: 0

            Program: 0,3,5,4,3,0""": 117440,
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


def runOp(registers, opcode, operand, pointer, out) -> (dict, int, list):
    codenames = ["adv", "bxl", "bst", "jnz", "bxc", "out", "bdv", "cdv"]
    # assert operand != 7
    coperand = operand
    if operand == 4:
        coperand = registers["A"]
    if operand == 5:
        coperand = registers["B"]
    if operand == 6:
        coperand = registers["C"]

    # print(f"{opcode=}, {operand=} - {codenames[opcode]} {operand=}")

    if opcode == 0:
        # adv
        registers["A"] = registers["A"] // 2**coperand
        # print(f"{registers['A']=}")
    if opcode == 1:
        # bxl
        registers["B"] = registers["B"] ^ operand
        # print(f"{registers['B']=}")
    if opcode == 2:
        # bst
        registers["B"] = coperand % 8
        # print(f"{registers['B']=}")
    if opcode == 3:
        # jnz
        if registers["A"] != 0:
            pointer = operand - 2
            # print(f"{pointer+2=}")
    if opcode == 4:
        # bxc
        registers["B"] = registers["B"] ^ registers["C"]
        # print(f"{registers['B']=}")
    if opcode == 5:
        # out
        out.append(coperand % 8)
        # print(f"{out}")
    if opcode == 6:
        # bdv
        registers["B"] = registers["A"] // 2**coperand
        # print(f"{registers['B']=}")
    if opcode == 7:
        # cdv
        registers["C"] = registers["A"] // 2**coperand
        # print(f"{registers['C']=}")

    return registers, pointer, out


def solve_a(data):
    out = []
    regs, prog = data.split("\n\n")
    registers = {"A": 0, "B": 0, "C": 0}
    for line in regs.splitlines():
        k, v = line.split(":")
        registers[k.split()[1]] = int(v)

    # print(registers)

    program = [int(p) for p in prog.split(": ")[1].split(",")]
    # print(program)
    pointer = 0
    while pointer < len(program):
        registers, pointer, out = runOp(
            registers, program[pointer], program[pointer+1], pointer, out)
        pointer += 2
        # print(f"{registers=} {pointer=}")

    return ",".join(str(o) for o in out)


def solve_b(data):
    out = []
    regs, prog = data.split("\n\n")
    registers = {"A": 0, "B": 0, "C": 0}
    for line in regs.splitlines():
        k, v = line.split(":")
        registers[k.split()[1]] = int(v)

    print(registers)

    program = [int(p) for p in prog.split(": ")[1].split(",")]
    print(program)

    i = 0
    while True:
        registers = {"A": i, "B": 0, "C": 0}
        prog = [p for p in program]
        out = []
        pointer = 0
        while pointer < len(program):
            registers, pointer, out = runOp(
                registers, program[pointer], program[pointer+1], pointer, out)
            pointer += 2
            # print(f"{registers=} {pointer=}")
            if program[:len(out)] != out:
                break

        if out == program:
            return i
        i += 1


if __name__ == "__main__":
    main()
