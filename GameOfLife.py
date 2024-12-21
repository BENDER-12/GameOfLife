import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
CELL_SIZE = 15
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
FPS = 15

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Create grid
def create_grid(rows, cols):
    return [[0 for _ in range(cols)] for _ in range(rows)]

def draw_grid(surface, grid):
    for row in range(ROWS):
        for col in range(COLS):
            color = GREEN if grid[row][col] else WHITE
            pygame.draw.rect(surface, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1))

# Count live neighbors
def count_live_neighbors(grid, x, y):
    neighbors = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    count = 0
    for dx, dy in neighbors:
        nx, ny = x + dx, y + dy
        if 0 <= nx < ROWS and 0 <= ny < COLS:
            count += grid[nx][ny]
    return count

# Update grid
def next_generation(grid):
    new_grid = create_grid(ROWS, COLS)
    for row in range(ROWS):
        for col in range(COLS):
            live_neighbors = count_live_neighbors(grid, row, col)
            if grid[row][col] == 1:  # Alive
                if live_neighbors in (2, 3):
                    new_grid[row][col] = 1
            else:  # Dead
                if live_neighbors == 3:
                    new_grid[row][col] = 1
    return new_grid

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game of Life - User Manipulated")
    clock = pygame.time.Clock()

    grid = create_grid(ROWS, COLS)
    running = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row, col = y // CELL_SIZE, x // CELL_SIZE
                grid[row][col] = 1 - grid[row][col]  # Toggle cell

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running  # Start/Stop simulation
                if event.key == pygame.K_c:
                    grid = create_grid(ROWS, COLS)  # Clear the grid

        screen.fill(BLACK)

        if running:
            grid = next_generation(grid)

        draw_grid(screen, grid)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
