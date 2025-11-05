import pygame
import sys

# --- Configuration ---

CELL_SIZE = 50
ROWS = 10
COLS = 10

WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

# Colors
COLOR_WALL = (40, 40, 40)
COLOR_EMPTY = (255, 255, 255)
COLOR_VISITING = (255, 215, 0)    # current exploration
COLOR_BACKTRACK = (255, 100, 100) # dead-end / backtrack
COLOR_PATH = (50, 205, 50)        # final solution path
COLOR_GRID = (200, 200, 200)


def build_maze():
    """
    Create a 10x10 maze with one guaranteed solution path
    and some extra dead-end branches to show backtracking.
    """
    maze = [[1] * COLS for _ in range(ROWS)]  # 1 = wall, 0 = free

    # Main path from (0,0) to (9,9)
    path = [
        (0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
        (1, 4), (2, 4), (3, 4),
        (3, 5), (3, 6), (3, 7),
        (4, 7), (5, 7), (6, 7),
        (6, 6), (6, 5),
        (7, 5), (8, 5), (9, 5),
        (9, 6), (9, 7), (9, 8), (9, 9)
    ]

    # Carve main path
    for r, c in path:
        maze[r][c] = 0

    # Add some branches (dead ends) off the main path
    for r, c in path:
        # Try to open a cell to the right
        if c + 1 < COLS and maze[r][c + 1] == 1 and (r + c) % 2 == 0:
            if (r, c + 1) != (ROWS - 1, COLS - 1):  # avoid goal
                maze[r][c + 1] = 0

        # Try to open a cell below
        if r + 1 < ROWS and maze[r + 1][c] == 1 and (r + c) % 3 == 0:
            if (r + 1, c) != (ROWS - 1, COLS - 1):
                maze[r + 1][c] = 0

    return maze


def draw_cell(screen, row, col, color):
    """
    Draw a single cell at (row, col) with the given color.
    """
    x = col * CELL_SIZE
    y = row * CELL_SIZE
    rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, COLOR_GRID, rect, 1)
    pygame.display.update(rect)


def draw_maze(screen, maze):
    """
    Draw the initial maze (walls and empty cells).
    """
    for r in range(ROWS):
        for c in range(COLS):
            if maze[r][c] == 1:
                color = COLOR_WALL
            else:
                color = COLOR_EMPTY
            draw_cell(screen, r, c, color)


def solve_maze(maze, visited, path, row, col, screen, depth=0):
    """
    Recursive backtracking solver.
    - maze: 2D grid with 0 = free, 1 = wall
    - visited: 2D grid marking visited cells
    - path: current path from start to this cell
    - (row, col): current position
    - depth: recursion depth (for pretty console printing)
    """
    pygame.event.pump()  # keep the window responsive

    indent = "  " * depth
    print(indent + "visit ({}, {})".format(row, col))

    # Bounds check
    if row < 0 or col < 0 or row >= ROWS or col >= COLS:
        print(indent + "out of bounds")
        return False

    # Wall or already visited
    if maze[row][col] == 1:
        print(indent + "hit wall")
        return False
    if visited[row][col]:
        print(indent + "already visited")
        return False

    # Mark as visited and add to path
    visited[row][col] = True
    path.append((row, col))

    # Visual: mark current cell as visiting
    draw_cell(screen, row, col, COLOR_VISITING)
    pygame.time.delay(80)  # slow down so we can see it

    # Goal check (bottom-right corner)
    if row == ROWS - 1 and col == COLS - 1:
        print(indent + "GOAL reached!")
        # Color final path in green
        for pr, pc in path:
            draw_cell(screen, pr, pc, COLOR_PATH)
            pygame.time.delay(40)
        return True

    # Explore neighbors: right, down, left, up
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for dr, dc in directions:
        next_row = row + dr
        next_col = col + dc
        if solve_maze(maze, visited, path, next_row, next_col, screen, depth + 1):
            return True

    # Backtrack: no way forward from here
    path.pop()
    draw_cell(screen, row, col, COLOR_BACKTRACK)
    pygame.time.delay(80)
    print(indent + "backtrack from ({}, {})".format(row, col))
    return False


def main():
    """
    Initialize pygame, build maze, solve it with backtracking,
    and keep window open until the user closes it.
    """
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Backtracking Maze Solver (10x10)")

    maze = build_maze()
    draw_maze(screen, maze)

    visited = [[False] * COLS for _ in range(ROWS)]
    path = []

    # Run the backtracking solver starting at (0, 0)
    solve_maze(maze, visited, path, 0, 0, screen)

    # Main loop to keep the window open after solving
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
