import pygame
import os
from pygame.sprite import Group

from pygame.locals import *

# Initialization of pygame.
pygame.init()
# Creating gaming window 1000 * 725.

screen_size = width, height = (600, 725)
window = pygame.display.set_mode(screen_size)
# Creating window's title.
pygame.display.set_caption('TETRIS')
# icon of game.
icon = pygame.image.load('data/tetris1.jpg')
pygame.display.set_icon(icon)
FPS = 50
clock = pygame.time.Clock()
cycle = True
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


def load_image(name, colorkey=None):
    # adding the folder name to the image name.
    fullname = os.path.join('data', name)
    # loading the picture.
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load:', name)
        raise SystemExit(message)
    image = image.convert()
    # If second setting =-1: doing transparent.
    # color from point 0,0.
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def terminate():
    pygame.quit()
    quit()


def start_screen():
    # loading background.
    fon = load_image('tetris1.jpg')
    # loading music.
    # pygame.mixer.music.load('data/zvuk-vstuplenija-v-tetrise-na-dendi.mp3')
    # pygame.mixer.music.set_volume(0.3)  # 1 -100%  громкости звука.
    # pygame.mixer.music.play(-1)  # играть бесконечно -1.

    # Creation the button 'Play'.
    play_button = Button(280, 70, window)
    # Creation the button 'Rules'.
    rules_button = Button(280, 70, window)
    # Creating the button 'Quit'.
    quit_btn = Button(280, 70, window)
    menu = True

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                check_play_button(play_button, mouse_x, mouse_y)
                check_rules_button(rules_button, mouse_x, mouse_y)
                check_quit_button(quit_btn, mouse_x, mouse_y)

        window.blit(fon, (0, 0))
        play_button.draw_button(160, 200, "Play")
        rules_button.draw_button(160, 300, "Rules")
        quit_btn.draw_button(160, 400, 'Quit')
        pygame.display.flip()
        clock.tick(FPS)


def check_play_button(button, mouse_x, mouse_y):
    """Launch a new game by pressing the button 'Play'."""
    if button.rect.collidepoint(mouse_x, mouse_y):
        pass
        start_game()


def check_rules_button(button, mouse_x, mouse_y):
    """Calling the screen with game's rules."""
    if button.rect.collidepoint(mouse_x, mouse_y):
        rules_show()


def rules_show():
    """Screen with game's rules."""
    intro_text = ["The aim: stay in the game as long as possible.", "",
                  "Collect so many points as possible.", "",
                  "The rate of appearance of 'tetramino' cubes increases", "",
                  " with each level.", "",
                  "Do all your best to fill the raw.", "",
                  "You can turn the figures.", "",
                  "You can personally increase the speed of falling figures.", "",
                  "To pause the game press ESC."]

    fon = load_image('black.jpg')
    window.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 20
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(165, 155, 168))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        window.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def check_quit_button(button, mouse_x, mouse_y):
    """Leave the game."""
    button_clicked = button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked:
        terminate()


def start_game():
    global cycle
    # Adding the music - only mp3.
    # pygame.mixer.music.load('data/space_game.mp3')
    # pygame.mixer.music.set_volume(0.3)  # 1 -100% sound
    # pygame.mixer.music.play(-1)  # play unlimited -1, either a number indicates the amount of payback cycles.
    cycle = True

    while cycle:
        action()


def print_text(x, y, msg, font_color=(0, 0, 0), font_type='data/PingPong.ttf', font_size=50):
    """
    Output the text from the button.
    :param x:  coordinate of starting the message on х.
    :param y: coordinate of starting the message on у.
    :param font_color: font color.
    :param font_type: font type.
    :param font_size: font size.
    :return:
    """
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(msg, True, font_color)
    window.blit(text, (x, y))


class Button:
    def __init__(self, width, heigth, screen):
        """
        Initialization the buttons's attributes.
        :param width: - buttons's width.
        :param heigth: -height.
        :param screen: -screen.
        """
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Purpose of sizes and functions of the buttons.
        self.width, self.heigth = width, heigth
        self.button_color = (0, 219, 106)

        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

    def draw_button(self, x, y, msg):
        # Displaying the buttons.
        self.rect = pygame.Rect(x, y, self.width, self.heigth)
        pygame.draw.rect(self.screen, self.button_color, self.rect)  # (x, y, self.width, self.heigth))
        print_text(x + 90, y + 10, msg)


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * 11 for _ in range(11)]
        self.left = 0
        self.top = 0
        self.cell_size = 30

    def set_view(self, left, top):
        self.left = left
        self.top = top

    def render(self):
        for i in range(10):
            for j in range(24):
                pygame.draw.rect(window, pygame.Color("white"), (
                    self.left + self.cell_size * i, self.top + self.cell_size * j, self.cell_size, self.cell_size), 1)
                pygame.draw.rect(window, pygame.Color("white"), (2, 2, 10 * self.cell_size, 24 * self.cell_size), 1)

# if __name__ == '__main__':
def action():
    pygame.init()
    width = 600
    height = 840
    fps = 10
    size = (width, height)
    # screen = pygame.display.set_mode(size)
    running = True
    game = Board(width, height)
    window.fill((0, 0, 0))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
        game.render()
        pygame.display.flip()


def main():
    start_screen()


main()
