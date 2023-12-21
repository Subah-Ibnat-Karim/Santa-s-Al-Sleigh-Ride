import os
class Consts:

    # Map
    MAP_FILE = 'maps/map7.txt'
    MAP_PATH = './maps/map'
    Num= input("The options for the size of the area of the neighbourhood to distribute gifts:\n0) 5x7 map_size\n1) 5x5 map_size\n2) 6x6 map_size\n3) 7x7 map_size\n4) 8x8 map_size\n5) 9x9 map_size\n6) 10x10 map_size\n7) 10x7 map_size\n Choose one of the following option (0-7) to choose the area of the neighbourhood to run the Santa's Al Sleigh Ride:\n")
    MAP_FILE='./maps/map'+Num+'.txt'
    # IDS
    FIRST_K = 1
    LAST_K = 50

    # PyGame Window Features
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480
    BACKGROUND = 198, 163, 138
    SCREEN_MARGIN_SIZE = 40
    CELL_COLOR = 131, 60, 11
    BLOCK_COLOR = 32, 32, 32
    CELL_WHITE = 230, 221, 220
    GIFT_IMAGE = './images/gift.png'
    santa_IMAGE = './images/santa-claus.png'
    X_IMAGE = './images/cabin.png'
    MARK_IMAGE = './images/mark.png'
    TREE = './images/tree.png'

    # Times
    STEP_TIME = 0.4
    FPS = 24
