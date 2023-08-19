import pygame
# from dataclasses import dataclass

from Scene.Home_Scene import home
from Scene.Maze_Scene import maze
from main_logic import (
    loopTimer,Timer,eachFrame,YieldListloop, # loop timer
    Maze,Render,                             # render,map
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
            "home" : home(self.screen,self.call_back),
            "maze" : maze(self.screen,self.call_back)
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

                self.current_scene.handle_events(event)


            self.update()

# for main and scene
class call_back:
    def __init__(self,main):
        self.main = main
        
        self.loopTimer1 = loopTimer(1)
        self.timer1 = Timer()
        self.eachFrame_render = eachFrame()
        self.SmoothPos = YieldListloop()
        self.maze = Maze()
        self.render = Render()
        # DynaPlayerMaster'instance is self.player
        self.set_MapSize(21)
        self.reset_MapPlayer()
        self.setMapPanel(None)

    # ------loop timer yield
    # acsess directory

    # ------Map : Gen Render
    
    def updateMap(self):
        self.map,self.solvedMap,self.solution = self.maze.genMapAsolve()
        self.map2Nomal()

    def draw_map(self):
        self.render.draw_map(
            self.main.screen,
            self.mapdata,
            self.mapPanel,
            True
        )  

    def draw_player(self):
        draw_player_pos = self.get_drawPpos()
        self.render.draw_player(
            draw_player_pos,
            self.main.screen,
            self.mapdata,
            self.mapPanel
        )
    
    def setMapPanel(self,palele):
        self.mapPanel = palele
    
    def map2Nomal(self):
        self.mapdata = self.map

    def map2Solution(self):
        self.mapdata = self.solvedMap

    def reset_MapPlayer(self):
        self.updateMap()
        self.player = DynaPlayerMaster(self.map)
        self.cooldown_Ppos = False
        self.SmoothPos.setlist([])
        
    # maze parameter
    def set_MapSize(self,size):
        self.map_size = size
        self.maze.set_MazeSize(size)
        
    def get_MapSize(self):
        return self.map_size

    # ------Player
    def playerMotionManager(self):
        speed = 15
        fps = 60
        
        speed = speed //2

        keys = pygame.key.get_pressed()
        player2pos = self.player.update(keys)
        # (monve) and (not in cooldown_Ppos)
        if (player2pos[0] != False) and (self.cooldown_Ppos == False):
            result = self.player.SmoothFPSmove(player2pos[0],player2pos[1],speed,fps)
            self.SmoothPos.setlist(result)
        else:
            self.player.reset_Ppos()
            
    def get_drawPpos(self):
        result = self.SmoothPos.next()
        if result is not False:
            self.cooldown_Ppos = True
            return result
        else:
            self.cooldown_Ppos = False
            return self.player.playerPos
        
    def is_goal(self):
        index = self.map_size -2
        if self.player.playerPos == [index,index]:
            return True
        
    def mapReset_goal(self):
        if self.is_goal():
            self.reset_MapPlayer()

    # ------Scene
    def change_scene(self,key):
        self.main.current_scene = self.main.scenes[key]
        self.eachFrame_render.remove()
        self.main.current_scene.setUP()
    
    
if __name__ == "__main__":
    print("start")
    maze = Main()
    maze.main_loop()
