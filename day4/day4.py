def word_search(grid, word):
    DIRECTIONS = [
        (0, 1, "right"),     # horizontal right
        (0, -1, "left"),     # horizontal left
        (1, 0, "down"),      # vertical down
        (-1, 0, "up"),       # vertical up
        (1, 1, "diagonal-down-right"),     # diagonal down-right
        (-1, -1, "diagonal-up-left"),      # diagonal up-left
        (1, -1, "diagonal-down-left"),     # diagonal down-left
        (-1, 1, "diagonal-up-right")       # diagonal up-right
    ]
    
    rows, cols = len(grid), len(grid[0])
    matches = []
    
    for start_row in range(rows):
        for start_col in range(cols):
            for d_row, d_col, direction in DIRECTIONS:
                if (0 <= start_row + d_row * (len(word) - 1) < rows and 
                    0 <= start_col + d_col * (len(word) - 1) < cols):
                    
                    if _check_word_match(grid, word, start_row, start_col, d_row, d_col):
                        matches.append((start_row, start_col, direction))
    
    return matches

def _check_word_match(grid, word, start_row, start_col, d_row, d_col):
    match = all(
        grid[start_row + i * d_row][start_col + i * d_col].lower() == 
        word[i].lower() 
        for i in range(len(word))
    )
    
    return match

def check_x_mas_pattern(grid):
    rows, cols = len(grid), len(grid[0])
    special_positions = []
    
    diag_up_left = (-1, -1)
    diag_up_right = (-1, 1)
    diag_down_right = (1, 1)
    diag_down_left = (1, -1)
    
    for row in range(rows):
        for col in range(cols):
            if grid[row][col].lower() != 'a':
                continue
            
            if (0 <= row + diag_up_left[0] < rows and 
                0 <= col + diag_up_left[1] < cols and
                0 <= row + diag_up_right[0] < rows and 
                0 <= col + diag_up_right[1] < cols and
                0 <= row + diag_down_right[0] < rows and 
                0 <= col + diag_down_right[1] < cols and
                0 <= row + diag_down_left[0] < rows and 
                0 <= col + diag_down_left[1] < cols):
                
                up_left = grid[row + diag_up_left[0]][col + diag_up_left[1]].lower()
                up_right = grid[row + diag_up_right[0]][col + diag_up_right[1]].lower()
                down_right = grid[row + diag_down_right[0]][col + diag_down_right[1]].lower()
                down_left = grid[row + diag_down_left[0]][col + diag_down_left[1]].lower()
                
                condition1 = ((up_left == 'm' and down_right == 's') or 
                              (up_left == 's' and down_right == 'm'))
                
                condition2 = ((up_right == 'm' and down_left == 's') or 
                              (up_right == 's' and down_left == 'm'))
                
                if condition1 and condition2:
                    special_positions.append((row, col))
    
    return special_positions

def main():
    with open("./day4/input") as file:
        grid = [line.rstrip() for line in file]
    word = "XMAS"
    matches = word_search(grid, word)
    print(len(matches))

    results = check_x_mas_pattern(grid)
    print(len(results))

if __name__ == "__main__":
    main()