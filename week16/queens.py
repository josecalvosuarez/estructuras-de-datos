def is_safe(board, row, col):
    """
    Check if a queen can be safely placed at (row, col) on the board.
    Ensures no other queen is in the same column or diagonal.
    """
    for prev_row in range(row):
        prev_col = board[prev_row]

        # Same column
        if prev_col == col:
            return False

        # Same diagonal
        if abs(prev_row - row) == abs(prev_col - col):
            return False

    return True


def solve_n_queens_util(n, row, board, solutions):
    """
    Recursive helper that tries to place queens row by row.
    If a safe position is found, move to the next row.
    When all rows are filled, store the valid board configuration.
    """
    if row == n:
        solutions.append(board[:])
        return

    for col in range(n):
        if is_safe(board, row, col):
            board[row] = col
            solve_n_queens_util(n, row + 1, board, solutions)
            board[row] = -1  # backtrack


def solve_n_queens(n):
    """
    Main function to solve the N-Queens problem.
    Initializes the board and collects all valid solutions.
    """
    solutions = []
    board = [-1] * n
    solve_n_queens_util(n, 0, board, solutions)
    return solutions


# Example for 4x4
solutions = solve_n_queens(4)
for s in solutions:
    print(s)
