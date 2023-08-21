import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from Scene.BaceScene import BaseScene,UIStore




class home(BaseScene):
    def __init__(self,screen,call_back):
        self.call_back = call_back
        super().__init__(screen)
        self.manager.get_theme().load_theme('theme/custom.json')
        UI_Store = UIStore(self.manager)

        self.window = screen.get_size()

        #elements
        self.Header = UI_Store.Header()
        self.Game_Screen = UI_Store.Game_Screen()
        
        self.panel_parameter = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((30,490), (700,350)),
            manager=self.manager,
            object_id=ObjectID("@info_panel"),
            container=self.Game_Screen
        )

        # GUI elements for scene 2
        self.Button_start = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((20, 280), (660,60)),
            text='start',
            manager=self.manager,
            container=self.panel_parameter
        )
        
        self.text_mapSize = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, 20), (300, 30)),
            text='map size : 21',
            manager=self.manager,
            container=self.panel_parameter
        )
        self.slider_mapSize = pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(
            relative_rect=pygame.Rect((320, 20), (300, 30)),
            start_value=21,  # 初期値
            value_range=(5,195),  # 値の範囲
            manager=self.manager,
            container=self.panel_parameter
        )

    def setUP(self):
        self.call_back.eachFrame_render.add([
            self.update_parameter,
        ])

    def update_parameter(self):
        map_size = self.slider_mapSize.get_current_value()
        if map_size % 2 == 0:
            map_size += 1
        self.call_back.set_MapSize(map_size)
        self.text_mapSize.set_text(f'map size : {map_size}')

    def handle_events(self,event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            
            if event.ui_element == self.Button_start:
                self.call_back.change_scene("maze")
                self.call_back.reset_MapPlayer()
                self.call_back.reset_mapStage()
                self.call_back.start_stopwatch()

