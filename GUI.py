import pygame as pg
from pygame.locals import *

import numpy as np
from numpy import random

def load_gui(world, size):

    file = 'Graphics/StarTiles.png'
    TILE_SIZE = 16

    class Game:
        W = size * TILE_SIZE
        H = size * TILE_SIZE
        SIZE = W, H

        def __init__(self, tileset, size=(10, 20), rect=None):
            pg.init()
            self.screen = pg.display.set_mode(Game.SIZE)
            pg.display.set_caption('Star Map')
            self.running = True

            self.size = size
            self.tileset = tileset
            self.map = np.zeros(size, dtype=int)

            h, w = self.size
            self.image = pg.Surface((TILE_SIZE*w, TILE_SIZE*h))
            if rect:
                self.rect = pg.Rect(rect)
            else:
                self.rect = self.image.get_rect()

        def run(self):
            while self.running:
                for event in pg.event.get():
                    if event.type == QUIT:
                        self.running = False
                    elif event.type == KEYDOWN:
                        if event.key == K_1:
                            self.load_image(file)
                        elif event.key == K_r:
                            self.set_random()
                        elif event.key == K_ESCAPE:
                            pg.quit()
                            

            pg.quit()

        def load_image(self, file):
            self.file = file
            self.image = pg.image.load(file)
            self.rect = self.image.get_rect()

            self.screen = pg.display.set_mode(self.rect.size)
            pg.display.set_caption(f'size{self.rect.size}')
            self.screen.blit(self.image, self.rect)
            pg.display.update()

        def set_zero(self):
            self.map = np.zeros(self.size, dtype=int)
            print(self.map)
            print(self.map.shape())
            self.render()

        def set_random(self):
            n = len(self.tileset.tiles)
            self.map = random.randint(n, size=self.size)
            print(self.map)
            self.render()

        def render(self):
            m, n = self.map.shape
            for i in range(m):
                for j in range(n):
                    tile = self.tileset.tiles[self.map[i, j]]
                    self.image.blit(tile, (j*TILE_SIZE, i*TILE_SIZE))

    class Tileset:
        def __init__(self, file, size=(TILE_SIZE, TILE_SIZE), margin=0, spacing=0):
            self.file = file
            self.size = size
            self.margin = margin
            self.spacing = spacing
            self.image = pg.image.load(file)
            self.rect = self.image.get_rect()
            self.tiles = []
            self.load()

        def load(self):
            self.tiles = []
            x0 = y0 = self.margin
            w, h = self.rect.size
            dx = self.size[0] + self.spacing
            dy = self.size[1] + self.spacing

            for x in range(x0, w, dx):
                for y in range(y0, h, dy):
                    tile = pg.surface(self.size)
                    tile.blit(self.image, (0, 0), (x, y, *self.size))
                    self.tiles.append(tile)

        def __str__(self):
            return f'{self.__class__.__name__} file:{self.file} tile:{self.size}'

    class TileMap:
        def __init__(self, tileset, size=(10, 20), rect=None):
            self.size = size
            self.tileset = tileset
            self.map = np.zeros(size, dtype=int)

            h, w = self.size
            self.image = pg.Surface((TILE_SIZE*w, TILE_SIZE*h))
            if rect:
                self.rect = pg.Rect(rect)
            else:
                self.rect = self.image.get_rect()

        def render(self):
            m, n = self.map.shape
            for i in range(m):
                for j in range(n):
                    tile = self.tileset.tiles[self.map[i, j]]
                    self.image.blit(tile, (j*TILE_SIZE, i*TILE_SIZE))

        def set_zero(self):
            self.map = np.zeros(self.size, dtype=int)
            print(self.map)
            print(self.map.shape())
            self.render()

        def set_random(self):
            n = len(self.tileset.tiles)
            self.map = random.randint(n, size=self.size)
            print(self.map)
            self.render()

        def __str__(self):
            return f'{self.__class__.__name__} {self.size}'


    game = Game()
    game.run()