import copy

def find_next_unused_spot(disk, start):
    while start < len(disk):
        if disk[start] == '.':
            break
        start += 1
    
    end = start
    while end < len(disk):
        if disk[start] != disk[end]:
            break
        end += 1

    return start, end - 1, end - start

def find_last_file(disk, end, specific=None):
    while end >= 0:
        if disk[end] != '.':
            if not specific or disk[end] == specific:
                break
        end -= 1
    
    start = end
    while start >= 0:
        if disk[end] != disk[start]:
            break
        start -= 1 

    return start + 1, end, end - start

def part1_compression(disk):
    # Find first unused disk space
    first_unused, _, _ = find_next_unused_spot(disk, 0)
    # Find last used disk space
    _, last_used, _ = find_last_file(disk, len(disk) -1)
    while first_unused < last_used:
        # Exchange
        temp = disk[first_unused]
        disk[first_unused] = disk[last_used]
        disk[last_used] = temp

        first_unused, _, _ = find_next_unused_spot(disk, first_unused)
        _, last_used, _ = find_last_file(disk, last_used)

def part2_compression(disk, max_file_id):
    file_id = max_file_id

    while file_id >= 0:
        file_start, file_end, file_length = find_last_file(disk, len(disk) - 1, str(file_id))

        unused_spot_start, unused_spot_end, unused_spot_length = find_next_unused_spot(disk, 0)
        while unused_spot_start < file_start:
            if unused_spot_length >= file_length:
                # Move
                for i in range(unused_spot_start, unused_spot_start + file_length):
                    disk[i] = disk[file_start]
                # Clear
                for i in range(file_start, file_start + file_length):
                    disk[i] = '.'
                break
            else:
                unused_spot_start, unused_spot_end, unused_spot_length = find_next_unused_spot(disk, unused_spot_end + 1)
        file_id -= 1
    
def generate_checksum(disk):
    checksum = 0
    for index, value in enumerate(disk):
        if value != '.':
            checksum += (index * int(value))
    return checksum

def main():
    with open("./day9/input") as file:
        items = [list(line.rstrip()) for line in file][0]

    # Process representation into actual disk content
    uncompressed_disk_content = []
    file_id = 0

    for index, value in enumerate(items):
        value = int(value)
        if index % 2 == 0:
            uncompressed_disk_content.extend([f"{file_id}"] * value)
            file_id += 1
        else:
            uncompressed_disk_content.extend(["."] * value)
    
    # Debugging
    # print(f"Uncompressed: {''.join(uncompressed_disk_content)}")
    
    # Part 1
    disk = copy.deepcopy(uncompressed_disk_content)
    # Compress
    part1_compression(disk)
    # Debugging
    # print(f"Compressed: {''.join(disk)}")
    # Find part 1 answer
    checksum = generate_checksum(disk)
    print(f"Part 1: {checksum}")

    # Part 2
    disk = copy.deepcopy(uncompressed_disk_content)
    # Compress
    part2_compression(disk, file_id - 1)
    # Debugging
    # print(f"Compressed: {''.join(disk)}")
    # Find part 2 answer
    checksum = generate_checksum(disk)
    print(f"Part 2: {checksum}")
    

if __name__ == "__main__":
    main()
