import pygame
import os
from pygame.sprite import Group
from typing import *

from pygame.locals import *

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Very simple tetris implementation
#
# Control keys:
# Down - Drop stone faster
# Left/Right - Move stone
# Up - Rotate Stone clockwise
# Escape - Quit game
# P - Pause game
#
# Have fun!

# Copyright (c) 2020 "Anatolii Trofimov & Bogdan Popov" <a3.trofimov@gmail.com popovbogdan21@yandex.ru>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# ._____________________.
# |                     |
# |                     |
# |                     |
# |   ###               |
# |   #                 |
# |   #            #    |
# |                #    |
# | #     ####     ###  |
# |## ## ###### ########|
# |_____________________|

from random import randrange as rand
from collections import deque
from typing import *
import pygame
import sys

# The configuration
config = {
    'cell_size': 25,
    'cols': 10,
    'rows': 24,
    'delay': 0,
    'maxfps': 260,
    'score': 0
}

# Define the colors of the single shapes
colors = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 150, 0),
    (0, 0, 255),
    (255, 120, 0),
    (255, 255, 0),
    (180, 0, 255),
    (0, 220, 220)
]

# Define the shapes of the single parts
tetris_shapes = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 6, 6, 6]],

    [[7, 7],
     [7, 7]]
]

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


config = {
    'cell_size': 25,
    'cols': 10,
    'rows': 24,
    'delay': 0,
    'maxfps': 260,
    'score': 0
}

colors = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 150, 0),
    (0, 0, 255),
    (255, 120, 0),
    (255, 255, 0),
    (180, 0, 255),
    (0, 220, 220)
]


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
    # If second parameter =-1: doing transparent.
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
    font = pygame.font.Font('data/PingPong.ttf', 21)
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
    :param msg:
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
        :param height: -heigth.
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
        self.screen = pygame.display.set_mode((self.width, self.height))

    def set_view(self, left, top):
        self.left = left
        self.top = top

    def render(self):
        for i in range(10):
            for j in range(24):
                pygame.draw.rect(window, pygame.Color("white"), (
                    self.left + self.cell_size * i, self.top + self.cell_size * j, self.cell_size, self.cell_size), 1)
                pygame.draw.rect(window, pygame.Color("white"), (2, 2, 10 * self.cell_size, 24 * self.cell_size), 1)

    def new_board(self) -> List[List[int]]:  # Board
        """
        Creating empty board for the new game.
        :return: new empty board
        """
        self.board = [[0 for _ in range(config['cols'])]
                 for _ in range(config['rows'])] + \
                [[1 for _ in range(config['cols'])]]
        return self.board

    def draw_matrix(self, matrix: List[List[int]], offset: Tuple[int, int]) -> None:  # Board
        """
        Drawing the given matrix with the given offset
        :param matrix: matrix of integers which is needed to draw
        :param offset: matrix offset
        :return: None
        """
        off_x, off_y = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                # going through every cell and paint it
                if val:
                    pygame.draw.rect(
                        self.screen,
                        colors[val],
                        pygame.Rect(
                            (off_x + x) *
                            config['cell_size'],
                            (off_y + y) *
                            config['cell_size'],
                            config['cell_size'],
                            config['cell_size']), 0)

    @staticmethod
    def join_matrixes(matrix_1: List[List[int]],
                      matrix_2: List[List[int]],
                      matrix_2_off: Tuple[int, int]) -> List[List[int]]:  # Board
        """
        Inserting one small matrix into the big matrix according to the given coordinates.
        :param matrix_1: big matrix
        :param matrix_2: small matrix
        :param matrix_2_off: small matrix's coordinates
        :return: big matrix including small one
        """
        off_x, off_y = matrix_2_off
        for cy, row in enumerate(matrix_2):
            for cx, val in enumerate(row):
                matrix_1[cy + off_y - 1][cx + off_x] += val
        return matrix_1

    @staticmethod
    def check_collision(board: List[List], shape: List[List], offset: Tuple) -> bool:  # Board
        """
        Checking whether shape doesn't hit borders.
        :param board: current playing board
        :param shape: falling shape
        :param offset: x and y coordinates of the falling shape
        :return: if shape hits border: True else: False
        """
        off_x, off_y = offset
        for cy, row in enumerate(shape):
            for cx, cell in enumerate(row):
                try:
                    if cell and board[cy + off_y][cx + off_x]:
                        return True
                except IndexError:
                    return True
        return False


class TetrisApp(object):
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(250, 25)
        pygame.mouse.set_visible(False)               # We do not need mouse movement
        pygame.event.set_blocked(pygame.MOUSEMOTION)  # events, so we block them.

        self.width = config['cell_size'] * config['cols']
        self.height = config['cell_size'] * config['rows']

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.stones = deque([tetris_shapes[rand(len(tetris_shapes))]], maxlen=2)
        self.stone = None
        self.stone_x = None
        self.stone_y = None
        self.board = None
        self.gameover = False
        self.paused = False
        self.init_game()

    def new_stone(self) -> None:
        """
        Preparing next random stone for the game.
        :return: None
        """
        self.stones.append(tetris_shapes[rand(len(tetris_shapes))])

        self.stone = self.stones.popleft()
        self.stone_x = int(config['cols'] / 2 - len(self.stone[0]) / 2)
        self.stone_y = 0

        print(*self.stones[-1], sep='\n')
        print()

        if check_collision(self.board,
                           self.stone,
                           (self.stone_x, self.stone_y)):
            self.gameover = True

    def init_game(self) -> None:
        """
        Resetting game (updating score and speed, making new board and new stones)
        :return: None
        """
        config['score'] = 0
        config['delay'] = 750
        self.board = new_board()
        self.new_stone()

    def center_msg(self, msg: str) -> None:  # App ?
        """
        Displays given message in the center of the screen.
        :param msg: message
        :return: None
        """
        for i, line in enumerate(msg.splitlines()):  # displaying every line
            msg_image = pygame.font.Font(
                pygame.font.get_default_font(), 20).render(
                line, False, (255, 255, 255), (0, 0, 0))

            msgim_center_x, msgim_center_y = msg_image.get_size()
            msgim_center_x //= 2
            msgim_center_y //= 2

            self.screen.blit(msg_image, (
                self.width // 2 - msgim_center_x,
                self.height // 2 - msgim_center_y + i * 22))

    def draw_matrix(self, matrix: List[List[int]], offset: Tuple[int, int]) -> None:  # Board (done)
        """
        Drawing the given matrix with the given offset
        :param matrix: matrix of integers which is needed to draw
        :param offset: matrix offset
        :return: None
        """
        off_x, off_y = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                # going through every cell and paint it
                if val:
                    pygame.draw.rect(
                        self.screen,
                        colors[val],
                        pygame.Rect(
                            (off_x + x) *
                            config['cell_size'],
                            (off_y + y) *
                            config['cell_size'],
                            config['cell_size'],
                            config['cell_size']), 0)

    def move(self, delta_x: int) -> None:
        if not self.gameover and not self.paused:  # checking whether game is paused or finished
            new_x = min(max(0, self.stone_x + delta_x), config['cols'] - len(self.stone[0]))
            if not check_collision(self.board,
                                   self.stone,
                                   (new_x, self.stone_y)):
                self.stone_x = new_x

    def quit(self) -> None:  # App ?
        self.center_msg("Exiting...")
        pygame.display.update()
        sys.exit()

    def drop(self) -> None:
        if not self.gameover and not self.paused:
            self.stone_y += 1
            if check_collision(self.board, self.stone,
                               (self.stone_x, self.stone_y)):
                self.board = join_matrixes(self.board, self.stone,
                                           (self.stone_x, self.stone_y))
                self.new_stone()
                while True:
                    for i, row in enumerate(self.board[:-1]):
                        if 0 not in row:
                            self.board = remove_row(self.board, i)
                            break
                    else:
                        break

    def rotate_stone(self) -> None:
        if not self.gameover and not self.paused:
            new_stone = rotate_clockwise(self.stone)
            if not check_collision(self.board,
                                   new_stone,
                                   (self.stone_x, self.stone_y)):
                self.stone = new_stone

    def toggle_pause(self) -> None:  # App ?
        self.paused = not self.paused

    def start_game(self) -> None:  # App ?
        if self.gameover:
            self.init_game()
            self.gameover = False

    def run(self) -> None:
        key_actions = {  # control key fuctions
            'ESCAPE': self.quit,
            'LEFT': lambda: self.move(-1),
            'RIGHT': lambda: self.move(+1),
            'DOWN': self.drop,
            'UP': self.rotate_stone,
            'p': self.toggle_pause,
            'SPACE': self.start_game
        }

        pygame.time.set_timer(pygame.USEREVENT + 1, config['delay'])
        dont_burn_my_cpu = pygame.time.Clock()
        while 1:
            # prepapring board
            self.screen.fill((0, 0, 0))

            # outputing the score
            text_score = pygame.font.Font(pygame.font.get_default_font(), 15) \
                .render(str(config['score']), False, (255, 255, 255))
            self.screen.blit(text_score, (10, 10))

            # must have conditions, checking the game process
            if self.gameover:
                self.center_msg(f"Game Over!\nYou scored: {config['score']}!\nPress space to continue...")
            elif self.paused:
                self.center_msg("Paused")
            else:  # if not paused and not finished the board will draw
                self.draw_matrix(self.board, (0, 0))
                self.draw_matrix(self.stone,
                                 (self.stone_x,
                                  self.stone_y))
            pygame.display.update()

            # checking pressed buttons and calling key controls functions
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 1:
                    self.drop()
                elif event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    for key in key_actions:
                        if event.key == eval("pygame.K_" + key):
                            key_actions[key]()

            dont_burn_my_cpu.tick(config['maxfps'])



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