import pygame, pygame_gui as pg_gui
from src.Elements.element import ParentElement, Element, TextElement


class Menu(ParentElement):

    def __init__(self, screen: pygame.Surface, elements: list):
        super().__init__(screen, './assets/json/graffics/game-menu/style.json')
        self.elements = elements
        self.get_elements()

    def get_elements(self):
        self.elems = []
        for elem in self.elements:
            classRef = elem['name']
            rect = elem['rect']
            text = elem['text']
            object_id = elem['object_id']
            container = elem['container']
            if text == '':
                self.elems.append(
                    Element(classRef, rect, self.ui_manager, object_id, container).UI
                )
            else:
                self.elems.append(
                    TextElement(classRef, rect, text, self.ui_manager, object_id, container ).UI
                )


