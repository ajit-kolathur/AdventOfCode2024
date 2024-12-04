import multiprocessing
import copy

def check_order(prev, curr, next, increasing):
    if increasing:
        if prev and prev >= curr:
            return False
        if next and next <= curr:
            return False
    else:
        if prev and prev <= curr:
            return False
        if next and next >= curr:
            return False
    return True

def check_diff (prev, curr, next, min_diff, max_diff):
    if prev and ((abs(prev - curr) < min_diff) or (abs(prev - curr) > max_diff)):
        return False
    if next and ((abs(next - curr) < min_diff) or (abs(next - curr) > max_diff)):
        return False
    return True

def check_safety(report, dampener=False):
    # determine direction
    increasing = True
    if report[0] > report[1]:
        increasing = False
    
    # check that the entire report obeys order
    # also check that adjacent elements differ by >= 1 to <= 3
    for i in range(len(report)):
        if i == 0:
            order = check_order(None, report[i], report[i+1], increasing)
            diff = check_diff(None, report[i], report[i+1], 1, 3)
        elif i == (len(report) - 1):
            order = check_order(report[i-1], report[i], None, increasing)
            diff = check_diff(report[i-1], report[i], None, 1, 3)
        else:
            order = check_order(report[i-1], report[i], report[i+1], increasing)
            diff = check_diff(report[i-1], report[i], report[i+1], 1, 3)

        if not (order and diff):
            if not dampener:
                return 0
            found_any = False
            for j in range(len(report)):
                clone_report = copy.deepcopy(report)
                del clone_report[j]
                if check_safety(clone_report, False) == 1:
                    found_any = True
                    break
            if not found_any:
                return 0
    return 1

def main():
    with open("./day2/input") as file:
        lines = [line.rstrip() for line in file]

    reports = []
    for line in lines:
        tokens = [int(token) for token in line.split(" ")]
        reports.append(tokens)

    results = []
    for report in reports:
        results.append(check_safety(report, True)) # Pass False for part 1

    print(sum(results))

if __name__ == "__main__":
    main()