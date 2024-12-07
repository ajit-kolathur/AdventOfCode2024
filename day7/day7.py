def find_possible_solutions(problems, functions):
    sum = 0
    for problem in problems:
        expected_sum = problem[0]
        solved = False
        formulae = [(None, problem[1])]

        while len(formulae) > 0:
            formula =  formulae.pop(0)

            if not formula[0]:
                formulae.append((formula[1][0], formula[1][1:]))
                continue
            else:
                if len(formula[1]) > 0:
                    for function in functions:
                        if formula[0] <= expected_sum:
                            formulae.append((function(formula[0], formula[1][0]), formula[1][1:]))
                else:
                    if formula[0] == expected_sum:
                        solved = True
                        break
                    else:
                        continue
        if solved:
            sum += expected_sum
    
    return sum

def main():
    problems = []
    with open("./day7/input") as file:
        for line in file:
            tokens = line.split(':')
            total = int(tokens[0])
            numbers =  [int(numb) for numb in tokens[1].strip().split(' ')]
            problems.append((total, numbers))

    sum = find_possible_solutions(problems, [lambda a,b: a+b, lambda a,b: a*b])
    print(sum) # Part 1

    sum = find_possible_solutions(problems, [lambda a,b: a+b, lambda a,b: a*b, lambda a,b: int(f"{a}{b}")])
    print(sum) # Part 2
if __name__ == "__main__":
    main()