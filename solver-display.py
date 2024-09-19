import pygame
from random import randint

GRID_LENGTH = 4
GRID_SIZE = int(100 * (1 / (GRID_LENGTH // 7 + 1)))
SPEED = float('inf')
counter = {2 ** x: 0 for x in range(0, 17)}
colors = {
    2: pygame.color.Color((231, 209, 186)),
    4: pygame.color.Color((225, 193, 158)),
    8: pygame.color.Color((230, 153, 71)),
    16: pygame.color.Color((239, 131, 17)),
    32: pygame.color.Color((239, 91, 17)),
    64: pygame.color.Color((239, 54, 17))
}


def init():
    global clock, screen
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((GRID_SIZE * GRID_LENGTH, GRID_SIZE * GRID_LENGTH), pygame.DOUBLEBUF)


def draw_handler(surface, grid):
    surface.fill(pygame.color.Color("white"))
    for x in range(0, screen.get_width(), GRID_SIZE):
        for y in range(0, screen.get_height(), GRID_SIZE):
            c_rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            cell_x = x // GRID_SIZE
            cell_y = y // GRID_SIZE
            block = cell_x + cell_y*GRID_LENGTH
            if 128 <= grid[block] < 4096:
                pygame.draw.rect(surface, pygame.color.Color((239, 232, 17)), c_rect)
            elif grid[block] >= 4096:
                pygame.draw.rect(surface, pygame.color.Color((25, 25, 13)), c_rect)
            elif grid[block] != 0 and grid[block] < 128:
                pygame.draw.rect(surface, colors[grid[block]], c_rect)
            if grid[block] != 0:
                pointfont = pygame.font.Font(None, int(200 // GRID_LENGTH))
                if grid[block] >= 4096:
                    col = (255, 255, 255)
                else:
                    col = (0, 0, 0)
                text = pointfont.render(f"{grid[block]}", True, col)
                text_rect = text.get_rect()
                text_rect.center = (x + (GRID_SIZE // 2), y + (GRID_SIZE // 2))
                surface.blit(text, text_rect)
            pygame.draw.rect(surface, pygame.color.Color("black"), c_rect, 2)


def move(grid, grid_check, direction):
    something = False
    for y in range(0, GRID_LENGTH):
        i = True
        m1, m2, m3 = 0, 0, 0
        if direction == "right":
            m1, m2, m3 = (GRID_LENGTH - 2), -1, -1
            change = 1
        elif direction == "left":
            m1, m2, m3 = 1, GRID_LENGTH, 1
            change = -1
        elif direction == "down":
            m1, m2, m3 = (GRID_LENGTH - 2), -1, -1
            change = GRID_LENGTH
        elif direction == "up":
            m1, m2, m3 = 1, GRID_LENGTH, 1
            change = -GRID_LENGTH

        while i:
            i = False
            for x in range(m1, m2, m3):
                mover = x + y * GRID_LENGTH
                if direction == "up" or direction == "down":
                    mover = y + x * GRID_LENGTH
                movee = mover + change
                if grid[mover] != 0 and grid[movee] == grid[mover] and grid_check[mover] == False and grid_check[
                    movee] == False:
                    grid[movee] = grid[mover] * 2
                    grid[mover] = 0
                    grid_check[movee] = True
                    grid_check[mover] = False
                    i = True
                    something = True
                elif grid[mover] != 0 and grid[movee] == 0:
                    grid[movee] = int(grid[mover])
                    grid[mover] = 0
                    i = True
                    something = True
    return something


def new_block(grid):
    while True:
        block = randint(0, (GRID_LENGTH ** 2 - 1))
        if grid[block] == 0:
            four = randint(0, 9)
            if four == 0:
                grid[block] = 4
            else:
                grid[block] = 2
            break

def key_press(event, grid):
    grid_check = [False] * (GRID_LENGTH ** 2)
    something = False
    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
        something = move(grid, grid_check, "down")
    elif event.key == pygame.K_w or event.key == pygame.K_UP:
        something = move(grid, grid_check, "up")
    elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
        something = move(grid, grid_check, "left")
    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
        something = move(grid, grid_check, "right")
    if something:
        new_block(grid)


def ai_run(grid, high):
    weights = [2, 2, 1, 1, 4, 4, 3, 2, 8, 16, 16, 32, 512, 128, 128, 64]

    def score(g, w):
        sum = 0
        for j in range(0, len(g) - 1):
            if high == g[j] and j == 12:
                sum += (g[j] * w[j] * 2)
            elif (g[13] == g[14] * 2 and j == 15) or (g[14] == g[15] * 2 and j == 11) or (
                    g[12] == g[13] * 2 and j == g[14]) or (g[14] == g[15] * 2 and j == 11):
                sum += (g[j] * w[j] * 2)
            else:
                sum += (g[j] * w[j])
        return sum

    best = [-1, -1]

    def fixed(depth, g, og_key, scor, test):
        for key in range(0, 3):
            temp_grid = list(g)
            grid_check = [False] * (GRID_LENGTH ** 2)
            valid = False
            new_score = scor
            if key == 0:
                valid = move(temp_grid, grid_check, "down")
            elif key == 1:
                valid = move(temp_grid, grid_check, "left")
            elif key == 2:
                valid = move(temp_grid, grid_check, "right")
            if depth == 0:
                og_key = key
                new_score += score(temp_grid, weights)
            elif depth == 1:
                new_score += score(temp_grid, weights) // 1.5
                test = True
            elif depth == 2:
                new_score += score(temp_grid, weights) // 3
            if valid:
                if depth == 2 and best[1] < new_score:
                    best[0] = og_key
                    best[1] = new_score
                elif depth != 2:
                    test = fixed(depth + 1, temp_grid, og_key, new_score, test)
        return test

    check = fixed(0, grid, -1, 0, False)

    if 0 not in grid and not check:
        counter[high] += 1
        total = ""
        for i in counter:
            if counter[i] > 0:
                total += f"{i}: {counter[i]},"
        print(total[:-1])
        for x in range(GRID_LENGTH**2):
            grid[x] = 0
        grid[randint(0, GRID_LENGTH ** 2 - 1)] = 2
        return
    grid_check = [False] * (GRID_LENGTH ** 2)
    if best[0] == -1:
        move(grid, grid_check, "up")
    elif best[0] == 0:
        move(grid, grid_check, "down")
    elif best[0] == 1:
        move(grid, grid_check, "left")
    elif best[0] == 2:
        move(grid, grid_check, "right")
    clock.tick(SPEED)
    new_block(grid)


def main():
    init()
    running = True
    auto = False

    grid = [0 for _ in range(GRID_LENGTH ** 2)]
    first_block = randint(0, (GRID_LENGTH ** 2 - 1))
    grid[first_block] = 2

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                auto = not auto
            elif event.type == pygame.KEYDOWN:
                key_press(event, grid)
        if auto:
            high = max(grid)
            ai_run(grid, high)
        draw_handler(screen, grid)
        pygame.display.flip()
        clock.tick(SPEED)


if __name__ == "__main__":
    main()
