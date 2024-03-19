# -*- coding: utf-8 -*-

'''各种自定义通用对象'''


import weakref
import pygame
from defines import get_text_surface, get_image_surface, BLACK

class MyUIText:
	def __init__(self, text, font_size = 24, font_color = BLACK, abs_offset = (0, 0)):
		self.text = text
		self.font_size = font_size
		self.hover_size = font_size
		self.click_size = font_size
		self.font_color = font_color
		self.hover_color = font_color
		self.click_color = font_color
		self.is_hover = False
		self.is_click = False
		self.click_func = None
		self.abs_offset = abs_offset
		self.text_rect = None

	def set_hover_size(self, size):
		self.hover_size = size

	def set_hover_color(self, color):
		self.hover_color = color

	def set_click_size(self, size):
		self.click_size = size

	def set_click_color(self, color):
		self.click_color = color

	def set_click_func(self, func):
		self.click_func = func

	def draw(self, surface, pos = None, abs_offset = None):
		text_surface = get_text_surface(self.text, self.size, self.color)
		if pos is None and self.text_rect:
			text_rect = self.text_rect
		else:
			x, y = pos
			if x is None:
				x = (surface.get_width() - text_surface.get_width())//2
			if y is None:
				y = (surface.get_height() - text_surface.get_height())//2
			text_rect = text_surface.get_rect(topleft=(x, y))
		surface.blit(text_surface, text_rect)
		self.text_rect = text_rect
		self.abs_offset = abs_offset if abs_offset else self.abs_offset

	def check_mouse(self, mouse_pos, mousebutton_state = None):
		is_collidepoint = self.collidepoint(mouse_pos)
		self.is_hover = is_collidepoint
		self.is_click =  mousebutton_state == pygame.MOUSEBUTTONDOWN and is_collidepoint
		if self.click_func and is_collidepoint and mousebutton_state == pygame.MOUSEBUTTONUP:
			self.click_func()
		
	def collidepoint(self, pos):
		if not self.text_rect:
			return False
		abs_x, abs_y = self.abs_offset
		pos_x, pos_y = pos
		w, h = self.text_rect.size
		x, y = self.text_rect.x + abs_x, self.text_rect.y + abs_y
		if pos_x < x or pos_x > x + w:
			return False
		if pos_y < y or pos_y > y + h:
			return False
		return True

	@property
	def size(self):
		if self.is_click:
			return self.click_size
		elif self.is_hover:
			return self.hover_size
		return self.font_size

	@property
	def color(self):
		if self.is_click:
			return self.click_color
		elif self.is_hover:
			return self.hover_color
		return self.font_color

class MyUIImage:
	def __init__(self, image_path, image_size = None, abs_offset = (0, 0)):
		self.image_path = image_path
		self.hover_image = self.image_path
		self.click_image = self.image_path
		self.image_size = image_size
		self.hover_size = image_size
		self.click_size = image_size
		self.abs_offset = abs_offset
		self.click_func = None
		self.is_hover = False
		self.is_click = False
		self.image_rect = None

	def set_hover_image(self, image_path):
		self.hover_image = image_path

	def set_click_image(self, image_path):
		self.click_image = image_path

	def set_hover_size(self, size):
		self.hover_size = size

	def set_click_size(self, size):
		self.click_size = size

	def set_click_func(self, func):
		self.click_func = func

	def draw(self, surface, pos = None, abs_offset = None):
		image_surface = get_image_surface(self.image)
		image_size = self.size
		if image_size:
			image_surface = pygame.transform.scale(image_surface, image_size)
		if pos is None and self.image_rect:
			image_rect = self.image_rect
		else:
			x, y = pos
			if x is None:
				x = (surface.get_width() - image_surface.get_width())//2
			if y is None:
				y = (surface.get_height() - image_surface.get_height())//2
			image_rect = image_surface.get_rect(topleft=(x, y))
		surface.blit(image_surface, image_rect)
		self.image_rect = image_rect
		self.abs_offset = abs_offset if abs_offset else self.abs_offset

	def check_mouse(self, mouse_pos, mousebutton_state = None):
		is_collidepoint = self.collidepoint(mouse_pos)
		self.is_hover = is_collidepoint
		self.is_click =  mousebutton_state == pygame.MOUSEBUTTONDOWN and is_collidepoint
		if self.click_func and is_collidepoint and mousebutton_state == pygame.MOUSEBUTTONUP:
			self.click_func()

	def collidepoint(self, pos):
		if not self.image_rect:
			return False
		abs_x, abs_y = self.abs_offset
		pos_x, pos_y = pos
		w, h = self.image_rect.size
		x, y = self.image_rect.x + abs_x, self.image_rect.y + abs_y
		if pos_x < x or pos_x > x + w:
			return False
		if pos_y < y or pos_y > y + h:
			return False
		return True
	
	@property
	def image(self):
		if self.is_click:
			return self.click_image
		elif self.is_hover:
			return self.hover_image
		return self.image_path

	@property
	def size(self):
		if self.is_click:
			return self.click_size
		elif self.is_hover:
			return self.hover_size
		return self.image_size

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

