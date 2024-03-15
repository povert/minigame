# -*- coding: utf-8 -*-

import pygame
from defines import get_text_surface, get_image_surface

class My_TextUI:

	def __init__(self, text, font_size, font_color):
		self.text = text
		self.font_size = font_size
		self.hover_size = font_size
		self.click_size = font_size

		self.font_color = font_color
		self.hover_color = font_color
		self.click_color = font_color

		self.text_rect = None

		self.is_hover = False
		self.is_click = False

	def draw(self, surface, x = None, y = None, absolute_point = None):
		text_surface = get_text_surface(self.text, self.size, self.color)
		if x is None and y is None and self.text_rect:
			text_rect = self.text_rect
		else:
			if x is None:
				x = (surface.get_width() - text_surface.get_width())//2
			if y is None:
				y = (surface.get_height() - text_surface.get_height())//2
			text_rect = text_surface.get_rect(topleft=(x, y))
		surface.blit(text_surface, text_rect)
		self.text_rect = text_rect
		self.absolute_point = absolute_point if absolute_point else (0, 0)

	def set_rect(self, rect):
		self.text_rect = rect

	def set_surface(self, surface):
		self.surface = surface

	def set_hover_size(self, size):
		self.hover_size = size

	def set_hover_color(self, color):
		self.hover_color = color

	def set_click_size(self, size):
		self.click_size = size

	def set_click_color(self, color):
		self.click_color = color

	def set_hover(self, is_hover):
		self.is_hover = is_hover
	
	def set_click(self, is_click):
		self.is_click = is_click

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

	def collidepoint(self, pos):
		abs_x, abs_y = self.absolute_point
		pos_x, pos_y = pos
		w, h = self.text_rect.size
		x, y = self.text_rect.x + abs_x, self.text_rect.y + abs_y
		if pos_x < x or pos_x > x + w:
			return False
		if pos_y < y or pos_y > y + h:
			return False
		return True

class My_ButtonUI:
	
	def __init__(self, image_path, button_size = None):
		self.button_image = get_image_surface(image_path)
		if button_size:
			self.button_image = pygame.transform.scale(self.button_image, button_size)
		self.hover_image = self.button_image
		self.click_image = self.button_image
		self.button_rect = None

		self.button_size = button_size
		self.absolute_point = (0, 0)
		self.is_hover = False
		self.is_click = False
	
	def draw(self, surface, x = None, y = None, absolute_point = None):
		if x is None and y is None and self.button_rect:
			button_rect = self.button_rect
		else:
			if x is None:
				x = (surface.get_width() - self.button_image.get_width())//2
			if y is None:
				y = (surface.get_height() - self.button_image.get_height())//2
			button_rect = self.button_image.get_rect(topleft=(x, y))
		surface.blit(self.image, button_rect)
		self.button_rect = button_rect
		if absolute_point:
			self.absolute_point = absolute_point

	def set_rect(self, rect):
		self.button_rect = rect

	def set_surface(self, surface):
		self.surface = surface

	def set_hover_image(self, image_path):
		self.hover_image = get_image_surface(image_path)
		if self.button_size:
			self.hover_image = pygame.transform.scale(self.hover_image, self.button_size)

	def set_click_image(self, image_path):
		self.click_image = get_image_surface(image_path)
		if self.button_size:
			self.click_image = pygame.transform.scale(self.click_image, self.button_size)

	def set_hover(self, is_hover):
		self.is_hover = is_hover
	
	def set_click(self, is_click):
		self.is_click = is_click

	def collidepoint(self, pos):
		# 垃圾pygame，collectpoint就不会做相对坐标和绝对坐标转换，无法对我自定义平面绘制的按钮做碰撞检测
		# 需要我自己处理相对坐标和绝对坐标转换
		abs_x, abs_y = self.absolute_point
		pos_x, pos_y = pos
		w, h = self.button_rect.size
		x, y = self.button_rect.x + abs_x, self.button_rect.y + abs_y
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
		return self.button_image
