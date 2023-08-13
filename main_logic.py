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

                # マップデータがTrueの場合、ブロックを描画
                if map_data[y][x] == True:
                    pygame.draw.rect(screen, pygame.Color("black"), rect)
                else:
                    pygame.draw.rect(screen, pygame.Color("white"), rect)

    def draw_player(self, player_pos, screen, map_data, panel=None):
        
        map_width = len(map_data[0])
        map_height = len(map_data)
        window_width = screen.get_width()
        window_height = screen.get_height()
        parent_pos = (0, 0)

        if panel is not None:
            parent_rect = panel.get_abs_rect()
            parent_pos = parent_rect[0], parent_rect[1]
            window_width = parent_rect[2]
            window_height = parent_rect[3]

        parent_pos = (parent_pos[0] + (window_width % map_width) // 2,
                    parent_pos[1] + (window_height % map_height) // 2)

        tile_width = window_width // map_width
        tile_height = window_height // map_height

        X = parent_pos[0] + player_pos[0] * tile_width
        Y = parent_pos[1] + player_pos[1] * tile_height

        rect = pygame.Rect(X, Y, tile_width, tile_height)  # Rectオブジェクトを作成

        pygame.draw.circle(
            screen, 
            pygame.Color("blue"), 
            rect.center, 
            tile_width // 2
        )



        
# access by call_back
# using class instance to communicate
class MazeGen:
    def __init__(self):
        pass
        
    def map_setup(self, sideL):
        # Create the initial map with outer walls and inner passages
        self.map_data = np.full((sideL, sideL), False, dtype=bool)
        self.map_data[0, :] = True         # Top row
        self.map_data[-1, :] = True        # Bottom row
        self.map_data[:, 0] = True         # Leftmost column
        self.map_data[:, -1] = True        # Rightmost 

        self.map_datas = []

        rang = range(2, sideL - 2, 2)
        self.candidates = [(x, y) for y in rang for x in rang]
        random.shuffle(self.candidates)

    def GenMap(self, sideL):
        self.map_setup(sideL)

        while self.candidates:
            self.MeWall = []
            startP = self.candidates.pop(0)
            self.map_data[startP] = True
            
            running = True
            while running:
                startP = self.wall_extend(startP) 
                if startP is False:
                    running = False
    
    def wall_extend(self, startP):
        directions = np.array([(0, 2), (2, 0), (0, -2), (-2, 0)])
        araund = np.array([(0, 1), (1, 0), (0, -1), (-1, 0)])
        np.random.shuffle(directions)
        re = False
        conect = False

        for direc in directions:          
            pos = (startP + direc)
            pos2 = (startP + direc // 2)

            if not self.is_inside_map(pos):
                continue
            
            if not self.MeWall or tuple(pos) not in self.MeWall:
                if self.map_data[tuple(pos)]:  # Extend to a wall 
                    conect = True
                elif np.any([self.map_data[index] for index in (araund + pos)]):
                    re = True

                self.map_data[pos[0], pos[1]] = True
                self.map_data[pos2[0], pos2[1]] = True
                self.map_datas.append(self.map_data.copy())
                self.MeWall.append(tuple(pos))

                if tuple(pos) in self.candidates:
                    self.candidates.remove(tuple(pos))

                if re or conect:
                    re = False
                else:
                    re = tuple(pos)
                break
        
        return re

    def is_inside_map(self, pos):
        return 0 <= pos[0] < self.map_data.shape[0] and 0 <= pos[1] < self.map_data.shape[1]


class Player:
    def __init__(self, map_data):
        self.playerPos = [1,1]
        self.map_data = map_data

    def update(self, keys):
        pass_playerPos = self.playerPos.copy()
        new_pos = self.playerPos.copy()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            new_pos[0] -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            new_pos[0] += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            new_pos[1] -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            new_pos[1] += 1

        if self.is_in_map(new_pos) and (not self.is_wall(new_pos)):
            self.playerPos = new_pos
        else:
            self.playerPos = pass_playerPos
        return self.playerPos

    def is_in_map(self, new_pos):
        map_width = len(self.map_data[0])
        map_height = len(self.map_data)

        if 0 <= new_pos[0] < map_width and 0 <= new_pos[1] < map_height:
            return not self.map_data[new_pos[1]][new_pos[0]]
        return False

    def is_wall(self, pos):
        x, y = pos
        if self.map_data[y][x]:
            return True
        else:
            return False

