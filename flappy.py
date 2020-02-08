import pygame
import random
import math
import os


class Bird:
    ROTATE = 30
    DROP_SPEED = 0.2
    CLIMB_SPEED = 0.24
    CLIMB_DURATION = 300.00
    BIRD_WIDTH = BIRD_HEIGHT = 32

    def __init__(self, x, y, climb_rate, bird_images):
        self.x = x
        self.y = y
        self.height = self.y
        self.climb_rate = climb_rate
        self._img_up = bird_images["up"]
        self._img_down = bird_images["down"]
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
    ANIMATION = .28

    def __init__(self, x, pipe_bottom_image, pipe_top_image):
        self.x = x
        self.top = 0
        self.bottom = 0
        self.height = 0
        self.pipe_bottom = pipe_bottom_image
        self.pipe_top = pipe_top_image
        self.visible = True
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
                     self.top - round(_bird.y))
        bottom_index = (int(self.x - _bird.x),
                        self.bottom - round(_bird.y))
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

    @property
    def width(self):
        return self.pipe_top.get_width()


class BaseSpiral:
    ANIMATION = .28

    def __init__(self, height, base_spiral_image):
        self.y = height
        self.width = base_spiral_image.get_width()
        self.img = base_spiral_image
        self.left_x = 0
        self.right_x = self.width
        self._frame = Frame()

    def update(self, delta=1):
        self.left_x -= self.ANIMATION * self._frame.to_ms(delta)
        self.right_x -= self.ANIMATION * self._frame.to_ms(delta)
        if self.left_x + self.width < 0:
            self.left_x = self.right_x + self.width
        if self.right_x + self.width < 0:
            self.right_x = self.left_x + self.width

    def draw(self, _screen):
        _screen.blit(self.img, (self.left_x, self.y))
        _screen.blit(self.img, (self.right_x, self.y))
        self.update()

    def collides_with(self, _bird):
        left_index = (int(self.left_x - _bird.x),
                      self.y - round(_bird.y))
        right_index = (int(self.right_x - _bird.x),
                       self.y - round(_bird.y))
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
        self.fps = 60
        self.ms = 1000.0

    def to_ms(self, frames):
        return self.ms * frames / self.fps

    def to_frame(self, millis):
        return self.fps * millis / self.ms


class Flappy:
    FPS = 60
    MS_UNIT = 1000.0
    WIDTH = 800
    HEIGHT = 800
    BLACK = (0, 0, 0)
    WIN_CAPTION = "Flappy's gonna breed"
    RESTART_MESSAGE = "Press ENTER to restart"
    SCORE_TEXT = "Score: {}"

    def __init__(self):
        self.background_image = None
        self.base_image = None
        self.pipe_bottom_image = None
        self.pipe_top_image = None
        self.bird_images = None
        self._load_assets()

        pygame.init()
        pygame.font.init()
        self._screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption(self.WIN_CAPTION)

        self.display_font = pygame.font.SysFont("calibri", 40)
        self.score_font = pygame.font.SysFont("calibri", 30)

    def basic_play(self):
        bird = self._init_bird()
        pipes = [self._init_pipe()]
        base = self._init_base()
        score = 0

        self.draw_screen(bird, pipes, base, score)

        clock = pygame.time.Clock()
        done = False
        lost = False
        while not done:
            clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird.jump()

            bird.update()

            for pipe in pipes:
                if pipe.collides_with(bird):
                    self.lost_screen()

                if base.collides_with(bird):
                    self.lost_screen()

                if pipe.visible and pipe.x < bird.x:
                    pipe.visible = False
                    pipes.append(self._init_pipe())
                    score += 1

                if pipe.x + pipe.width < 0:
                    pipes.remove(pipe)
            self.draw_screen(bird, pipes, base, score)

        pygame.quit()
        quit()

    def draw_screen(self, bird, pipes, base, score):
        self._screen.blit(self.background_image, (0, 0))
        bird.draw(self._screen)

        for pipe in pipes:
            pipe.draw(self._screen)

        base.draw(self._screen)

        score_label = self.score_font \
            .render(self.SCORE_TEXT.format(score), 1, self.BLACK)
        self._screen.blit(score_label, (5, 5))
        pygame.display.flip()

    def lost_screen(self):
        active = True
        message = self.display_font.render(self.RESTART_MESSAGE, 1, self.BLACK)
        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    active = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.basic_play()

            self._screen.blit(message, (self.WIDTH / 2 - message.get_width() / 2, self.HEIGHT / 2))
            pygame.display.flip()

        pygame.quit()

    def _load_assets(self):
        def _load_transform(file_name, scale):
            if scale == 1:
                return pygame.transform.scale(
                    pygame.image.load(os.path.join("img", file_name)),
                    (self.WIDTH, self.HEIGHT)
                )
            elif scale == 2:
                return pygame.transform.scale2x(
                    pygame.image.load(os.path.join("img", file_name))
                )

        self.background_image = _load_transform("background.png", scale=1)
        self.pipe_bottom_image = _load_transform("pipe_bottom.png", scale=2)
        self.pipe_top_image = _load_transform("pipe_top.png", scale=2)
        self.base_image = _load_transform("base_spiral.png", scale=2)
        self.bird_images = {
            "up": _load_transform("bird_up.png", scale=2),
            "down": _load_transform("bird_down.png", scale=2)
        }

    def _init_pipe(self):
        return Pipe(self.WIDTH,
                    self.pipe_bottom_image,
                    self.pipe_top_image)

    def _init_bird(self):
        return Bird(self.WIDTH / 4, self.HEIGHT / 2, 2, self.bird_images)

    def _init_base(self):
        return BaseSpiral(self.HEIGHT - 100, self.base_image)


if __name__ == "__main__":
    flappy = Flappy()
    flappy.basic_play()
