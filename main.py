import pygame
import pygame_gui
# from dataclasses import dataclass

from Scene.Home_Scene import home
from Scene.Maze_Scene import maze
from main_logic import (
    loopTimer,Timer,eachFrame,YieldListloop, # loop timer
    MazeGen,Render,                          # render,map
    DynaPlayerMaster)                        # player master


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
        self.call_back.change_scene("home")

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

        self.call_back.eachFrame_render.process()            

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

        self.loopTimer1 = loopTimer(1)
        self.timer1 = Timer()
        self.eachFrame_render = eachFrame()
        self.SmoothPos = YieldListloop()
        self.MazeGen = MazeGen()
        self.render = Render()
        # DynaPlayerMaster'instance is self.player   
        self.reset_MapPlayer() 

        def print_message():
            print("This is cooldown_Ppos's")      

        self.Timer02 = loopTimer(1,[print_message])            

    # ------loop timer yield
    # acsess directory

    # ------Map : Gen Render
    def updateMap(self):
        self.MazeGen.GenMap(21)
        self.map = self.MazeGen.map_data

    def draw_map(self,map_data, panel=None):
        self.render.draw_map(
            self.main.screen,
            map_data,
            panel
        )  

    def draw_player(self,map_data, panel=None):
        draw_player_pos = self.get_drawPpos()
        self.render.draw_player(
            draw_player_pos,
            self.main.screen,
            map_data,
            panel
        )

    def renderAll(self):
        self.Timer02.check()

        self.draw_map(
            self.map,
            self.main.current_scene.panel_map
        )
        
        self.draw_player(
            self.map,
            self.main.current_scene.panel_map
        )


    def reset_MapPlayer(self):
        self.updateMap()
        self.player = DynaPlayerMaster(self.MazeGen.map_data)
        self.cooldown_Ppos = False
        self.SmoothPos.setlist([])

    # ------Player
    def playerMotionManager(self):
        keys = pygame.key.get_pressed()
        player2pos = self.player.update(keys)
        # (monve) and (not in cooldown_Ppos)
        if (player2pos[0] != False) and (self.cooldown_Ppos == False):
            result = self.player.SmoothFPSmove(player2pos[0],player2pos[1])
            self.SmoothPos.setlist(result)
            # print(len(result))
            

    def get_drawPpos(self):
        result = self.SmoothPos.next()
        Pcooldown = self.cooldown_Ppos
        if result is not False:
            self.cooldown_Ppos = True
            if Pcooldown != self.cooldown_Ppos:
                print("cooldown_Ppos is ",Pcooldown, self.cooldown_Ppos)
            return result
        else:
            self.cooldown_Ppos = False
            return self.player.playerPos

    # ------Scene
    def change_scene(self,key):
        self.main.current_scene = self.main.scenes[key]
        self.eachFrame_render.remove()
        self.main.current_scene.setUP(self)
    
    
if __name__ == "__main__":
    print("start")
    maze = Main()
    maze.main_loop()
