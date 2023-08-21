import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from Scene.BaceScene import BaseScene,UIStore


class maze(BaseScene):
    def __init__(self,screen,call_back):
        self.call_back = call_back
        super().__init__(screen)
        self.manager.get_theme().load_theme('theme/custom.json')
        UI_Store = UIStore(self.manager)

        self.window = screen.get_size()

        #elements
        # HeaderElem is dictionary
        self.HeaderElem = UI_Store.Header()
        self.Game_Screen = UI_Store.Game_Screen()
        
        pad = 15
        map = 900-50-pad*2
        self.panel_map = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((pad,pad), (map,map)),
            starting_height=1,
            manager=self.manager,
            container=self.Game_Screen
        )

        # info_Panel
        infoX = self.window[0]-pad-(map+pad*2)
        self.info_Panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((map+pad*2,pad), (infoX,map)),
            starting_height=1,
            manager=self.manager,

            container=self.Game_Screen
        )
        self.Score_Panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((0, 0), (infoX,500)),
            starting_height=2,
            manager=self.manager,
            object_id=ObjectID("@info_panel"),
            container=self.info_Panel
        )
        
        
        self.label_Scores = self.auto_layout(
            self.Score_Panel, 
            pygame_gui.elements.UILabel, 
            (20,20), 
            (300, 30), 
            10, 
            ["time", "stage", "Avge"], 
            direction="vertical")
        
        
        self.map_buttons = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((0, 500), (infoX,map-500)),
            starting_height=2,
            manager=self.manager,
            object_id=ObjectID("@info_panel"),
            container=self.info_Panel
        )
        
        #info_Panels end

        button_texts = ["Next", "Solution", "Nomal","Button","Button","Button","Button",]
        self.buttons = self.auto_layout(
            self.map_buttons, 
            pygame_gui.elements.UIButton, 
            (20,20), 
            (100, 30), 
            10, 
            button_texts, 
            direction="vertical")
        
    def setUP(self):
        self.call_back.setMapPanel(self.panel_map)
        self.call_back.eachFrame_render.add([
            self.call_back.playerMotionManager,
            self.call_back.draw_map,
            self.call_back.draw_player,
            self.call_back.mapReset_goal,
            self.update_label,
        ])
        
    def update_label(self):
        time = self.call_back.get_time()
        time = round(time,1)
        self.label_Scores[0].set_text(f"time : {time}")
        
        mapStage = self.call_back.get_mapStage()
        self.label_Scores[1].set_text(f"stage : {mapStage}")
        
        if mapStage == 0:
            mapStage = 1
        avge = time / mapStage
        avge = round(avge,1)
        self.label_Scores[2].set_text(f"avge time: {avge}")
        

    def handle_events(self,event):
        
        if event.type == pygame_gui.UI_BUTTON_PRESSED:

            if event.ui_element == self.HeaderElem["logo"]:
                self.call_back.change_scene("home")     

            if event.ui_element == self.buttons[0]:
                self.call_back.reset_MapPlayer()
            
            if event.ui_element == self.buttons[1]:
                self.call_back.map2Solution()
            
            if event.ui_element == self.buttons[2]:
                self.call_back.map2Nomal()





