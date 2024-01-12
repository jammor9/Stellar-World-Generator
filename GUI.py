import pygame as pg
from pygame.locals import *

import numpy as np

def load_gui(world, size):

    tile_size = 16
    screen_width = 1280
    screen_height = 720

    class Level:
        def __init__(self, world, surface):
            self.display_surface = surface

            terrain_layout = world
            self.terrain_sprites = self.create_tile_group(terrain_layout, world)

        def create_tile_group(self,layout,type):
            sprite_group = pg.sprite.Group()
            
            for row_i, row in enumerate(layout):
                for col_i, col in enumerate(row):
                    if col != 0:
                        x = col_i * tile_size
                        y = row_i * tile_size

                        if type == world:
                            terrain_tile_list = import_cut_graphics('Graphics/StarTiles.png', tile_size)
                            tile_surface = terrain_tile_list[int(col)]
                            sprite = StaticTile(tile_size,x,y,tile_surface)
                            sprite_group.add(sprite)
            print(sprite_group)
            return sprite_group

        def run(self):
            self.terrain_sprites.draw(self.display_surface)
            self.terrain_sprites.update(1)

    class Tile(pg.sprite.Sprite):
        def __init__(self, size, x, y):
            super().__init__()
            self.image = pg.Surface((size, size))
            self.rect = self.image.get_rect(topleft = (x,y))

        def update(self, shift):
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == K_UP:
                        self.rect.y += 1

    class StaticTile(Tile):
        def __init__(self, size, x, y, surface):
            super().__init__(size, x, y)
            self.image = surface

    screen = pg.display.set_mode((screen_width, screen_height))
    clock = pg.time.Clock()
    level = Level(world, screen)

    #Imports the StarMap Tiles
    star_map = import_cut_graphics('Graphics/StarTiles.png', tile_size)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.KEYDOWN:
                if K_ESCAPE:
                    pg.quit()

        
        screen.fill('black')
        level.run()

        pg.display.update()
        clock.tick(60)

#Imports spritesheets
def import_cut_graphics(path, tile_size):
    surface = pg.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tile_size)
    tile_num_y = int(surface.get_size()[1] / tile_size)

    cut_tiles = []

    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            new_surf = pg.Surface((tile_size, tile_size))
            new_surf.blit(surface,(0,0),pg.Rect(x,y,tile_size,tile_size))
            cut_tiles.append(new_surf)

    return cut_tiles

