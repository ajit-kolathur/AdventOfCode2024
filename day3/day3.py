import re

def main():
    with open("./data/day3/input") as file:
        lines = [line.rstrip() for line in file]
    
    sum = 0
    counts = True

    for line in lines:
        # for match in re.finditer(r"mul\(([0-9]{1,3}),([0-9]{1,3})\)", line): # Part 1
        for match in re.finditer(r"mul\(([0-9]{1,3}),([0-9]{1,3})\)|do\(\)|don\'t\(\)", line): # Part 2
            if "do()" in match.group(0):
                counts = True
            elif "don't()" in match.group(0):
                counts = False
            elif "mul" in match.group(0):
                x = int(match.group(1))
                y = int(match.group(2))
                if counts:
                    sum += (x * y)
    print(sum)

if __name__ == "__main__":
    main()