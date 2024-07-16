import pygame
import neat
import time
import os
import random

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800

IMAGES_DIR_PREFIX="images"

def load_image(dir, fn):
    return pygame.image.load(os.path.join(dir,fn))


BIRD_IMAGES = [pygame.transform.scale2x(load_image(IMAGES_DIR_PREFIX, "bird1.png")), pygame.transform.scale2x(load_image(IMAGES_DIR_PREFIX, "bird2.png")), pygame.transform.scale2x(load_image(IMAGES_DIR_PREFIX, "bird2.png"))]
PIPE_IMAGE = pygame.transform.scale2x(load_image(IMAGES_DIR_PREFIX, "pipe.png"))
BASE_IMAGE = pygame.transform.scale2x(load_image(IMAGES_DIR_PREFIX, "base.png"))
BG_IMAGE = load_image(IMAGES_DIR_PREFIX, "bg.png") # BG is originally designed in 600x800


class Bird:
    IMAGES = BIRD_IMAGES
    MAX_ROTATION = 25
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMAGES[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):


while True:
    bird.move()