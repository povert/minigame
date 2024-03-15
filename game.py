# -*- coding: utf-8 -*-

import sys
import pygame


class Game:

	scene_SIZE = (700, 700)

	def __init__(self, manager):
		self.manager = manager
		self.scene = pygame.Surface(Game.scene_SIZE)
		self.absolute_point = (0, 120) # 记录场景的绝对坐标转换

	def start(self):
		pass

	def end(self):
		pass

	def deal_keydown_event(self, event):
		pass

	def deal_mousebuttondown_event(self, event):
		pass

	def deal_mousebuttonup_event(self, event):
		pass

	def deal_mousemotion_event(self, event):
		pass

	def draw(self):
		pass

	@property
	def name(self):
		return "小游戏"
