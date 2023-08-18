import pygame
import numpy as np
import time
import random


#------------------------------------------------------------yield,Timer
# access from Main
# use for loop process
class loopTimer:
    def __init__(self,delay,processes = None):
        self.delay = delay
        self.processFuncs = processes if processes is not None else []
        self.timer_iterator = self.loop()

    def change_delay(self,delay):
        self.delay = delay

    def add(self,process):
        if type(process) is list:
            for i in process:
                self.processFuncs.append(i)
        else:
            self.processFuncs.append(process)
        self.processFuncs = list(set(self.processFuncs))

    def remove(self,process):
        if process in self.processFuncs:
            self.processFuncs.remove(process)
        if process == None:
            self.processFuncs = []

    def check(self):
        next(self.timer_iterator)

    def loop(self):
        start_time = time.time()
        last_print_time = start_time

        while True:
            current_time = time.time()
            if current_time - last_print_time >= self.delay:
                last_print_time = current_time
                for func in self.processFuncs:
                    func()
            yield

class eachFrame:
    def __init__(self,processes = None):
        self.processFuncs = processes if processes is not None else []

    def add(self, process):
        if isinstance(process, list):
            for i in process:
                if i not in self.processFuncs:
                    self.processFuncs.append(i)
        else:
            if process not in self.processFuncs:
                self.processFuncs.append(process)

    def remove(self,process = None):
        if process in self.processFuncs:
            self.processFuncs.remove(process)
        if process == None:
            self.processFuncs = []

    def process(self):
        for i in self.processFuncs:
            i()


class Timer:
    def set_timer(self, duration):
        self.start_time = time.time()
        self.duration = duration

    def check(self):
        if self.start_time is None or self.duration is None:
            return False

        current_time = time.time()
        elapsed_time = current_time - self.start_time
        if elapsed_time >= self.duration:
            return True
        else:
            return False

class YieldListloop:
    def setlist(self, input_list):
        self.input_list = input_list
        self.iterator = self.loop()

    def loop(self):
        for element in self.input_list:
            yield element

    def next(self):
        try:
            next_element = next(self.iterator)
            return next_element
        except StopIteration:
            return False



#------------------------------------------------------------map
# access from Main
# just render map to screen
class Render:
    def draw_map(self, screen, map_data, panel=None,goal=False):
        map_data = map_data.tolist()
        if goal:
            map_data[-2][-2] = 2
        
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
                elif map_data[y][x] == False:
                    pygame.draw.rect(screen, pygame.Color("white"), rect)
                elif map_data[y][x] == 2:
                    pygame.draw.rect(screen, pygame.Color("green"), rect)

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

        X = player_pos[0] * tile_width
        Y = player_pos[1] * tile_height

        X = parent_pos[0] + X
        Y = parent_pos[1] + Y

        rect = pygame.Rect(X, Y, tile_width, tile_height)  # Rectオブジェクトを作成

        pygame.draw.circle(
            screen, 
            pygame.Color("blue"), 
            rect.center, 
            (tile_width-2) // 2
        )



        
# access by call_back

class Maze:
    def __init__(self,sideL):
            self.Iwall = []
            
            self.MazeGen = self.MazeGenerator(sideL)
            self.solveMaze = self.SolveMaze(sideL)
            
    def genMapAsolve(self):
        map = self.GenerateMaze()
        solution,solvedMap = self.solveM(map)
        return map,solvedMap,solution
    
    def GenerateMaze(self):
        map = self.MazeGen.GenMap()
        return map
    
    def solveM(self,map):
        solution = self.solveMaze.solve(map)
        solvedMap = self.wall2map(map,solution)
        return solution,solvedMap
    
    def wall2map(self,map,wall):
        map = map.astype(int)
        for pos in wall:
            map[pos[1],pos[0]] = 2
        return map
    
    # maze generator
    class MazeGenerator:
        def __init__(self,sideL):
            self.sideL = sideL
            self.Iwall = []
        
        def GenMap(self):
            map,maps,candidates = self.SetupMap(self.sideL)
            
            # loop through the candidate
            while len(candidates):
                # store wall pos
                self.Iwall = []
                startPos = candidates.pop(0)
                self.Iwall.append(startPos)
                
                available_wall = True
                while available_wall:
                    available_wall = False
                    running = True
                    NextPos = startPos
                    while running:
                        NextPos = self.wall_extend(map,NextPos)
                        
                        if NextPos is None:
                            # stack wall reset
                            running = False
                            available_wall = True
                            self.Iwall = []
                            
                        elif NextPos is False:
                            running = False
                            
                map,candidates = self.Iwall2map(map,candidates)
                
            return map
        
        # extend the wall for two blocks
        def wall_extend(self,map,startPos):
            directions = np.array([(0,2),(2,0),(0,-2),(-2,0)])
            np.random.shuffle(directions)
            connect = False
            
            for direc in directions:
                
                pos = (startPos + direc)
                pos2 = (startPos + direc // 2)
                
                if self.outOFbounds(pos):
                    continue
                
                if not any(np.all(pos == index) for index in self.Iwall):
                    
                    self.Iwall.append(tuple(pos))
                    self.Iwall.append(tuple(pos2))
                    
                    # check pos is connect to wall
                    try:
                        if np.any([map[index[0],index[1]] for index in self.Iwall]):
                            connect = True
                    except IndexError:
                        print("map size mast be odd number")
                        
                    if connect:
                        return False
                    else:
                        return tuple(pos)
                    
                    
                    
        # convert Iwall to map
        def Iwall2map(self,map,candidates):
            for pos in self.Iwall:
                if pos in candidates:
                    candidates.remove(pos)
                    pass
                map[pos[0],pos[1]] = True
                
            self.Iwall = []
            return map,candidates
            
        def outOFbounds(self,pos):
            isINx = 0 <= pos[0] < self.sideL
            isINy = 0 <= pos[1] < self.sideL
            return not (isINx or isINy)
            
        @staticmethod
        def SetupMap(Sidelength):
            # Create an initial map with walls
            map = np.full((Sidelength,Sidelength),False,dtype=bool)
            map[0,:] = True    #Top row
            map[:,0] = True    #Left column
            map[-1,:] = True   #Bottom row
            map[:,-1] = True   #Right column
            
            maps = []
            
            Range = range(2,Sidelength -2 ,2)
            candidates = [(x,y) for x in Range for y in Range]
            random.shuffle(candidates)
            
            return map,maps,candidates
        
    class SolveMaze:
        def __init__(self,Sidelength):
            self.sideL = Sidelength
            
        def solve(self,map):
            self.map = map
            self.start = np.array([1, 1])
            self.goal = np.array([self.sideL - 2, self.sideL - 2])
        
            path = []
            self.dfs(self.start, path)
            return self.solution
        
        def dfs(self, pos, path):
            if np.array_equal(pos, self.goal):
                path.append(pos)
                self.update_solution(path)
                return True
            
            path.append(pos)

            directions = self.get_destination(pos)
            
            for new_pos in directions:
                if any(np.array_equal(new_pos, pos) for pos in path):
                    continue
                if self.dfs(new_pos, path):
                    return True
            
            path.pop()
            return False
        
        def update_solution(self,path):
            self.solution = []
            Ppos = self.start
            for pos in path:
                x1, y1 = Ppos
                x2, y2 = pos
                if abs(x1 - x2) == 2 and y1 == y2:
                    self.solution.append(((x1 + x2) // 2, y1))
                elif x1 == x2 and abs(y1 - y2) == 2:
                    self.solution.append((x1, (y1 + y2) // 2))
                self.solution.append(pos)
                Ppos = pos
        
        def get_destination(self,pos):
            directions = np.array([(0,1),(1,0),(0,-1),(-1,0)])
            np.random.shuffle(directions)
            destinations = []
            for direc in directions:
                goPos = pos + direc
                goto = self.map[goPos[1],goPos[0]]
                if  goto == False:
                    destinations.append(goPos + direc)
            return destinations
        
        
#------------------------------------------------------------player
class DynaPlayerMaster:
    def __init__(self, map_data):
        self.playerPos = [1,1]
        self.map_data = map_data

    def update(self, keys):
        def is_in_map(new_pos):
            map_width = len(self.map_data[0])
            map_height = len(self.map_data)

            if 0 <= new_pos[0] < map_width and 0 <= new_pos[1] < map_height:
                return not self.map_data[new_pos[1]][new_pos[0]]
            return False

        def is_wall( pos):
            x, y = pos
            if self.map_data[y][x]:
                return True
            else:
                return False
            
        self.pass_playerPos = self.playerPos.copy()
        new_pos = self.playerPos.copy()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            new_pos[0] += 1

        elif keys[pygame.K_LEFT]  or keys[pygame.K_a]:
            new_pos[0] -= 1

        elif keys[pygame.K_DOWN]  or keys[pygame.K_s]:
            new_pos[1] += 1

        elif keys[pygame.K_UP]    or keys[pygame.K_w]:
            new_pos[1] -= 1
   
        

        if (is_in_map(new_pos)) and (not is_wall(new_pos)) and (new_pos != self.pass_playerPos):
            self.playerPos = new_pos
            return self.pass_playerPos,self.playerPos
        else:
            return False,False
        
    def reset_Ppos(self):
        self.playerPos = self.pass_playerPos
        
    @staticmethod
    def SmoothFPSmove(start, end,speed, fps):
        def lerp(start, end, t):
            return (1 - t) * start + t * end
        
        def lerp_loop(start, end, n):
            result = []
            for i in range(n + 1):
                t = i / n
                smoothed_value = lerp(start, end, t)
                smoothed_value = round(smoothed_value, 2)
                result.append(smoothed_value)
            result.pop(0)
            return result
        
        def smoothFPSmove(start, end, speed, fps):
            fpsS = 1 / fps
            speedS = 1 / speed
            n = int(speedS / fpsS)
            
            if type(start) is int:
                result = lerp_loop(start, end, n)
            else:
                X = lerp_loop(start[0], end[0], n)
                Y = lerp_loop(start[1], end[1], n)
                result = [pos for pos in zip(X, Y)]
            return result
        
        result = smoothFPSmove(start, end, speed, fps)
        return result






