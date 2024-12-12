from queue import Queue

lookup = {}

def get_numbers(file_path):
    with open(file_path) as file:
        content = file.read()
        return [int(entry) for entry in content.split(' ') if entry != '']

def single_number_blink(number, count):
    if count == 0:
        return 1

    tup = (number, count)
    if tup in lookup:
        return lookup[tup]

    results = 0
    if number == 0:
        result = single_number_blink(1, count - 1)
        results += result
        lookup[(1, count - 1)] = result
    elif len(list(str(number))) % 2 == 0:
        numb_str = list(str(number))
        first_half_str = "".join(numb_str[:len(numb_str)//2])
        second_half_str = "".join(numb_str[len(numb_str)//2:])
        first_half = int(first_half_str if first_half_str != "" else "0")
        second_half = int(second_half_str if second_half_str != "" else "0")
        first_result = single_number_blink(first_half, count - 1)
        second_result = single_number_blink(second_half, count - 1)
        lookup[(first_half, count -1)] = first_result
        lookup[(second_half, count -1)] = second_result
        results += first_result
        results += second_result
    else:
        result = single_number_blink(number * 2024, count -1)
        lookup[(number * 2024, count -1)] = result
        results += result
    
    lookup[tup] = results
    return results

def blink(numbers, count):
    final_list = 0

    for number in numbers:
        new_numbers = single_number_blink(number, count)
        final_list += new_numbers
    return final_list

def main():
    # Test1
    # print(blink(get_numbers("./day11/test1"), 1))
    # Test
    # print(blink(get_numbers("./day11/test"), 6))
    # Part 1 
    # print(blink(get_numbers("./day11/input"), 25))
    # Part 2
    print(blink(get_numbers("./day11/input"), 75))
if __name__ == "__main__":
    main()