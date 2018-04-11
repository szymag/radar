import pygame, sys
from pygame.locals import *


def rotate_radar(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


def print_objects(*args):
    for i in args:
        screen.blit(*i)


if __name__ == "__main__":

    pygame.init()
    window = pygame.display.set_mode((938, 1025))

    pygame.display.set_caption('Radar')
    background = pygame.image.load('background.png')
    radar = pygame.image.load('radar.png')
    red_airplane = pygame.image.load('red_airplane.png')
    green_airplane = pygame.image.load('green_airplane.png')

    screen = pygame.display.get_surface()
    print_objects((background, (0, 0)), (green_airplane, (500, 700)),
                  (green_airplane, (300, 300)), (red_airplane, (600, 600)),
                  (radar, (0, 90)))
    pygame.display.flip()

    angle = 0

    while True:
        rot_radar = radar
        rot_radar = rotate_radar(rot_radar, angle)
        print_objects((background, (0, 0)), (green_airplane, (500, 700)),
                      (green_airplane, (300, 300)), (red_airplane, (600, 600)),
                      (rot_radar, (0, 90)))

        pygame.display.update()
        angle += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
