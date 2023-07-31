import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from Scene.BaceScene import BaseScene,UIStore




class Scene1(BaseScene):
    def __init__(self,screen):
        super().__init__(screen,'theme.json')
        self.UIStore = UIStore(self.manager)

        self.Baselabel1 = self.UIStore.Baselabel1

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
