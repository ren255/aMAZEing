import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from Scene.BaceScene import BaseScene,UIStore




class Scene1(BaseScene):
    def __init__(self,screen):
        super().__init__(screen)
        self.manager.get_theme().load_theme('theme/custom.json')
        UI_Store = UIStore(self.manager,screen)

        self.window = screen.get_size()

        #elements
        # self.Header = UI_Store.Header()
        self.Game_Screen = UI_Store.Game_Screen()

        # GUI elements for scene 2
        self.button1 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((150, 100), (100, 40)),
            text='to scene1',
            manager=self.manager
        
        )
        self.label1 = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((100, 30), (200, 30)),
            text='this is scene2',
            manager=self.manager
        )


    def handle_events(self,event,call_back):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            print("Button",event.ui_element)
