import pygame
import sys
import time
from constants import Consts

class PygameInputHandler:
    flag = True
    grids = ["5x7", "5x5", "6x6", "7x7", "8x8", "9x9", "10x10", "10x7"]
    def __init__(self):
        pygame.init()
        self.screen_size = (600, 125)
        self.screen = pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)
        pygame.display.set_caption("Grid Example")
        self.clock = pygame.time.Clock()


        self.grid_size = (1,len(self.grids))
        self.box_size = self.screen_size[0] // self.grid_size[1]
        self.grid = [self.grids]  # Just one row with all items

        # Background color
        self.background_color = Consts.BACKGROUND
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(self.background_color)

        # Heading font and text
        self.heading_font = pygame.font.Font(None, 36)
        self.heading_text = self.heading_font.render("Select the map size", True, (0, 0, 0), self.background_color)
        self.heading_text_rect = self.heading_text.get_rect(center=(self.screen_size[0] // 2, 10))

        # Selected number
        self.selected_number = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_mouse_click(event.pos)
            elif event.type == pygame.VIDEORESIZE:
                self.screen_size = event.size
                self.screen = pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)
                self.box_size = self.screen_size[0] // self.grid_size[1]

    def handle_mouse_click(self, pos):
        row = (pos[1] - 30) // self.box_size
        col = pos[0] // self.box_size
        if 0 <= row < self.grid_size[0] and 0 <= col < self.grid_size[1]:
            self.selected_number = self.grids.index(self.grid[row][col])
            print(f"Selected number: {self.selected_number}")
            time.sleep(1)
            self.flag = False

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def draw_grid(self):
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                square_rect = pygame.Rect(j * self.box_size, i * self.box_size + 30, self.box_size, self.box_size)
                pygame.draw.rect(self.background, Consts.CELL_WHITE, square_rect)
                pygame.draw.rect(self.background, (0, 0, 0), square_rect, 2)

                font = pygame.font.Font(None, 24)
                text = font.render(str(self.grid[i][j]), True, (0, 0, 0))
                text_rect = text.get_rect(center=(j * self.box_size + self.box_size // 2, i * self.box_size + 30 + self.box_size // 2))
                self.background.blit(text, text_rect)

    def draw_heading(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.heading_text, self.heading_text_rect)

    def run(self):
        while self.flag:
            self.handle_events()

            self.draw_heading()
            self.draw_grid()

            pygame.display.flip()
            self.clock.tick(60)

class PygameInputManager:
    @staticmethod
    def get_selected_number():
        input_handler = PygameInputHandler()
        input_handler.run()
        return input_handler.selected_number

if __name__ == "__main__":
    selected_number = PygameInputManager.get_selected_number()
    print(f"Number selected by the user: {selected_number}")
