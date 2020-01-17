import pygame
import os
from pygame.sprite import Group

from pygame.locals import *

# Инициализируем pygame
pygame.init()
# Создаём игровое окно 800*570

screen_size = width, height = (800, 570)
window = pygame.display.set_mode(screen_size)
# Ставим свой заголовок окна
pygame.display.set_caption('TETRIS')
# иконка игры
icon = pygame.image.load('data/tetris1.jpg')
pygame.display.set_icon(icon)
FPS = 50
clock = pygame.time.Clock()
cycle = True
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


def load_image(name, colorkey=None):
    # Добавляем к имени картинки имя папки
    fullname = os.path.join('data', name)
    # Загружаем картинку
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert()
    # Если второй параметр =-1 делаем прозрачным
    # цвет из точки 0,0
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image, image.get_rect()


def terminate():
    pygame.quit()
    quit()


def start_screen():
    # загружаем фон
    fon, b = load_image('tetris1.jpg')
    # загружаем музыку
    pygame.mixer.music.load('data/zvuk-vstuplenija-v-tetrise-na-dendi.mp3')
    pygame.mixer.music.set_volume(0.3)  # 1 -100%  громкости звука
    pygame.mixer.music.play(-1)  # играть бесконечно -1

    # # Создание кнопки Play.
    # play_button = Button(280, 70, window)
    # # Создание кнопки Показать правила
    # rules_button = Button(280, 70, window)
    # # кнопка завершить игру
    # quit_btn = Button(280, 70, window)
    menu = True

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # check_play_button(play_button, mouse_x, mouse_y)
                # check_rules_button(rules_button, mouse_x, mouse_y)
                # check_quit_button(quit_btn, mouse_x, mouse_y)

        window.blit(fon, (0, 0))
        # play_button.draw_button(500, 200, "Play")
        # rules_button.draw_button(500, 300, "Rules")
        # quit_btn.draw_button(500, 400, 'Quit')
        pygame.display.flip()
        clock.tick(FPS)


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * 11 for _ in range(11)]
        self.left = 0
        self.top = 0
        self.cell_size = 35

    def set_view(self, left, top):
        self.left = left
        self.top = top

    def render(self):
        for i in range(10):
            for j in range(10):
                pygame.draw.rect(screen, pygame.Color("white"), (
                    self.left + self.cell_size * i, self.top + self.cell_size * j, self.cell_size, self.cell_size), 1)


# if __name__ == '__main__':
def action():
    pygame.init()
    width = 600
    height = 840
    fps = 10
    size = (width, height)
    screen = pygame.display.set_mode(size)
    running = True
    game = Board(width, height)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        game.render()
        pygame.display.flip()


def main():
    start_screen()


main()