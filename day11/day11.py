from queue import Queue

lookup = {}

def get_numbers(file_path):
    with open(file_path) as file:
        content = file.read()
        return [int(entry) for entry in content.split(' ') if entry != '']

def single_number_blink(tup):
    if tup in lookup:
        return lookup[tup]

    numbers = []
    if tup[0] == 0:
        numbers.append((1, tup[1] - 1))
    elif len(list(str(tup[0]))) % 2 == 0:
        numb_str = list(str(tup[0]))
        first_half_str = "".join(numb_str[:len(numb_str)//2])
        second_half_str = "".join(numb_str[len(numb_str)//2:])
        first_half = int(first_half_str if first_half_str != "" else "0")
        second_half = int(second_half_str if second_half_str != "" else "0")
        numbers.append((first_half, tup[1] -1))
        numbers.append((second_half, tup[1] -1))
    else:
        numbers.append((tup[0] * 2024, tup[1] -1))
    
    lookup[tup] = numbers
    return numbers

def blink(numbers, count):
    final_list = []
    work_queue = []
    for number in numbers:
        work_queue.append((number, count))
    
    while len(work_queue) > 0:
        element = work_queue.pop(0)
        if element[1] == 0:
            final_list.append(element[0])
            continue
        new_elements = single_number_blink(element)
        for new_element in new_elements:
            work_queue.append(new_element)
    return final_list

def main():
    # Test1
    # print(blink(get_numbers("./day11/test1"), 1))
    # Test
    # print(blink(get_numbers("./day11/test"), 6))
    # Part 1 
    print(len(blink(get_numbers("./day11/input"), 25)))
    # Part 2
    # print(len(blink(get_numbers("./day11/input"), 75)))
if __name__ == "__main__":
    main()