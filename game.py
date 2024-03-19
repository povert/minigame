# -*- coding: utf-8 -*-

import sys
import pygame


class Game:

	scene_SIZE = (700, 700)

	def __init__(self, manager):
		self.manager = manager
		self.scene = pygame.Surface(Game.scene_SIZE)
		self.abs_offset = (0, 120) # 记录场景的绝对坐标转换
		self.custom_mouseUI = {} # 自定义鼠标事件相关的UI

	def start(self):
		pass

	def end(self):
		pass
	
	def quit(self):
		self.end()

	def deal_keydown_event(self, event):
		self.on_keydown(event)
	
	def on_keydown(self, event):
		pass

	def deal_mousebuttondown_event(self, event):
		for customUI in self.custom_mouseUI.values():
			customUI.check_mouse(event.pos, pygame.MOUSEBUTTONDOWN)
		self.on_mousebuttondown(event)
	
	def on_mousebuttondown(self, event):
		pass

	def deal_mousebuttonup_event(self, event):
		for customUI in self.custom_mouseUI.values():
			customUI.check_mouse(event.pos, pygame.MOUSEBUTTONUP)
		self.on_mousebuttonup(event)
	
	def on_mousebuttonup(self, event):
		pass

	def deal_mousemotion_event(self, event):
		for customUI in self.custom_mouseUI.values():
			customUI.check_mouse(event.pos, pygame.MOUSEMOTION)
		self.on_mousemotion(event)
	
	def on_mousemotion(self, event):
		pass

	def deal_mousewheel_event(self, event):
		self.on_mousewheel(event)
	
	def on_mousewheel(self, event):
		pass

	def draw(self, surface):
		self.draw_background()
		self.draw_customUI()
		self.custom_draw()
		surface.blit(self.scene, self.abs_offset)

	def draw_background(self):
		self.scene.fill((255, 255, 255))

	def draw_customUI(self):
		for customUI in self.custom_mouseUI.values():
			customUI.draw(self.scene)

	def custom_draw(self):
		pass

	@property
	def name(self):
		return "小游戏"

	@property
	def is_change(self):
		for self.customUI in self.customUI.values():
			if self.customUI.is_change:
				return True
		return self._is_change