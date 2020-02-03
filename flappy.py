import pygame
import random
import os

WIDTH = 800
HEIGHT = 800
WIN_CAPTION = "Flappy's gonna breed"


def load_img(name):
    return pygame.image.load(os.path.join("img", name))


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(WIN_CAPTION)

pipe_bottom = pygame.transform.scale2x(load_img("pipe_bottom.png"))
pipe_top = pygame.transform.scale2x(load_img("pipe_top.png"))
background = pygame.transform.scale(load_img("background.png"), (WIDTH, HEIGHT))
base_spiral = pygame.transform.scale2x(load_img("base_spiral.png"))
birds = {
    "up": pygame.transform.scale2x(load_img("bird_up.png")),
    "level": pygame.transform.scale2x(load_img("bird_level.png")),
    "down": pygame.transform.scale2x(load_img("bird_down.png"))
}


class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = self.y
        self.img = birds["level"]

    def jump(self):
        pass

    def move(self):
        pass

    def draw(self, _screen):
        _screen.blit(self.img, (self.x, self.y))


class Pipe:
    distance_between = 150

    def __init__(self, x):
        self.x = x
        self.top = 0
        self.bottom = 0
        self.height = 0
        self.pipe_bottom = pipe_bottom
        self.pipe_top = pipe_top
        self._pick_rand_height()

    def move(self):
        pass

    def draw(self, _screen):
        _screen.blit(self.pipe_top, (self.x, self.top))
        _screen.blit(self.pipe_bottom, (self.x, self.bottom))

    def _pick_rand_height(self):
        self.height = random.randrange(50, 400)
        self.top = self.height - self.pipe_top.get_height()
        self.bottom = self.height + self.distance_between


class BaseSpiral:
    def __init__(self):
        self.y = HEIGHT - 100
        self.img = base_spiral
        self.left_x = 0
        self.right_x = base_spiral.get_width()

    def move(self):
        pass

    def draw(self, _screen):
        _screen.blit(self.img, (self.left_x, self.y))
        _screen.blit(self.img, (self.right_x, self.y))


if __name__ == "__main__":
    screen.blit(background, (0, 0))

    bird = Bird(200, 300)
    bird.draw(screen)

    pipe = Pipe(600)
    pipe.draw(screen)

    base = BaseSpiral()
    base.draw(screen)

    pygame.display.flip()
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

    pygame.quit()
