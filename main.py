import pygame
import neat
import time
import os
import random

pygame.font.init()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800

IMAGES_DIR_PREFIX = "images"


def load_image(dir, fn):
    return pygame.image.load(os.path.join(dir, fn))


BIRD_IMAGES = [
    pygame.transform.scale2x(load_image(IMAGES_DIR_PREFIX, "bird2.png")), # wings up
    pygame.transform.scale2x(load_image(IMAGES_DIR_PREFIX, "bird1.png")), # wings normal
    pygame.transform.scale2x(load_image(IMAGES_DIR_PREFIX, "bird3.png")), # wings down
]
PIPE_IMAGE = pygame.transform.scale2x(load_image(IMAGES_DIR_PREFIX, "pipe.png"))
BASE_IMAGE = pygame.transform.scale2x(load_image(IMAGES_DIR_PREFIX, "base.png"))
BG_IMAGE = load_image(
    IMAGES_DIR_PREFIX, "bg.png"
)  # BG is originally designed in 600x800

STAT_FONT = pygame.font.SysFont("comicsans", 50)

class Bird:
    IMAGES = BIRD_IMAGES
    MAX_ROTATION = 25
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        """Init method for a new bird.

        Sets the initial xy-position, the tilt of the object on screen, physics of our bird, the initial image taken for drawing to screen...
        """
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMAGES[0]

    def jump(self):
        """Method for calculating jumps.

        Negative velocity in y-direction is needed to move the bird upwards. tick_count, height and move are set to calculate physics and direction.
        """
        self.velocity = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        d = self.velocity * self.tick_count + 1.5 * self.tick_count**2 # calculate y-direction

        if d >= 16: # terminal velocity
            d = 16
        
        if d < 0:
            d -= 2 # TODO: adjust this later for move tuning
        
        self.y = self.y + d

        if d < 0 or self.y < self.height + 50: # check if we are still in a jump motion or starting to fall
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90: # make the bird do a nose dive
                self.tilt -= self.ROTATION_VELOCITY

    def draw(self, window):
        self.img_count += 1 # keep track of how the bird image we're showing

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMAGES[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMAGES[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMAGES[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMAGES[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMAGES[0]
            self.img_count = 0

        if self.tilt <= -80: # if bird is nose-diving, show falling image
            self.img = self.IMAGES[1]
        
        # when tilting, instead of tilting around (0,0) which is the upper left corner
        # tilt it around its own axis
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rectangle = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        window.blit(rotated_image, new_rectangle.topleft)

    def get_mask(self): # TODO: explain
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 200 # how much space is between our pipes?
    VELOCITY = 5 # pipes are actually moving towards the bird

    def __init__(self, x=random.randrange(600,750)):
        self.x = x
        self.height = 0
        self.gap = 100

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMAGE, False, True)
        self.PIPE_BOTTOM = PIPE_IMAGE # one Pipe instance actually contains two that behave like one object

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height() # we possibly draw the pipe starting in a negative location, this is wanted
        self.bottom = self.height + self.GAP # place the bottom pipe
    
    def move(self):
        self.x -= self.VELOCITY
    
    def draw(self, window):
        window.blit(self.PIPE_TOP, (self.x, self.top))
        window.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
    
    def collide(self, bird):
        bird_pixelmask = bird.get_mask()
        top_pixelmask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_pixelmask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_pixelmask.overlap(bottom_pixelmask, bottom_offset)
        t_point = bird_pixelmask.overlap(top_pixelmask, top_offset)
        if t_point or b_point:
            return True

class Base:
    VELOCITY = 5
    WIDTH = BASE_IMAGE.get_width()
    IMG = BASE_IMAGE

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
    
    def move(self):
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, window):
        window.blit(self.IMG, (self.x1, self.y))
        window.blit(self.IMG, (self.x2, self.y))


def draw_window(window: pygame.Surface, bird: Bird, pipes: list[Pipe], base: Base, score):
    window.blit(BG_IMAGE, (0,0)) # TODO: Should be a moving object, moving muuuuuch slower than the rest so we have some kind of "journey"


    for pipe in pipes:
        pipe.draw(window)
    
    text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
    window.blit(text, (WINDOW_WIDTH - 10 - text.get_width(), 10))

    base.draw(window)

    bird.draw(window)
    pygame.display.update()

def main():
    print("Started main loop...")
    bird = Bird(230,350)
    base = Base(730)
    pipes = [Pipe(700)]
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    run = True

    score = 0

    while run:
        add_pipe = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                print("Received quit event...")
        remove = []
        for pipe in pipes:
            if pipe.collide(bird):
                pass

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                remove.append(pipe)
            
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

            pipe.move()
        if add_pipe:
            score += 1
            pipes.append(Pipe())

        for r in remove:
            pipes.remove(r)


        base.move()
        draw_window(window=window, bird=bird, pipes=pipes, base=base, score=score)
    print("Quitting...")
    pygame.quit()
    quit()

if __name__=="__main__":
    print("Invoked as main program, starting main loop...")
    main()
