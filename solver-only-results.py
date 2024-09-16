from random import randint
import time

GRID_LENGTH = 4


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
        mover = x + y*GRID_LENGTH
        if direction == "up" or direction == "down":
          mover = y + x*GRID_LENGTH
        movee = mover + change
        if grid[mover] != 0 and grid[movee] == grid[mover] and grid_check[mover] == False and grid_check[movee] == False:
          grid[movee] = grid[mover]*2
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
    i = True
    while i:
      block = randint(0, (GRID_LENGTH**2 - 1))
      if grid[block] == 0:
        four = randint(0, 9)
        if four == 0:
          grid[block] = 4
        else:
          grid[block] = 2
        i = False


def ai_run(grid, high, t):
  best = (-1, -1)
  weights = [2, 2, 1, 1, 4, 4, 3, 2, 8, 16, 16, 32, 512, 128, 128, 64]
  def score(g, w):
    sum = 0
    for j in range(0, len(g) - 1):
      if high == g[j] and j == 12:
        sum += (g[j]*w[j]*2)
      elif (g[13] == g[14]*2 and j == 15) or (g[14] == g[15]*2 and j == 11) or (g[12] == g[13]*2 and j == g[14]) or (g[14] == g[15]*2 and j == 11):
        sum += (g[j]*w[j]*2)
      else:
        sum += (g[j]*w[j])
    return sum

  check = False
  for ke in range(0, 3):
    t_grid2 = list(grid)
    g_check2 = [False]*(GRID_LENGTH**2)
    val = False
    if ke == 0:
      val = move(t_grid2, g_check2, "down")
    elif ke == 1:
      val = move(t_grid2, g_check2, "left")
    elif ke == 3:
      val = move(t_grid2, g_check2, "up")
    elif ke == 2:
      val = move(t_grid2, g_check2, "right")
    if val:
      for k in range(0, 3):
        t_grid = list(t_grid2)
        g_check = [False]*(GRID_LENGTH**2)
        v = False
        if k == 0:
          v = move(t_grid, g_check, "down")
          check = True
        elif k == 1:
          v = move(t_grid, g_check, "left")
          check = True
        elif k == 3:
          v = move(t_grid, g_check, "up")
          check = True
        elif k == 2:
          v = move(t_grid, g_check, "right")
          check = True
        if v:
          for key in range(0, 3):
            temp_grid = list(t_grid)
            grid_check = [False]*(GRID_LENGTH**2)
            if key == 0:
              valid = move(temp_grid, grid_check, "down")
              sc = score(temp_grid, weights) // 3
              sc += score(t_grid, weights) // 1.5
              sc += score(t_grid2, weights)
              if sc > best[1] and valid:
                best = (ke, sc)
            elif key == 1:
              valid = move(temp_grid, grid_check, "left")
              sc = score(temp_grid, weights) // 3
              sc += score(t_grid, weights) // 1.5
              sc += score(t_grid2, weights)
              if sc > best[1] and valid:
                best = (ke, sc)
            elif key == 3:
              valid = move(temp_grid, grid_check, "up")
              sc = score(temp_grid, weights) // 3
              sc += score(t_grid, weights) // 1.5
              sc += score(t_grid2, weights)
              if sc > best[1] and valid:
                best = (ke, sc)
            elif key == 2:
              valid = move(temp_grid, grid_check, "right")
              sc = score(temp_grid, weights) // 3
              sc += score(t_grid, weights) // 1.5
              sc += score(t_grid2, weights)
              if sc > best[1] and valid:
                best = (ke, sc)
          grid_check = [False]*(GRID_LENGTH**2)
  if 0 not in grid and not check:
    print(f"TRIAL END, {round(time.time() - t, 3)} s, MAX BLOCK: {high}")
    t = time.time()
    for x in range(0, GRID_LENGTH**2):
      grid[x] = 0
    grid[randint(0, GRID_LENGTH**2 - 1)] = 2
    return t
  grid_check = [False]*(GRID_LENGTH**2)
  if best[0] == -1:
    move(grid, grid_check, "up")
    new_block(grid)
    move(grid, grid_check, "down")
  elif best[0] == 0:
    move(grid, grid_check, "down")
  elif best[0] == 1:
    move(grid, grid_check, "left")
  elif best[0] == 3:
    move(grid, grid_check, "up")
  elif best[0] == 2:
    move(grid, grid_check, "right")
  new_block(grid)
  return t

def main():
  running = True
  global high
  global t
  t = time.time()

  grid = [0 for _ in range(GRID_LENGTH**2)]
  first_block = randint(0, (GRID_LENGTH**2 - 1))
  grid[first_block] = 2
  while running:
    high = max(grid)
    t = ai_run(grid, high, t)


if __name__ == "__main__":
  main()
