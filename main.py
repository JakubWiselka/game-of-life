import pygame
import numpy as np
import random
import time
import math

COL_DRAW = (100, 255, 100)
COL_ABOUNT_TO_DIE = (255, 150, 150)
COL_ALIVE = (255, 255, 215)
COL_BACKGROUND = (10, 10, 40)
COL_GRID = (30, 30, 60)
GAME_SIZE = (50, 50, 10)
GAME_TICK = 0.2

SETTINGS = {
    'pause': False,
    'random_start': True,
}

def update(surface, cur, sz):
    nxt = np.zeros((cur.shape[0], cur.shape[1]))

    for r, c in np.ndindex(cur.shape):

        num_alive = np.sum(cur[r-1:r+2, c-1:c+2]) - cur[r, c]

        if cur[r, c] == 1 and num_alive < 2 or num_alive > 3:
            col = COL_ABOUNT_TO_DIE
        elif (cur[r, c] == 1 and 2 <= num_alive <= 3) or (cur[r, c] == 0 and num_alive == 3):
            nxt[r, c] = 1
            col = COL_ALIVE

        col = col if cur[r, c] == 1 else COL_BACKGROUND
        pygame.draw.rect(surface, col, (c*sz, r*sz, sz-1, sz-1))

    return nxt

def init(dimx, dimy):
    cells = np.zeros((dimy, dimx))
    if SETTINGS['random_start']:
        for row in range(cells.shape[0]):
            for el in range(cells.shape[1]):
                r = random.randint(1, 9)
                if r == 1:
                    cells[row][el] = r

    return cells

def main(dimx, dimy, cellsize):
    pygame.init()
    surface = pygame.display.set_mode((dimx * cellsize, dimy * cellsize))
    pygame.display.set_caption("GAME OF LIFE")

    cells = init(dimx, dimy)
    tick = time.time()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                SETTINGS['pause'] = False if SETTINGS['pause'] else True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                cells = np.zeros((dimy, dimx))
            if event.type in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN] and pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
                mouse = pygame.mouse.get_pressed()
                pos = pygame.mouse.get_pos()
                col = math.floor(pos[0]/GAME_SIZE[2])
                row = math.floor(pos[1]/GAME_SIZE[2])
                if mouse[0]:
                    cells[row][col] = 1
                    color = COL_DRAW
                elif mouse[2]:
                    cells[row][col] = 0
                    color = COL_BACKGROUND
                pygame.draw.rect(surface, color, (col*cellsize, row*cellsize, cellsize-1, cellsize-1))
                

        if not SETTINGS['pause'] and (time.time() - tick) > GAME_TICK:
            tick = time.time()
            surface.fill(COL_GRID)
            cells = update(surface, cells, cellsize)
            pygame.display.update()
        pygame.display.update()
        


if __name__ == "__main__":
    main(GAME_SIZE[0],GAME_SIZE[1],GAME_SIZE[2])
