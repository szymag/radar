import pygame
import sys
import os
import time
import subprocess
import math

from pygame.locals import *
from text_box import TextBox

window = pygame.display.set_mode((1024, 768))
key_words = ['40401010', 'test', 'test', 'test', 'test']
radar_center = (0, 61)
working_time = 30 * 60


class Graphics:
    def __init__(self, graphic, init_position):
        self.init_position = init_position
        self.graphic = graphic
        self.time = 0

    def position(self):
        return self.init_position

    def name(self):
        return self.graphic

    def tim(self):
        return self.time


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
        screen.blit(i.name(), i.position())


def calculate_common_angle(position):
    radar_shift = (320, 320)
    x = position[0] - radar_shift[0] - radar_center[0]
    y = position[1] - radar_shift[1] - radar_center[1]
    return 180 - abs(math.degrees(math.atan2(x, y)))


def calculate_movement(time_part, meteor):
    pl_position = meteor.position()
    center = radar_center[0] + 320, radar_center[1] + 320
    distance = center[0] - pl_position[0], center[1] - pl_position[1]
    movement = [i - (1 - (time_part / working_time)) * i for i, j in zip(distance, center)]
    return pl_position[0] + movement[0], pl_position[1] + movement[1]


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.get_surface()

    input_box1 = TextBox(700, 300, 140, 32)
    input_box2 = TextBox(700, 350, 140, 32)
    input_box3 = TextBox(700, 400, 140, 32)
    input_box4 = TextBox(700, 450, 140, 32)
    input_box5 = TextBox(700, 500, 140, 32)

    input_boxes = [input_box1, input_box2, input_box3, input_box4, input_box5]
    [i.draw(screen) for i in input_boxes]

    pygame.display.set_caption('Radar')
    background = pygame.image.load('background.png')
    radar = pygame.image.load('radar.png')
    red_meteor = pygame.image.load('red_meteor.png')
    green_meteor = pygame.image.load('green_meteor.png')
    alpha = pygame.image.load('alpha.png')
    beta = pygame.image.load('beta.png')
    gamma = pygame.image.load('gamma.png')
    delta = pygame.image.load('delta.png')
    lambda_ = pygame.image.load('lambda.png')
    text = pygame.image.load('text.png')
    background = Graphics(background, (0, 0))
    meteor_1 = Graphics(green_meteor, (40, 170))
    meteor_2 = Graphics(green_meteor, (100, 210))
    meteor_3 = Graphics(green_meteor, (20, 300))
    meteor_4 = Graphics(green_meteor, (250, 70))
    meteor_5 = Graphics(green_meteor, (60, 400))
    alpha = Graphics(alpha, (670, 305))
    beta = Graphics(beta, (670, 350))
    gamma = Graphics(gamma, (670, 405))
    delta = Graphics(delta, (670, 450))
    lambda_ = Graphics(lambda_, (670, 500))
    text = Graphics(text, (700, 240))
    printed_objects = [background, meteor_1, meteor_2, meteor_3, meteor_4, meteor_5,
                       alpha, beta, gamma, delta, lambda_, text]
    print_objects(*printed_objects)

    effect = pygame.mixer.music.load('radar_sound.wav')
    pygame.mixer.music.play()
    SONG_END = pygame.USEREVENT + 1
    pygame.mixer.music.set_endevent(SONG_END)

    radar_angle = 0
    condition = True
    start_time = time.time()
    while condition:
        current_time = time.time() - start_time
        if all(i[0] == i[1] for i in zip(key_words,
                                         (input_box1.text, input_box2.text,
                                          input_box3.text, input_box4.text, input_box5.text))):
            condition = False

        if input_box1.text == key_words[0]:
            setattr(meteor_1, 'graphic', red_meteor)
        else:
            setattr(meteor_1, 'graphic', green_meteor)
        if input_box2.text == key_words[1]:
            setattr(meteor_2, 'graphic', red_meteor)
        else:
            setattr(meteor_2, 'graphic', green_meteor)
        if input_box3.text == key_words[2]:
            setattr(meteor_3, 'graphic', red_meteor)
        else:
            setattr(meteor_3, 'graphic', green_meteor)
        if input_box4.text == key_words[3]:
            setattr(meteor_4, 'graphic', red_meteor)
        else:
            setattr(meteor_4, 'graphic', green_meteor)
        if input_box5.text == key_words[4]:
            setattr(meteor_5, 'graphic', red_meteor)
        else:
            setattr(meteor_5, 'graphic', green_meteor)

        if abs(radar_angle - calculate_common_angle(meteor_1.position()) - 2) < 0.5:
            setattr(meteor_1, 'init_position', calculate_movement(current_time - meteor_1.tim(), meteor_1))
            setattr(meteor_1, 'time', current_time)
        if abs(radar_angle - calculate_common_angle(meteor_2.position()) - 2) < 0.5:
            setattr(meteor_2, 'init_position', calculate_movement(current_time - meteor_2.tim(), meteor_2))
            setattr(meteor_2, 'time', current_time)
        if abs(radar_angle - calculate_common_angle(meteor_3.position()) - 2) < 0.5:
            setattr(meteor_3, 'init_position', calculate_movement(current_time - meteor_3.tim(), meteor_3))
            setattr(meteor_3, 'time', current_time)
        if abs(radar_angle - calculate_common_angle(meteor_4.position()) - 2) < 0.5:
            setattr(meteor_4, 'init_position', calculate_movement(current_time - meteor_4.tim(), meteor_4))
            setattr(meteor_4, 'time', current_time)
        if abs(radar_angle - calculate_common_angle(meteor_5.position())) < 0.5:
            setattr(meteor_5, 'init_position', calculate_movement(current_time - meteor_5.tim(), meteor_5))
            setattr(meteor_5, 'time', current_time)

        rot_radar = rotate_radar(radar, radar_angle)
        print_objects(*printed_objects)
        screen.blit(rot_radar, radar_center)

        pygame.display.update()
        radar_angle += 1
        radar_angle %= 360
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            if event.type == SONG_END:
                pygame.mixer.music.play()
            for box in input_boxes:
                box.handle_event(event)
        screen.fill((30, 30, 30))
        for box in input_boxes:
            box.draw(screen)
    pygame.mixer.music.stop()
    time.sleep(2)
    if os.path.islink("/home/szymag/python/escape_room/movie.mp4"):
        subprocess.call(['/usr/bin/xplayer', '/home/szymag/python/escape_room/movie.mp4'])
    sys.exit(0)
