import pygame as pg
# SETTINGS

# CUSTOM EVENTS

SLASH_ANIMATION_TIMER= pg.USEREVENT + 1
# pg.USEREVENT + 2 is UI_BUTTON_PRESSED
RESET_TRADERS_STUFF= pg.USEREVENT + 12

# SCREEN POINTS:

def COIN_BOX(vw: int) -> list[float]: return [vw - 270, 10]

def INVENTORY() -> list[float]: return [220, 50]

def WEAPON_CASE(vw: int, vh: int) -> list[float]: return [vw - 200, vh - 200]

def SELECTED_WEAPON(vw: int, vh: int) -> tuple[int, int]: return vw - 185, vh - 185

def MUNITION_NUMBER(vw: int, vh: int) -> tuple[int, int]: return vw - 115, vh - 45

def MARKET(vw: int, vh: int) -> list[float]: return [vw / 8, vh / 20]
