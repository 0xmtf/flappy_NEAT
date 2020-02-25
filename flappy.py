import pygame
import random
import neat
import os


class Bird:
    ROTATE_ANGLE = 30
    CLIMB_RATE = 0
    DROP_SPEED = 0.18
    CLIMB_SPEED = 0.18
    CLIMB_DURATION = 280.00

    def __init__(self, x, y, bird_images):
        self.x = x
        self.y = y
        self.climb_rate = self.CLIMB_RATE
        self._img_up = bird_images["up"]
        self._img_down = bird_images["down"]
        self._img_up_mask = pygame.mask \
            .from_surface(self._img_up)
        self._img_down_mask = pygame.mask \
            .from_surface(self._img_down)
        self._rotate_up = False
        self._rotate_down = False
        self._frame = Frame()

    def jump(self):
        self.climb_rate = self.CLIMB_DURATION

    def update(self, delta=1):
        if self.climb_rate > 0:
            self.y -= self.CLIMB_SPEED * self._frame.to_ms(delta)
            self.climb_rate -= self._frame.to_ms(delta)
            self._rotate_down = False
            self._rotate_up = True
        else:
            self.y += self.DROP_SPEED * self._frame.to_ms(delta)
            self._rotate_down = True
            self._rotate_up = False

    def draw(self, _screen):
        if self._rotate_up:
            self._tilted_move(_screen, direction=1)
        elif self._rotate_down:
            self._tilted_move(_screen, direction=-1)
        else:
            self._tilted_move(_screen, direction=0)

    def _tilted_move(self, _screen, direction=0):
        if direction > 0:
            _rotated = pygame.transform.rotate(self.image, self.ROTATE_ANGLE)
            _screen.blit(_rotated, self.rect)
        elif direction < 0:
            _rotated = pygame.transform.rotate(self.image, -self.ROTATE_ANGLE)
            _screen.blit(_rotated, self.rect)
        else:
            _screen.blit(self.image, self.rect)

    @property
    def rect(self):
        return pygame.Rect(self.x,
                           self.y,
                           self.img_width,
                           self.img_height)

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

    @property
    def img_height(self):
        return self._img_up.get_height()

    @property
    def img_width(self):
        return self._img_up.get_width()


class Pipe:
    DISTANCE = 160
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
                     self.top - round(_bird.y) - 15)
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
        self.height = random.randrange(100, 420)
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

    def __init__(self, y, base_spiral_image):
        self.y = y
        self.img = base_spiral_image
        self.left_x = 0
        self.right_x = self.img_width
        self._frame = Frame()

    def update(self, delta=1):
        self.left_x -= self.ANIMATION * self._frame.to_ms(delta)
        self.right_x -= self.ANIMATION * self._frame.to_ms(delta)
        if abs(self.left_x) > self.img_width:
            self.left_x = self.right_x + self.img_width
        if abs(self.right_x) > self.img_width:
            self.right_x = self.left_x + self.img_width

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

    @property
    def img_width(self):
        return self.img.get_width()


class Frame:
    def __init__(self):
        self.fps = 60
        self.ms = 1000.0

    def to_ms(self, frames):
        return self.ms * frames / self.fps

    def to_frame(self, millis):
        return self.fps * millis / self.ms


class Flappy:
    FPS = 90
    MS_UNIT = 1000.0
    WIDTH = 600
    HEIGHT = 800
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    WIN_CAPTION = "Flappy's gonna breed"
    RESTART_MESSAGE = "Press ENTER to restart"
    BASIC_PLAY = "1. Basic play"
    NEAT_LIB_PLAY = "2. NEAT lib"
    NEAT_SELF_IMPL = "3. NEAT impl"
    SCORE_TEXT = "Score: {}"
    GEN_TEXT = "Generation: {}"

    def __init__(self):
        self.background_image = None
        self.base_image = None
        self.pipe_bottom_image = None
        self.pipe_top_image = None
        self.bird_images = None
        self._bird_generation = 0
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

        self._draw_screen(bird, pipes, base, score)

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
                    self._lost_screen()

                if base.collides_with(bird):
                    self._lost_screen()

                if pipe.visible and pipe.x < bird.x:
                    pipe.visible = False
                    pipes.append(self._init_pipe())
                    score += 1

                if pipe.x + pipe.width < 0:
                    pipes.remove(pipe)
            self._draw_screen(bird, pipes, base, score)

        pygame.quit()
        quit()

    def neat_lib_play(self):
        config_file = self._get_config_path()

        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             config_file)

        population = neat.Population(config)
        population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        population.add_reporter(stats)

        winner = population.run(self._eval_genomes, 150)

        print("\nBest genome: \n{!s}".format(winner))

    def neat_self_impl_play(self):
        pass

    def intro_screen(self):
        basic_msg = self.display_font. \
            render(self.BASIC_PLAY, 1, self.BLACK)
        neat_lib_msg = self.display_font. \
            render(self.NEAT_LIB_PLAY, 1, self.BLACK)
        neat_impl_msg = self.display_font. \
            render(self.NEAT_SELF_IMPL, 1, self.BLACK)

        self._screen.blit(self.background_image, (0, 0))
        self._screen.blit(self.base_image, (0, self.HEIGHT - 100))
        self._screen.blit(basic_msg,
                          (self.WIDTH / 2 - basic_msg.get_width() / 2, self.HEIGHT / 3))
        self._screen.blit(neat_lib_msg,
                          (self.WIDTH / 2 - basic_msg.get_width() / 2, self.HEIGHT / 3 + 75))
        self._screen.blit(neat_impl_msg,
                          (self.WIDTH / 2 - basic_msg.get_width() / 2, self.HEIGHT / 3 + 150))
        pygame.display.flip()

    def _eval_genomes(self, genomes, config):
        birds = []
        local_genomes = []
        networks = []
        self._bird_generation += 1
        for genome_id, genome in genomes:
            genome.fitness = 0.0
            networks.append(neat.nn.FeedForwardNetwork.
                            create(genome, config))
            birds.append(self._init_bird())
            local_genomes.append(genome)

        pipes = [self._init_pipe()]
        base = self._init_base()
        score = 0

        clock = pygame.time.Clock()
        done = False
        while not done and len(birds) > 0:
            clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    pygame.quit()
                    quit()

            curr_pipe = 0
            if len(pipes) > 1 and pipes[0].x < bird.x:
                curr_pipe = 1

            for idx, bird in enumerate(birds):
                bird.update()
                output = networks[idx].activate(
                    (bird.y,
                     abs(bird.y - pipes[curr_pipe].height),
                     abs(bird.y - pipes[curr_pipe].bottom),
                     abs(bird.y - base.y)))

                if output[0] > 0.5:
                    bird.jump()

            for bird in birds:
                bird.update()

            for pipe in pipes:  # O(n^3)
                for bird in birds:
                    if pipe.collides_with(bird) or \
                            base.collides_with(bird) or \
                            bird.y < -10:
                        bird_idx = birds.index(bird)
                        local_genomes[bird_idx].fitness -= 1.5
                        local_genomes.pop(bird_idx)
                        networks.pop(bird_idx)
                        birds.pop(bird_idx)

                    if bird in birds and \
                            pipe.visible and \
                            pipe.x + pipe.width < bird.x:
                        bird_idx = birds.index(bird)
                        pipe.visible = False
                        pipes.append(self._init_pipe())
                        score += 1
                        local_genomes[bird_idx].fitness += 1.5

                if pipe.x + pipe.width < 0:
                    pipes.remove(pipe)

            self._draw_screen_neat(birds, pipes, base, score)

    def _draw_screen(self, bird, pipes, base, score):
        self._screen.blit(self.background_image, (0, 0))
        bird.draw(self._screen)

        for pipe in pipes:
            pipe.draw(self._screen)

        base.draw(self._screen)

        score_label = self.score_font \
            .render(self.SCORE_TEXT.format(score), 1, self.BLACK)
        self._screen.blit(score_label, (5, 5))
        pygame.display.flip()

    def _draw_screen_neat(self, birds, pipes, base, score):
        self._screen.blit(self.background_image, (0, 0))
        for bird in birds:
            bird.draw(self._screen)
            pygame.draw \
                .line(self._screen, self.WHITE,
                      (bird.x + bird.img_width, bird.y + bird.img_height),
                      (pipes[0].x, pipes[0].height),
                      3)
            pygame.draw \
                .line(self._screen, self.WHITE,
                      (bird.x + bird.img_width, bird.y + bird.img_height),
                      (pipes[0].x, pipes[0].bottom),
                      3)
            pygame.draw \
                .line(self._screen, self.WHITE,
                      (bird.x + bird.img_width / 2, bird.y + bird.img_height),
                      (bird.x + bird.img_width, base.y),
                      3)

        for pipe in pipes:
            pipe.draw(self._screen)

        base.draw(self._screen)

        generation_label = self.score_font \
            .render(self.GEN_TEXT.format(self._bird_generation), 1, self.BLACK)

        score_label = self.score_font \
            .render(self.SCORE_TEXT.format(score), 1, self.BLACK)

        self._screen.blit(generation_label, (5, 5))
        self._screen.blit(score_label, (5, 35))

        pygame.display.flip()

    def _lost_screen(self):
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
        quit()

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
        return Pipe(self.WIDTH + 50,
                    self.pipe_bottom_image,
                    self.pipe_top_image)

    def _init_bird(self):
        rand_y = random.randrange(10, 50)
        return Bird(self.WIDTH / 4, self.HEIGHT / 2 - rand_y, self.bird_images)

    def _init_base(self):
        return BaseSpiral(self.HEIGHT - 100, self.base_image)

    @staticmethod
    def _get_config_path():
        curr_dir = os.path.dirname(__file__)
        return os.path.join(curr_dir, "config.txt")


if __name__ == "__main__":
    flappy = Flappy()
    active = True
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    flappy.basic_play()
                if event.key == pygame.K_2:
                    flappy.neat_lib_play()
                if event.key == pygame.K_3:
                    flappy.neat_self_impl_play()
        flappy.intro_screen()

    pygame.quit()
    quit()
