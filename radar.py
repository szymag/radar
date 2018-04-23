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


def calculate_movement(time_part, plane):
    pl_position = plane.position()
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
    red_airplane = pygame.image.load('red_airplane.png')
    green_airplane = pygame.image.load('green_airplane.png')
    background = Graphics(background, (0, 0))
    plane_1 = Graphics(green_airplane, (60, 170))
    plane_2 = Graphics(green_airplane, (100, 210))
    plane_3 = Graphics(green_airplane, (30, 300))
    plane_4 = Graphics(green_airplane, (250, 70))
    plane_5 = Graphics(green_airplane, (60, 400))
    printed_objects = [background, plane_1, plane_2, plane_3, plane_4, plane_5]
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
            setattr(plane_1, 'graphic', red_airplane)
        else:
            setattr(plane_1, 'graphic', green_airplane)
        if input_box2.text == key_words[1]:
            setattr(plane_2, 'graphic', red_airplane)
        else:
            setattr(plane_2, 'graphic', green_airplane)
        if input_box3.text == key_words[2]:
            setattr(plane_3, 'graphic', red_airplane)
        else:
            setattr(plane_3, 'graphic', green_airplane)
        if input_box4.text == key_words[3]:
            setattr(plane_4, 'graphic', red_airplane)
        else:
            setattr(plane_4, 'graphic', green_airplane)
        if input_box5.text == key_words[4]:
            setattr(plane_5, 'graphic', red_airplane)
        else:
            setattr(plane_5, 'graphic', green_airplane)

        if abs(radar_angle - calculate_common_angle(plane_1.position()) - 2) < 0.5:
            setattr(plane_1, 'init_position', calculate_movement(current_time - plane_1.tim(), plane_1))
            setattr(plane_1, 'time', current_time)
        if abs(radar_angle - calculate_common_angle(plane_2.position()) - 2) < 0.5:
            setattr(plane_2, 'init_position', calculate_movement(current_time - plane_2.tim(), plane_2))
            setattr(plane_2, 'time', current_time)
        if abs(radar_angle - calculate_common_angle(plane_3.position()) - 2) < 0.5:
            setattr(plane_3, 'init_position', calculate_movement(current_time - plane_3.tim(), plane_3))
            setattr(plane_3, 'time', current_time)
        if abs(radar_angle - calculate_common_angle(plane_4.position()) - 2) < 0.5:
            setattr(plane_4, 'init_position', calculate_movement(current_time - plane_4.tim(), plane_4))
            setattr(plane_4, 'time', current_time)
        if abs(radar_angle - calculate_common_angle(plane_5.position())) < 0.5:
            setattr(plane_5, 'init_position', calculate_movement(current_time - plane_5.tim(), plane_5))
            setattr(plane_5, 'time', current_time)

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
