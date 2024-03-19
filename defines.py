# -*- coding: utf-8 -*-
import weakref
import pygame

BLACK = (0, 0, 0)	# 黑色
WHITE = (255, 255, 255)	# 白色
RED = (255, 0, 0)	# 红色
GREEN = (0, 255, 0)	# 绿色
BLUE = (0, 0, 255)	# 蓝色
YELLOW = (255, 255, 0)	# 黄色
PURPLE = (128, 0, 128)	# 紫色
GREY = (128, 128, 128)	# 灰色

FONT_DICT = {}
IMAGE_DICT = {}

def get_text_surface(text, size, color):
	if size not in FONT_DICT:
		FONT_DICT[size] = pygame.font.Font("./font/simkai.ttf", size)
	font = FONT_DICT[size]	
	text_surface = font.render(text, True, color)
	return text_surface

def get_image_surface(image_name):
	if image_name not in IMAGE_DICT:
		IMAGE_DICT[image_name] = pygame.image.load(image_name)
	return IMAGE_DICT[image_name]

