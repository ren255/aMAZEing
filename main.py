import pygame
import pygame_gui
# from dataclasses import dataclass

from Scene.scene2 import Scene2
from main_logic import MazeGen,Render,Timer



class Main:
    def __init__(self):
        window = (1400,900)
        pygame.init()
        #from main_logic.py
        self.render = Render()

        self.call_back = call_back(self)

        self.screen = pygame.display.set_mode(window)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Maze Game")

        self.scenes = [Scene2(self.screen)]
        self.current_scene = self.scenes[0]

        self.call_back.updateMap()
        self.map_index = 0


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

        self.render.draw_map(
            self.screen,
            self.map,
            self.scenes[0].panel_map)

        pygame.display.flip()
        self.clock.tick(60)

    def main_loop(self):
        Timer1 = Timer(1)
        Timer1.add(self.call_back.updateMap)

        while True:

            for event in pygame.event.get():
                if self.quit(event):
                    pygame.quit()
                    return
                
                """ not working
                self.current_scene.handle_events(event,self.call_back)

                if event.type == pygame.USEREVENT:
                    if event.type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == Scene2.buttons[0]:
                            self.call_back.updateMap()
                            print("update_map")
                        print("Button", event.ui_element)
                    print(event.type,pygame_gui.UI_BUTTON_PRESSED)32866 32867
                """
            Timer1.check()
            self.update()

class call_back:
    def __init__(self,main):
        self.main = main
        self.MazeGen = MazeGen()

    def updateMap(self):
        self.MazeGen.GenMap(21)
        self.main.map = self.MazeGen.map_data
        

if __name__ == "__main__":
    print("start")
    maze = Main()
    maze.main_loop()