import pygame
import random
import math
import os

FPS = 60
MS_UNIT = 1000.0
WIDTH = 800
HEIGHT = 800
WIN_CAPTION = "Flappy's gonna breed"


# DISPLAY_FONT = pygame.font.SysFont("calibri", 60)


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
    DROP_SPEED = 0.2
    CLIMB_SPEED = 0.2
    CLIMB_DURATION = 300.00
    BIRD_WIDTH = BIRD_HEIGHT = 42

    def __init__(self, x, y, climb_rate):
        self.x = x
        self.y = y
        self.height = self.y
        self.climb_rate = climb_rate
        self._img_up = birds["up"]
        self._img_down = birds["down"]
        self._img_up_mask = pygame.mask \
            .from_surface(self._img_up)
        self._img_down_mask = pygame.mask \
            .from_surface(self._img_down)
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
            _rotated = pygame.transform.rotate(self.image, self.ROTATE)
            _screen.blit(_rotated, self.rect)
        elif direction < 0:
            _rotated = pygame.transform.rotate(self.image, -self.ROTATE)
            _screen.blit(_rotated, self.rect)
        else:
            _screen.blit(self.image, self.rect)

    @property
    def rect(self):
        return pygame.Rect(self.x,
                           self.y,
                           self.BIRD_WIDTH,
                           self.BIRD_HEIGHT)

    @property
    def mask(self):
        if pygame.time.get_ticks() % 500 >= 250:
            return self._img_up_mask
        else:
            return self._img_down_mask

    @property
    def image(self):
        if pygame.time.get_ticks() % 500 >= 250:
            return self._img_up
        else:
            return self._img_down


class Pipe:
    DISTANCE = 200
    ANIMATION = .18

    def __init__(self, x):
        self.x = x
        self.top = 0
        self.bottom = 0
        self.height = 0
        self.pipe_bottom = pipe_bottom
        self.pipe_top = pipe_top
        self._frame = Frame()
        self._pick_rand_height()

    def update(self, delta=1):
        self.x -= self.ANIMATION * self._frame.to_ms(delta)

    def draw(self, _screen):
        _screen.blit(self.pipe_top, (self.x, self.top))
        _screen.blit(self.pipe_bottom, (self.x, self.bottom))
        self.update()

    def collides_with(self, _bird):
        top_index = (int(self.x - _bird.x),
                     self.top - math.floor(_bird.y))
        bottom_index = (int(self.x - _bird.x),
                        self.bottom - math.floor(_bird.y))
        top_hit = _bird.mask \
            .overlap(self._get_mask(position="top"), top_index)
        bottom_hit = _bird.mask \
            .overlap(self._get_mask(position="bottom"), bottom_index)

        if top_hit is not None or bottom_hit is not None:
            return True

        return False

    def _pick_rand_height(self):
        self.height = random.randrange(50, 400)
        self.top = self.height - self.pipe_top.get_height()
        self.bottom = self.height + self.DISTANCE

    def _get_mask(self, position):
        if position.lower() == "top":
            return pygame.mask.from_surface(self.pipe_top)
        elif position.lower() == "bottom":
            return pygame.mask.from_surface(self.pipe_bottom)


class BaseSpiral:
    IMG_WIDTH = base_spiral.get_width()
    ANIMATION = .18

    def __init__(self):
        self.y = HEIGHT - 100
        self.img = base_spiral
        self.left_x = 0
        self.right_x = self.IMG_WIDTH
        self._frame = Frame()

    def update(self, delta=1):
        self.left_x -= self.ANIMATION * self._frame.to_ms(delta)
        self.right_x -= self.ANIMATION * self._frame.to_ms(delta)
        if self.left_x + self.IMG_WIDTH < 0:
            self.left_x = self.right_x + self.IMG_WIDTH
        if self.right_x + self.IMG_WIDTH < 0:
            self.right_x = self.left_x + self.IMG_WIDTH

    def draw(self, _screen):
        _screen.blit(self.img, (self.left_x, self.y))
        _screen.blit(self.img, (self.right_x, self.y))
        self.update()

    def collides_with(self, _bird):
        left_index = (int(self.left_x - _bird.x),
                      self.y - math.floor(_bird.y))
        right_index = (int(self.right_x - _bird.x),
                       self.y - math.floor(_bird.y))
        left_hit = _bird.mask \
            .overlap(self.mask, left_index)
        right_hit = _bird.mask \
            .overlap(self.mask, right_index)

        if left_hit is not None or right_hit is not None:
            return True

        return False

    @property
    def mask(self):
        return pygame.mask.from_surface(self.img)


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
    pipe = Pipe(850)
    base = BaseSpiral()

    draw_game(screen, background, bird, pipe, base)
    clock = pygame.time.Clock()
    done = False
    while not done:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        if pipe.collides_with(bird) or base.collides_with(bird):
            done = True
        bird.update()

        draw_game(screen, background, bird, pipe, base)

    pygame.quit()
