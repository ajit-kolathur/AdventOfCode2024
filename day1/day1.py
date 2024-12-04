def main():
    with open("./day1/input") as file:
        lines = [line.rstrip() for line in file]
    a = []
    b = []

    for line in lines:
        tokens = [token for token in line.split(" ") if token != ""]
        a.append(int(tokens[0]))
        b.append(int(tokens[1]))
    
    a.sort()
    b.sort()

    sum = 0
    for i in range(len(a)):
        sum += abs(a[i] - b[i])
    print(sum) # Part 1 answer

    a = []
    b = {}

    for line in lines:
        tokens = [token for token in line.split(" ") if token != ""]
        a.append(tokens[0])
        if tokens[1] in b:
            b[tokens[1]] += 1
        else:
            b[tokens[1]] = 1

    sum = 0
    for val in a:
        if val in b:
            sum += int(b[val]) * int(val)
    print(sum) # Part 2 answer


if __name__ == "__main__":
    main()