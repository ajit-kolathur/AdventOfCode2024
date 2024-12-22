import re
from multiprocessing import Pool

def read_program(file_name):
    with open(file_name) as file:
        lines = [line.rstrip() for line in file]
    
    register_regex = r"Register (?P<register>[A-Z]): (?P<value>\d+)"
    program_regex = r"Program: (?P<program>[0-9\,]+)"
    reg_a = None
    reg_b = None
    reg_c = None
    program = None
    
    for line in lines:
        if "Register" in line:
            match = re.match(register_regex, line)
            register = match.group("register")
            value = int(match.group("value"))

            if register == "A":
                reg_a = value
            elif register == "B":
                reg_b = value
            elif register == "C":
                reg_c = value
        elif "Program" in line:
            match = re.match(program_regex, line)
            program = [int(entry) for entry in match.group("program").split(',')]
    return program, reg_a, reg_b, reg_c

def get_combo_operand(operand, reg_a, reg_b, reg_c):
    if 0 <= operand <= 3:
        return get_literal_operand(operand)
    if operand == 4:
        return reg_a
    if operand == 5:
        return reg_b
    if operand == 6:
        return reg_c
    if operand == 7:
        raise Exception("Invalid program")

def get_literal_operand(operand):
    return operand

def run_program(program, reg_a, reg_b, reg_c):
    a = reg_a
    b = reg_b
    c = reg_c

    # instruction pointer starts at 0
    ip = 0
    outputs = []

    while ip < len(program):
        instruction = program[ip]
        match instruction:
            case 0:
                # The adv instruction (opcode 0) performs division. The numerator is the value in the A register. The denominator is found by raising 2 to the power of the instruction's combo operand. (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.) The result of the division operation is truncated to an integer and then written to the A register.
                a = a // (2**get_combo_operand(program[ip+1],a, b, c))
                ip += 2
                continue
            case 1:
                # The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal operand, then stores the result in register B.
                b = b ^ get_literal_operand(program[ip+1])
                ip += 2
                continue
            case 2:
                # The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby keeping only its lowest 3 bits), then writes that value to the B register.
                b = get_combo_operand(program[ip+1],a, b, c) % 8
                ip += 2
                continue
            case 3:
                # The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero, it jumps by setting the instruction pointer to the value of its literal operand; if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.
                if a == 0:
                    ip += 2
                else:
                    ip = get_literal_operand(program[ip+1])
                continue
            case 4:
                # The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores the result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)
                b = b ^ c
                ip += 2
                continue
            case 5:
                # The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value. (If a program outputs multiple values, they are separated by commas.)
                outputs.append(get_combo_operand(program[ip+1],a, b, c)%8)
                ip += 2
                continue
            case 6:
                # The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored in the B register. (The numerator is still read from the A register.)
                b = a // (2**get_combo_operand(program[ip+1],a, b, c))
                ip += 2
                continue
            case 7:
                # The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored in the C register. (The numerator is still read from the A register.)
                c = a // (2**get_combo_operand(program[ip+1],a, b, c))
                ip += 2
                continue
    return [output for output in outputs]

def zipped_run_program(entries):
    return run_program(entries[0], entries[1], entries[2], entries[3]) == entries[0]


def main():
    # Part 1
    program, reg_a, reg_b, reg_c = read_program("./day17/input")
    outputs = run_program(program, reg_a, reg_b, reg_c)
    print(",".join([str(output) for output in outputs]))

    # Part 2
    # replace reg_a with a value that would make outputs == program
    # Attempt 1: brute force
    # seach_range = [(program, new_reg_a, reg_b, reg_c) for new_reg_a in range(100000000)]
    
    # p = Pool()
    # outputs = p.map(zipped_run_program, seach_range)

    # print(outputs.index(True))
    # Attempt 2: evaluate what changes are made to a and debug
    # Attempt 3: evaluate all operations and find those that modify and work backwards
if __name__ == "__main__":
    main()