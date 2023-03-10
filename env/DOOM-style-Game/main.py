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
from io import BytesIO
from PIL import Image
import pandas as pd
from numpy import save
from numpy import savetxt
import csv


def convert_img_to_base64(screen):
    buffer = io.BytesIO()
    pg.image.save(screen, buffer)
    img_str = base64.b64encode(buffer.getvalue()).decode()
    image_data = base64.b64decode(img_str)
    

    # Create a BytesIO object from the decoded bytes
    image = Image.open(io.BytesIO(image_data)) 
    image_np = np.array(image)
    return image_np
    
    

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
            "Kills": []
        }
        self.img = []
        self.img_file = open('data/img.csv', 'w', newline='')
        self.img_writer = csv.writer(self.img_file)
        self.updf = pd.DataFrame()
        self.main_df = pd.DataFrame()
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
        self.data['Player_Loc'].append([self.player.x,self.player.y])
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
        self.data['Enemies'].append(enemies)
        self.data['Kills'].append(self.object_handler.kill_count)
        
        # Get the pixel values of the current screen image as a list of lists
        self.img.append(convert_img_to_base64(self.screen))
        # Append the current image to the list
        self.img.append(convert_img_to_base64(self.screen))

        # Write the image data to the CSV file
        self.img_writer.writerow(self.img[-1])
        
        # self.updf = pd.DataFrame(self.img)
        # self.main_df.append(self.updf)
        with open("data/g_stats.json", "w") as f:
                json.dump(self.data, f)
        
       
        

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

    def __del__(self):
        # Close the CSV file when the Game object is deleted
        self.img_file.close()


if __name__ == '__main__':
    game = Game()
    game.run()