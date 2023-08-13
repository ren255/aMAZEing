import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from Scene.BaceScene import BaseScene,UIStore




class home(BaseScene):
    def __init__(self,screen):
        super().__init__(screen)
        self.manager.get_theme().load_theme('theme/custom.json')
        UI_Store = UIStore(self.manager,screen)

        self.window = screen.get_size()

        #elements
        self.Header = UI_Store.Header()
        self.Game_Screen = UI_Store.Game_Screen()

        # GUI elements for scene 2
        self.button1 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((20, 750), (600,60)),
            text='start',
            manager=self.manager,
            container=self.Game_Screen
        )
        self.label1 = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, 700), (200, 30)),
            text='LEVEL 1',
            manager=self.manager,
            container=self.Game_Screen
        )


    def handle_events(self,event,call_back):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.button1:
                call_back.change_scene("maze")

