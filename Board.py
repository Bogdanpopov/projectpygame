import pygame


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
        # for i in range(10):
        #     for j in range(24):
        #        pygame.draw.rect(screen, pygame.Color("white"), (
        #        self.left + self.cell_size * i, self.top + self.cell_size * j, self.cell_size, self.cell_size), 0)
        pygame.draw.rect(screen, pygame.Color("white"), (2, 2, 12 * self.cell_size, 26 * self.cell_size), 1)

if __name__ == '__main__':
    pygame.init()
    width = 600
    height = 656
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