import random
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

# Define color schemes for different tile values
def get_tile_color(value):
    """Return the appropriate color for a tile based on its value."""
    color_map = {
        0: Fore.WHITE,
        2: Fore.GREEN,
        4: Fore.BLUE,
        8: Fore.CYAN,
        16: Fore.MAGENTA,
        32: Fore.RED,
        64: Fore.YELLOW,
        128: Fore.LIGHTGREEN_EX,
        256: Fore.LIGHTBLUE_EX,
        512: Fore.LIGHTRED_EX,
        1024: Fore.LIGHTMAGENTA_EX,
        2048: Fore.LIGHTYELLOW_EX,
        4096: Fore.LIGHTCYAN_EX
    }
    return color_map.get(value, Fore.WHITE + Style.BRIGHT)


def init_board():
    """Initialize a 4x4 board with two random tiles added."""
    board = [[0] * 4 for _ in range(4)]
    add_tile(board)
    add_tile(board)
    return board, 0  # Return initial board and score of 0


def add_tile(board):
    """Add a new tile to a random empty cell. 90% chance of a 2, 10% chance of a 4."""
    empty_cells = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if not empty_cells:
        return
    i, j = random.choice(empty_cells)
    board[i][j] = 4 if random.random() < 0.1 else 2


def print_board(board, score):
    """Display the board in a formatted grid with score."""
    # Print score bar with color
    print(Fore.CYAN + Style.BRIGHT + f"Score: {score}")
    print(Fore.BLUE + "-" * 17)
    
    for row in board:
        print(Fore.BLUE + "|", end="")
        for cell in row:
            # Use appropriate color for each cell
            cell_color = get_tile_color(cell)
            # Use a dot for empty cells
            if cell == 0:
                print(cell_color + "   .", end=Fore.BLUE + "|")
            else:
                print(cell_color + "{:4}".format(cell), end=Fore.BLUE + "|")
        print("\n" + Fore.BLUE + "-" * 17)


def merge(row):
    """
    Merge a single row to the left by
    1. Removing zeros.
    2. Merging equal numbers (only once per merge operation).
    3. Padding the row with zeros on the right.
    Returns the merged row and the points gained from merging.
    """
    non_zero = [num for num in row if num != 0]
    merged = []
    skip = False
    points = 0  # Track points gained in this merge
    for i in range(len(non_zero)):
        if skip:
            skip = False
            continue
        # If the current and next tile are equal, merge them
        if i + 1 < len(non_zero) and non_zero[i] == non_zero[i + 1]:
            merged_value = non_zero[i] * 2
            merged.append(merged_value)
            points += merged_value  # Add the value of the merged tile to points
            skip = True  # Skip next tile since it has been merged
        else:
            merged.append(non_zero[i])
    # Pad with zeros to maintain row length
    merged += [0] * (4 - len(merged))
    return merged, points


def move_left(board):
    """Perform a left move on the board."""
    new_board = []
    changed = False
    points_gained = 0
    for row in board:
        new_row, row_points = merge(row)
        points_gained += row_points
        if new_row != row:
            changed = True
        new_board.append(new_row)
    return new_board, changed, points_gained


def reverse(board):
    """Reverse each row in the board (used for moves to the right)."""
    return [row[::-1] for row in board]


def transpose(board):
    """Transpose the board (swap rows and columns)."""
    return [list(row) for row in zip(*board)]


def move_right(board):
    """Perform a right move by reversing, merging as if moving left, and reversing again."""
    reversed_board = reverse(board)
    new_board, changed, points = move_left(reversed_board)
    new_board = reverse(new_board)
    return new_board, changed, points


def move_up(board):
    """Perform an upward move by transposing, merging to the left, and transposing back."""
    transposed = transpose(board)
    new_board, changed, points = move_left(transposed)
    new_board = transpose(new_board)
    return new_board, changed, points


def move_down(board):
    """Perform a downward move by transposing, performing a right move, and transposing back."""
    transposed = transpose(board)
    new_board, changed, points = move_right(transposed)
    new_board = transpose(new_board)
    return new_board, changed, points


def can_move(board):
    """Return True if there's at least one legal move available."""
    # Check for any empty cell
    for row in board:
        if 0 in row:
            return True
    # Check for possible horizontal merges
    for row in board:
        for i in range(3):
            if row[i] == row[i + 1]:
                return True
    # Check for possible vertical merges
    for j in range(4):
        for i in range(3):
            if board[i][j] == board[i + 1][j]:
                return True
    return False


def game_loop():
    """Main game loop: prints the board, takes user input, processes moves, and checks for win/loss."""
    board, score = init_board()
    while True:
        print_board(board, score)
        move = input(Fore.WHITE + Style.BRIGHT + "Enter move (W=Up, A=Left, S=Down, D=Right, Q=Quit): ").strip().lower()
        if move == 'q':
            print(Fore.RED + "Game aborted.")
            break
        if move not in ['w', 'a', 's', 'd']:
            print(Fore.RED + "Invalid move! Please try again.")
            continue

        if move == 'w':
            board, changed, points = move_up(board)
        elif move == 's':
            board, changed, points = move_down(board)
        elif move == 'a':
            board, changed, points = move_left(board)
        elif move == 'd':
            board, changed, points = move_right(board)

        if not changed:
            print(Fore.YELLOW + "Move not possible. Try a different direction.")
            continue

        # Update the score with points gained from the move
        score += points
        
        add_tile(board)

        # Check for win condition (tile with 2048 reached)
        if any(2048 in row for row in board):
            print_board(board, score)
            print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + f"Congratulations, you've reached 2048! Final score: {score}")
            continue_playing = input(Fore.WHITE + "Do you want to continue playing? (y/n): ").strip().lower()
            if continue_playing != 'y':
                break

        # Check for game over condition (no valid moves left)
        if not can_move(board):
            print_board(board, score)
            print(Fore.RED + Style.BRIGHT + f"Game Over. No more moves available! Final score: {score}")
            break


if __name__ == "__main__":
    game_loop()