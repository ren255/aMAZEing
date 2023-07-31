import pygame
import pygame_gui
from pygame_gui.core import ObjectID

class BaseScene:

    def __init__(self,screen,theme = 'theme/theme.json'):
        self.screen = (screen.get_width(),screen.get_height())
        self.manager = pygame_gui.UIManager(self.screen,theme)

    def process_events(self, event):
        self.manager.process_events(event)

    def update(self, dt):
        self.manager.update(dt)

    def draw(self, surface):
        self.manager.draw_ui(surface)

    @staticmethod
    def auto_layout(panel, element, start_point, size, spacing, text_list, direction="vertical"):
        # panel: 要素が配置されるUIPanelオブジェクト
        # element: 配置されるUI要素のクラス (例: Button, Labelなど)
        # start_point: 自動配置が始まる座標 (x, y) 
        # size: 各UI要素のサイズ (幅, 高さ)
        # spacing: UI要素間の間隔
        # text_list: 各UI要素に表示されるテキストのリスト
        # direction: 配置の方向 ("vertical" または "horizontal")

        manager = panel.ui_manager 
        elements = []
        num_elements = len(text_list)

        for i in range(num_elements):
            if direction == "vertical":
                element_rect = pygame.Rect(start_point[0], start_point[1] + (size[1] + spacing) * i, size[0], size[1])
            elif direction == "horizontal":
                element_rect = pygame.Rect(start_point[0] + (size[0] + spacing) * i, start_point[1], size[0], size[1])
            else:
                raise ValueError("Invalid direction parameter. Use 'vertical' or 'horizontal'.")

            element_obj = element(
                relative_rect=element_rect, 
                text=text_list[i], 
                manager=manager, 
                container=panel)
            elements.append(element_obj)

        return elements

class UIStore():
    def __init__(self,manager):
        self.Header = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((0,0), (1400,50)),
            starting_height=1,
            manager=manager,
            object_id=ObjectID("@info_panel"),
        )
        self.Game_Screen = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((0,50), (1400,850)),
            starting_height=0,
            manager=manager,
        )