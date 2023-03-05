import pygame as pg
import sys
import base64
import json
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *
import numpy as np
import io
import base64



def convert_img_to_base64(screen):
    buffer = io.BytesIO()
    pg.image.save(screen, buffer)
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str

class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        self.frame_counter = 0
        self.data = {
            "Player_Loc": [],
            "Enemies": [],
            "Kills": [],
            "Img": []
        }
        pg.time.set_timer(self.global_event, 40)
        self.new_game()

    def new_game(self):
        
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        pg.mixer.music.play(-1)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')
        self.data['Player_Loc']= [self.player.x,self.player.y] 
        # Update enemy locations and other properties
        enemies = []
        for npc in self.object_handler.npc_list:
            enemy = {
                'position': [npc.x, npc.y],
                'health': npc.health,
                'type': type(npc).__name__
                # add any other properties of the enemy here
            }
            enemies.append(enemy)
        self.data['Enemies'] = enemies
        self.data['Kills'] = self.object_handler.kill_count
        
        # Get the pixel values of the current screen image as a list of lists
        self.data['Img'] = convert_img_to_base64(self.screen)

        # Save data to JSON file
        self.frame_counter += 1
        if self.frame_counter == 5:
            with open("data.json", "w") as f:
                json.dump(self.data, f)
            self.frame_counter = 0

    def draw(self):
        # self.screen.fill('black')
        self.object_renderer.draw()
        self.weapon.draw()
        # self.map.draw()
        # self.player.draw()

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
