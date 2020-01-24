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


def rotate_clockwise(shape: List[List]) -> List[List]:  # Tetris
    """
    Rotating the falling shape clockwise.
    :param shape: current shape
    :return: rotated shape
    """
    return [[shape[y][x]
             for y in range(len(shape))]
            for x in range(len(shape[0]) - 1, -1, -1)]


def check_collision(board: List[List], shape: List[List], offset: Tuple) -> bool:  # Board
    """
    Checking whether shape doesn't hit borders.
    :param board: current playing board
    :param shape: falling shape
    :param offset: x and y coordinates
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


def remove_row(board: List[List[int]], row: int) -> List[List[int]]:  # Tetris App
    """
    - Removing row which is full of blocks.
    - Adding score.
    - Adding empty row to the top of the board
    :param board: current playing board
    :param row: row number
    :return: new board without first row
    """
    del board[row]
    config['score'] += 100
    return [[0 for _ in range(config['cols'])]] + board


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


def new_board() -> List[List[int]]:  # Board
    """
    Creating empty board for the new game.
    :return: new empty board
    """
    board = [[0 for _ in range(config['cols'])]
             for _ in range(config['rows'])] + \
            [[1 for _ in range(config['cols'])]]
    return board


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


if __name__ == '__main__':
    App = TetrisApp()
    App.run()