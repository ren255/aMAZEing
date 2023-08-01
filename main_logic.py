import pygame
import numpy as np
import time
import random



# access from Main
# use for loop process
class Timer:
    def __init__(self,delay,processes = None):
        self.delay = delay
        self.processFuncs = processes if processes is not None else []
        self.timer_iterator = self.seconds()

    def change_delay(self,delay):
        self.delay = delay

    def add(self,process):
        self.processFuncs.append(process)
        self.processFuncs = list(set(self.processFuncs))

    def remove(self,process):
        if process in self.processFuncs:
            self.processFuncs.remove(process)

    def check(self):
        next(self.timer_iterator)

    def seconds(self):
        start_time = time.time()
        last_print_time = start_time

        while True:
            current_time = time.time()
            if current_time - last_print_time >= self.delay:
                last_print_time = current_time
                for i in self.processFuncs:
                    i()
            yield


# access from Main
# just render map to screen
class Render:
    def draw_map(self, screen, map_data, panel=None):
        # print(map_data)
        map_width = len(map_data[0])
        map_height = len(map_data)
        window_width = screen.get_width()
        window_height = screen.get_height()
        parent_pos = (0, 0)

        if panel is not None:
            parent_rect = panel.get_abs_rect()
            parent_pos = parent_rect[0],parent_rect[1]
            window_width = parent_rect[2]
            window_height = parent_rect[3]

        parent_pos = (parent_pos[0] + (window_width % map_width) // 2,
                    parent_pos[1] + (window_height % map_height) // 2)

        tile_width = window_width // map_width
        tile_height = window_height // map_height

        for y in range(map_height):
            for x in range(map_width):
                X = parent_pos[0] + x * tile_width
                Y = parent_pos[1] + y * tile_height
                rect = (X, Y, tile_width, tile_height)

                # マップデータが1の場合、ブロックを壁として描画
                if map_data[y][x] == 1:
                    pygame.draw.rect(screen, Color.black, rect)
                elif map_data[y][x] == 2:
                    pygame.draw.rect(screen, Color.orange, rect)
                else:
                    pygame.draw.rect(screen, Color.white, rect)

        
# access by call_back
# using class instance to communicate
class MazeGen:
    def __init__(self):
        pass
        
    def map_setup(self,sideL):
        
        # Create the initial map with outer walls and inner passages
        self.map_data = np.zeros((sideL,sideL), dtype=int)
        self.map_data[0, :] = 1         # Top row
        self.map_data[-1, :] = 1        # Bottom row
        self.map_data[:, 0] = 1         # Leftmost column
        self.map_data[:, -1] = 1        # Rightmost 

        self.map_datas = []

        rang = range(2, sideL - 2, 2)
        self.candidates = [(x, y)for y in rang for x in rang]
        #print(self.candidates)
        
        random.shuffle(self.candidates)

    def GenMap(self, sideL):
        self.map_setup(sideL)

        while self.candidates:            
            self.MeWall = []
            startP = self.candidates.pop(0)
            self.map_data[startP] = 1
            
            running = True
            while running:
                # print(self.map_data)
                startP = self.wall_extend(startP) 
                if startP == False:
                    # print("---------------wall is made") 
                    running = False
                                      
                 
    
    def wall_extend(self,startP):
        # print("wall_extend------S")
        
        directions = np.array([(0, 2), (2, 0), (0, -2), (-2, 0)])
        araund = np.array([(0,1), (1, 0), (0, -1), (-1, 0)])
        np.random.shuffle(directions)
        re = False
        conect = False

        for direc in directions:          
            pos =(startP + direc)
            # print("from",startP,"to",pos)
            pos2 = (startP + direc // 2)

            if tuple(pos) not in self.MeWall:
                # print("place was ",self.map_data[tuple(pos)])
                if self.map_data[tuple(pos)]:#extend to wall 
                    conect = True
                    # print("and set")
                # araund of extend is wall
                elif (np.any([self.map_data[index] for index in (araund + pos)] == 1)):
                    re = True
                    # print("and not set")

                self.map_data[pos[0],pos[1]] = 1
                self.map_data[pos2[0],pos2[1]] = 1
                self.map_datas.append(self.map_data.copy())
                self.MeWall.append(tuple(pos))

                if tuple(pos) in self.candidates:
                    self.candidates.remove(tuple(pos))
                    #print(pos)

                if re or conect == True:
                    re = False
                else:
                    re = tuple(pos)
                break
        # print("re",re)
        # print("wall_extend------E")
        return re


#
class Color:
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    cyan = (0, 255, 255)
    magenta = (255, 0, 255)
    white = (255, 255, 255)
    black = (0, 0, 0)
    gray = (128, 128, 128)
    orange = (255, 165, 0)
    purple = (128, 0, 128)
    brown = (165, 42, 42)
    pink = (255, 192, 203)