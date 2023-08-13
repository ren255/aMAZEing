import pygame
import pygame_gui
# from dataclasses import dataclass

from Scene.Home_Scene import home
from Scene.Maze_Scene import maze
from main_logic import MazeGen,Render,Timer,Player



class Main:
    def __init__(self):
        window = (1400,900)
        pygame.init()

        self.call_back = call_back(self)

        self.screen = pygame.display.set_mode(window)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Maze Game")

        self.scenes = {
            "home" : home(self.screen),
            "maze" : maze(self.screen)
        }
        self.current_scene = self.scenes["home"]


    def quit(self,event):
        if event.type == pygame.QUIT:
            return 1
        elif event.type == pygame.KEYDOWN:
            # Press "Windows" + "w" to quit
            if event.key == pygame.K_w and event.mod & pygame.KMOD_LMETA:
                return 1
        return 0
            
    def update(self):
        self.screen.fill((255, 255, 255))
        fps = round(self.clock.get_fps()+0.1, 1)
        caption = "maze  " + str(fps) + "fps"
        pygame.display.set_caption(caption)

        self.current_scene.update(1 / fps)
        self.current_scene.draw(self.screen)

        if self.current_scene == self.scenes["maze"]:
            self.call_back.draw_map(
                self.map,
                self.current_scene.panel_map
            )
            
            self.call_back.draw_player(
                self.map,
                self.current_scene.panel_map
            )

        pygame.display.flip()
        self.clock.tick(60)

    def main_loop(self):
        while True:

            for event in pygame.event.get():
                self.current_scene.process_events(event)
                if self.quit(event):
                    pygame.quit()
                    return

                self.current_scene.handle_events(event,self.call_back)


            self.update()

# for main and scene
class call_back:
    def __init__(self,main):
        self.main = main
        self.MazeGen = MazeGen()
        self.render = Render()
        self.timer1 = Timer(1)
        self.reset_MapPlayer()


    # ------Map : Gen Render
    def updateMap(self):
        self.MazeGen.GenMap(21)
        self.main.map = self.MazeGen.map_data

    def draw_map(self,map_data, panel=None):
        self.render.draw_map(
            self.main.screen,
            map_data,
            panel
        )  

    # map--player
    
    def draw_player(self,map_data, panel=None):
        self.render.draw_player(
            self.player_pos,
            self.main.screen,
            map_data,
            panel
        )

    def reset_MapPlayer(self):
        self.updateMap()
        self.player = Player(self.MazeGen.map_data)
        self.player_pos = [1,1]

    # ------Player
    def updatePlayer(self):
        keys = pygame.key.get_pressed()
        self.player_pos = self.player.update(keys)

    # ------Scene
    def change_scene(self,key):
        self.main.current_scene = self.main.scenes[key]
    
    
if __name__ == "__main__":
    print("start")
    maze = Main()
    maze.main_loop()
