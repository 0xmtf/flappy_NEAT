import pygame
import random
import math
import os

FPS = 60
MS_UNIT = 1000.0
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
    ROTATE = 30
    DROP_SPEED = 0.3
    CLIMB_SPEED = 0.3
    CLIMB_DURATION = 300.00
    BIRD_WIDTH = BIRD_HEIGHT = 42

    def __init__(self, x, y, climb_rate):
        self.x = x
        self.y = y
        self.height = self.y
        self.climb_rate = climb_rate
        self._img_up = birds["up"]
        self._img_down = birds["down"]
        self._rotate_up = False
        self._rotate_down = False

    def jump(self):
        self.climb_rate = self.CLIMB_DURATION

    def update(self, delta=1.2):
        _frame = Frame()
        if self.climb_rate > 0:
            _climb = 1 - self.climb_rate / self.CLIMB_DURATION
            self.y -= (self.CLIMB_SPEED *
                       _frame.to_ms(delta) *
                       (1 - math.cos(_climb * math.pi)))
            self.climb_rate -= _frame.to_ms(delta)
            self._rotate_down = False
            self._rotate_up = True
        else:
            self._rotate_down = True
            self._rotate_up = False
            self.y += self.DROP_SPEED * _frame.to_ms(delta)

    def draw(self, _screen):
        if self._rotate_up:
            self._tilted_move(_screen, 1)
        elif self._rotate_down:
            self._tilted_move(_screen, -1)
        else:
            self._tilted_move(_screen, 0)

    def _tilted_move(self, _screen, direction=0):
        if direction > 0:
            _rotated = pygame.transform.rotate(self._animated_wings, self.ROTATE)
            _screen.blit(_rotated, self._position)
        elif direction < 0:
            _rotated = pygame.transform.rotate(self._animated_wings, -self.ROTATE)
            _screen.blit(_rotated, self._position)
        else:
            _screen.blit(self._animated_wings, self._position)

    @property
    def _animated_wings(self):
        if pygame.time.get_ticks() % 500 >= 250:
            return self._img_up
        else:
            return self._img_down

    @property
    def _position(self):
        return pygame.Rect(self.x,
                           self.y,
                           self.BIRD_WIDTH,
                           self.BIRD_HEIGHT)


class Pipe:
    DISTANCE = 200

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
        self.bottom = self.height + self.DISTANCE


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


class Frame:
    def __init__(self):
        self.fps = FPS
        self.ms = MS_UNIT

    def to_ms(self, frames):
        return self.ms * frames / self.fps

    def to_frame(self, millis):
        return self.fps * millis / self.ms


def draw_game(_screen, _background, _bird, _pipe, _base):
    _screen.blit(_background, (0, 0))
    _bird.draw(_screen)
    _pipe.draw(_screen)
    _base.draw(_screen)

    pygame.display.flip()


if __name__ == "__main__":
    bird = Bird(200, 300, 2)
    pipe = Pipe(600)
    base = BaseSpiral()

    draw_game(screen, background, bird, pipe, base)
    clock = pygame.time.Clock()
    done = False
    while not done:
        clock.tick(FPS)
        base.move()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        bird.update()
        draw_game(screen, background, bird, pipe, base)

    pygame.quit()
