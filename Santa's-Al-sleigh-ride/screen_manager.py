import pygame
from constants import Consts
import threading
import sys
import time
from map import Map
from state import State


class Display:

    display_thread: threading.Thread

    def __init__(self, map_object: Map):
        w, h = map_object.w, map_object.h
        self.map_array = map_object.map
        self.w = w
        self.h = h
        self.points = map_object.points
        self.marks = []                      # Used in debugging
        
        # PyGame part
        pygame.init()
        sw, sh = Consts.SCREEN_WIDTH, Consts.SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((sw, sh))
        self.screen.fill(Consts.BACKGROUND)

        # Setting cell size and other sizes
        if w / h > sw / sh:
            rect_width = sw - 2 * Consts.SCREEN_MARGIN_SIZE
            cell_size = int(rect_width / w)
            rect_height = cell_size * h
        else:
            rect_height = sh - 2 * Consts.SCREEN_MARGIN_SIZE
            cell_size = int(rect_height / h)
            rect_width = cell_size * w
        self.cell_size = cell_size
        self.rect_width = rect_width
        self.rect_height = rect_height
        # self.step_count_font = pygame.font.Font(None, 36)
        # Threading part
        self.display_thread = None
        self.stop_event = threading.Event()

        # Loading images
        self.GIFT_IMAGE = pygame.image.load(Consts.GIFT_IMAGE)
        self.GIFT_IMAGE = pygame.transform.scale(self.GIFT_IMAGE, (cell_size, cell_size))
        self.santa_image = pygame.image.load(Consts.santa_IMAGE)
        self.santa_image = pygame.transform.scale(self.santa_image, (cell_size, cell_size))
        self.x_image = pygame.image.load(Consts.X_IMAGE)
        self.x_image = pygame.transform.scale(self.x_image, (cell_size, cell_size))
        self.mark_image = pygame.image.load(Consts.MARK_IMAGE)
        self.mark_image = pygame.transform.scale(self.mark_image, (cell_size, cell_size))
        self.tree_image = pygame.image.load(Consts.TREE)
        self.tree_image = pygame.transform.scale(self.tree_image, (cell_size, cell_size))

        self.draw_cells()
        pygame.display.update()

    def update(self, state: State, save=False):
        self.draw_cells()
        santa_y, santa_x = state.santa
        self.draw_in_position(santa_y, santa_x, self.santa_image)
        for gift in state.gifts:
            self.draw_in_position(gift[0], gift[1], self.GIFT_IMAGE)
        for mark in self.marks:
            self.draw_in_position(mark[0], mark[1], self.mark_image)
        pygame.display.update()

    def draw_cells(self):
        sw, sh = Consts.SCREEN_WIDTH, Consts.SCREEN_HEIGHT
        w, h = self.w, self.h
        rect_width, rect_height = self.rect_width, self.rect_height
        cell_size = self.cell_size

        # Drawing cells
        init_y = (sh - rect_height) / 2
        init_x = (sw - rect_width) / 2
        for j in range(h):
            for i in range(w):
                x = init_x + i * cell_size
                y = init_y + j * cell_size
                if self.map_array[j][i] == 'x':
                    color = Consts.CELL_WHITE
                else:
                    color = Display.darker(Consts.CELL_WHITE, int(self.map_array[j][i]))
                    
                # Drawing Rectangles
                pygame.draw.rect(self.screen, color, (x, y, cell_size, cell_size), 0)
                pygame.draw.rect(self.screen, (0, 0, 0), (x, y, cell_size, cell_size), 1)

        for j in range(h):
            for i in range(w):
                x = init_x + i * cell_size
                y = init_y + j * cell_size
                if self.map_array[j][i] == 'x':
                    self.draw_in_position(j, i, self.tree_image)
        # Drawing X Points
        for p in self.points:
            self.draw_in_position(p[0], p[1], self.x_image)
        

    def draw_in_position(self, y: int, x: int, image):
        init_y = (Consts.SCREEN_HEIGHT - self.rect_height) / 2
        init_x = (Consts.SCREEN_WIDTH - self.rect_width) / 2
        pos_x = init_x + x * self.cell_size
        pos_y = init_y + y * self.cell_size
        self.screen.blit(image, (pos_x, pos_y))

    def begin_display(self,l):
        def infinite_loop(l):
            """ This is the function which includes the infinite loop for pygame pumping. """
            while l!=0:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        sys.exit(0)
                pygame.display.update()
                pygame.time.wait(int(1000/Consts.FPS))
                l= l-1
        # Starting thread
        self.display_thread = threading.Thread(name='Display', target=infinite_loop, args = (l,))
        self.display_thread.setDaemon(False)
        self.display_thread.start()
        # step_count_text = f"Time taken: "
        # step_count_surface = self.step_count_font.render(step_count_text, True, (255, 255, 255))
        # step_count_rect = step_count_surface.get_rect()
        # step_count_rect.topleft = (self.rect_width -200, 10)  # Adjust the position as needed
        # self.screen.blit(step_count_surface, step_count_rect)


    @staticmethod
    def darker(color: tuple[int, int, int], radius: int):
        r = color[0] - (radius - 1) * 30
        g = color[1] - (radius - 1) * 30
        b = color[2] - (radius - 1) * 30
        r = 0 if r < 0 else r
        g = 0 if g < 0 else g
        b = 0 if b < 0 else b
        return r, g, b
