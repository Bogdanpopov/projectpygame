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
    # pygame.mixer.music.load('data/zvuk-vstuplenija-v-tetrise-na-dendi.mp3')
    # pygame.mixer.music.set_volume(0.3)  # 1 -100%  громкости звука
    # pygame.mixer.music.play(-1)  # играть бесконечно -1

    # Создание кнопки Play.
    play_button = Button(280, 70, window)
    # Создание кнопки Показать правила
    rules_button = Button(280, 70, window)
    # кнопка завершить игру
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
        play_button.draw_button(500, 200, "Play")
        rules_button.draw_button(500, 300, "Rules")
        quit_btn.draw_button(500, 400, 'Quit')
        pygame.display.flip()
        clock.tick(FPS)


def check_play_button(button, mouse_x, mouse_y):
    """Запускает новую игру при нажатии кнопки Play."""
    if button.rect.collidepoint(mouse_x, mouse_y):
        pass
        start_game()


def check_rules_button(button, mouse_x, mouse_y):
    """Вызывает экран с правилами игры"""
    if button.rect.collidepoint(mouse_x, mouse_y):
        rules_show()


def rules_show():
    """экран с правилами игры"""
    intro_text = ["Цель: как можно дольше продержаться в игре", "",
                  "Собрать как можно больше очков ", "",
                  "Скорость появления кубиков тетрамино с каждым уровнем растет", "",
                  "Стараться заполнить ряд", "",
                  "Можно поворачивать фигурки", "",
                  "Можно собственноручно увеличивать скорость падения фигур", "",
                  "Для паузы в игре нажмите ESC"]

    fon, b = load_image('tetris2.jpg')
    window.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 20
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(32, 17, 240))
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
    """Выход из игры."""
    button_clicked = button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked:
        terminate()


def start_game():
    global cycle
    # добавляем музыку - только mp3
    # pygame.mixer.music.load('data/space_game.mp3')
    # pygame.mixer.music.set_volume(0.3)  # 1 -100%   звука
    # pygame.mixer.music.play(-1)  # играть бесконечно -1, либо число означаюшее кличество циклов проигрывания
    cycle = True

    while cycle:
        action()


def print_text(x, y, msg, font_color=(0, 0, 0), font_type='data/PingPong.ttf', font_size=50):
    """
    вывод текста на кнопке
    :param x:  координата начала сообщения по х
    :param y: координата начала сообщения по у
    :param font_color: цвет шрифта
    :param font_type: тип  шрифта
    :param font_size: размер шрифта
    :return:
    """
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(msg, True, font_color)
    window.blit(text, (x, y))


class Button:
    def __init__(self, width, heigth, screen):
        """
        Инициализирует атрибуты кнопки.
        :param width: -ширина кнопки
        :param heigth: -высота
        :param screen: -экран
        """
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Назначение размеров и свойств кнопок.
        self.width, self.heigth = width, heigth
        self.button_color = (0, 219, 106)

        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

    def draw_button(self, x, y, msg):
        # Отображение  кнопки
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
        self.cell_size = 25

    def set_view(self, left, top):
        self.left = left
        self.top = top

    def render(self):
        for i in range(10):
            for j in range(24):
               pygame.draw.rect(window, pygame.Color("white"), (
               self.left + self.cell_size * i, self.top + self.cell_size * j, self.cell_size, self.cell_size), 0)
        pygame.draw.rect(window, pygame.Color("white"), (2, 2, 12 * self.cell_size, 26 * self.cell_size), 1)


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

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        game.render()
        pygame.display.flip()


def main():
    start_screen()


main()
