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

FONT_DICT = {}
IMAGE_DICT = {}

def get_text_surface(text, size, color):
	if size not in FONT_DICT:
		FONT_DICT[size] = pygame.font.Font("./font/simkai.ttf", size)
	font = FONT_DICT[size]	
	text_surface = font.render(text, True, color)
	return text_surface

def draw_text(surface, text, size, color, x = None, y = None):
	if size not in FONT_DICT:
		FONT_DICT[size] = pygame.font.Font("./font/simkai.ttf", size)
	font = FONT_DICT[size]
	text_surface = font.render(text, True, color)
	if x is None:
		x = (surface.get_width() - text_surface.get_width())//2
	if y is None:
		y = (surface.get_height() - text_surface.get_height())//2
	text_rect = text_surface.get_rect(topleft=(x, y))
	surface.blit(text_surface, text_rect)
	return text_rect

def draw_surface(target_surface, source_surface, x = None, y = None):
	if x is None:
		x = (target_surface.get_width() - source_surface.get_width())//2
	if y is None:
		y = (target_surface.get_height() - source_surface.get_height())//2
	surface_rect = source_surface.get_rect(topleft=(x, y))
	target_surface.blit(source_surface, surface_rect)
	return surface_rect

def get_image_surface(image_name):
	if image_name not in IMAGE_DICT:
		IMAGE_DICT[image_name] = pygame.image.load(image_name)
	return IMAGE_DICT[image_name]

def draw_image(target_surface, image_name, x = None, y = None, deal_image_func = None):
	if image_name not in IMAGE_DICT:
		IMAGE_DICT[image_name] = pygame.image.load(image_name)
	image = IMAGE_DICT[image_name]
	if x is None:
		x = (target_surface.get_width() - image.get_width())//2
	if y is None:
		y = (target_surface.get_height() - image.get_height())//2
	image_rect = image.get_rect(topleft=(x, y))
	if deal_image_func:
		image = deal_image_func(image)
	target_surface.blit(image, image_rect)
	return image_rect

class Function:

	def __init__(self, func, args = None, kwargs = None):
		self.func = func
		self.args = args if args is not None else []
		self.kwargs = kwargs if kwargs is not None else {}
		self.name = func.__name__
		self.backward = False

	def __call__(self, *args, **kwargs):
		if self.backward:
			all_args = list(args) + self.args
		else:
			all_args = self.args + list(args)
		all_kwargs = {**self.kwargs, **kwargs}
		return self.func(*all_args, **all_kwargs)

	@property
	def __name__(self):
		return self.name

	def args_backward(self):
		self.backward = True

class LFunction:

	def __init__(self, func, args = None, kwargs = None):
		self.func_ref = weakref.ref(func)  # 使用弱引用
		self.args = args if args is not None else []
		self.kwargs = kwargs if kwargs is not None else {}
		self.name = func.__name__
		self.backward = False

	def __call__(self, *args, **kwargs):
		func = self.func_ref()
		if func is None:
			return None
		if self.backward:
			all_args = list(args) + self.args
		else:
			all_args = self.args + list(args)
		all_kwargs = {**self.kwargs, **kwargs}
		return self.func(*all_args, **all_kwargs)

	def args_backward(self):
		self.backward = True

	@property
	def __name__(self):
		return self.name


