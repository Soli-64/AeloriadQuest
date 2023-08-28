import pygame, pygame_gui as pg_gui
from pygame_gui.core import ObjectID
import src.Utils.pygame_functions as f_pg


class ParentElement:

    def __init__(self, _screen: pygame.Surface, _stylesheet_path: str):
        self.screen = _screen
        self.set_manager(_screen, _stylesheet_path)

    def set_manager(self, _screen, _stylesheet_path):
        self.ui_manager = pg_gui.UIManager(_screen.get_size(), _stylesheet_path)

    def update(self, _time_delta):
        self.ui_manager.update(_time_delta)

    def draw(self):
        self.ui_manager.draw_ui(self.screen)


class Element:

    def __init__(self, name, rect, ui_manager, object_id, container):
        self.name = name
        self.rect = pygame.Rect(rect)
        self.ui_manager = ui_manager
        self.object_id = object_id
        self.container = container
        self.UI = eval(f'pg_gui.elements.UI{name}('
                       f'relative_rect=pygame.Rect({rect[0]}, {rect[1]}), '
                       f'manager=self.ui_manager, '
                       f'object_id="{object_id}",'
                       f'container=self.container)')


class TextElement:
    def __init__(self, name, rect, text, ui_manager, object_id, container):
        self.name = name
        self.rect = pygame.Rect(rect)
        self.text = text
        self.ui_manager = ui_manager
        self.object_id = object_id
        self.container = container
        self.UI = eval(f'pg_gui.elements.UI{name}('
                       f'relative_rect=pygame.Rect({rect[0]}, {rect[1]}), '
                       f'text="{text}", '
                       f'manager=self.ui_manager, '
                       f'object_id="{object_id}",'
                       f'container=self.container)')

class ImageElement:

    def __init__(self, rect, img, ui_manager, object_id, container):
        self.name = 'Image'
        self.rect = pygame.Rect(rect[0], rect[1])
        self.image = img
        self.ui_manager = ui_manager
        self.object_id = object_id
        self.container = container
        self.UI = pg_gui.elements.UIImage(
                                        relative_rect=self.rect,
                                        image_surface=self.image,
                                        manager=self.ui_manager,
                                        object_id=self.object_id,
                                        container=self.container
                                        )

class Button:

    def __init__(self, rect, text, ui_manager, object_id, container):
        self.name = 'Button'
        self.rect = pygame.Rect(rect)
        self.text = text
        self.ui_manager = ui_manager
        self.object_id = object_id
        self.container = container
        #self.func = func
        self.UI = pg_gui.elements.UIButton(
                                           relative_rect=pygame.Rect(rect[0], rect[1]),
                                           text=self.text,
                                           manager=self.ui_manager,
                                           object_id=self.object_id,
                                           container=self.container
                                           )


class IndexButton(Button):

    def __init__(self, _rect, _text, _ui_manager, _object_id, _container, _inventory):
        super().__init__(_rect, _text, _ui_manager, _object_id, _container)
        self.inventory = _inventory

    def execute(self):
        self.inventory.set_index(self)


class EventButton(Button):

    def __init__(self, _rect, _text, _ui_manager, _object_id, _container, _func):
        super().__init__(_rect, _text, _ui_manager, _object_id, _container)
        self.func = _func
    def execute(self): self.func()



class Ids:

    def __init__(self, _class_id, _object_id):
        self.all = ObjectID(class_id=_class_id, object_id=_object_id)

class ScrollZone:

    def __init__(self, _rect, _visible_percentage, _ui_manager, _object_id, _container):
        self.rect = pygame.Rect(_rect[0], _rect[1])
        self.visible_percentage = _visible_percentage
        self.ui_manager = _ui_manager
        self.object_id = _object_id
        self.container = _container
        self.UI = pg_gui.elements.UIVerticalScrollBar(
                                                  relative_rect=self.rect,
                                                  visible_percentage=self.visible_percentage,
                                                  manager=self.ui_manager,
                                                  container=self.container,
                                                  object_id=self.object_id
                                                  )
