# -*- coding: utf-8 -*-

import time
import pygame
import objects
from defines import *

class GameMenu(object):

	SCENE_SIZE = (700, 1000)
	FPS_LIMIT = 60

	def __init__(self):
		self.scene = pygame.display.set_mode(GameMenu.SCENE_SIZE)
		self.clock = pygame.time.Clock()
		self.backgroud = get_image_surface("./images/background.jpg")
		self.backgroud = pygame.transform.scale(self.backgroud, GameMenu.SCENE_SIZE)
		self.curgame = None 
		self.game_list = []
		self.game_menu = {}
		self.custom_mouseUI = {}
		self.running = False
		self.select_game = 0
		self.page = 0
		self._fps_info = [0, 0, 0]

	def add_game(self, game):
		self.game_list.append(game)
	
	def run(self):
		self.running = True
		self.init_run()
		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
					break
				elif event.type == pygame.KEYDOWN:
					self.deal_keydown_event(event)
				elif event.type == pygame.MOUSEBUTTONDOWN:
					self.deal_mousebuttondown_event(event)
				elif event.type == pygame.MOUSEBUTTONUP:
					self.deal_mousebuttonup_event(event)
				elif event.type == pygame.MOUSEMOTION:
					self.deal_mousemotion_event(event)
			self.draw()
			pygame.display.update()
			self.clock.tick(GameMenu.FPS_LIMIT)
		self.quit()
	
	def init_run(self):
		self.game_menu = {}
		self.custom_mouseUI = {}
		for i, game in enumerate(self.game_list):
			if i >= 22:		# 先只支持显示22个，后面做的多了在做分页处理
				break
			x = 50 if i % 2 == 0 else GameMenu.SCENE_SIZE[0] // 2
			y = 120 + i // 2 * 60
			game_text_ui = objects.MyUIText("%s：%s"%(i + 1, game.name), 30, BLACK)
			game_text_ui.set_hover_color(RED)
			game_text_ui.set_hover_size(32)
			game_text_ui.set_pos((x, y))
			self.game_menu[i] = game_text_ui
		self.custom_mouseUI["home"] = objects.MyUIText("返回主菜单", 30, BLACK)
		self.custom_mouseUI["home"].set_hover_color(RED)
		self.custom_mouseUI["home"].set_hover_size(40)
		self.custom_mouseUI["home"].set_click_func(self.go_home)
		self._fps_info = [int(time.time()), 0, GameMenu.FPS_LIMIT]

	def start_game(self, index):
		if self.curgame:
			self.curgame.quit()
		self.curgame = self.game_list[index]
		self.select_game = index
		self.curgame.start()

	def go_home(self):
		if not self.curgame:
			return
		self.curgame.quit()
		self.curgame = None

	def deal_keydown_event(self, event):
		if event.key == pygame.K_ESCAPE:
			if self.curgame:
				self.curgame.quit()
				self.curgame = None
			else:
				self.running = False
			return
		if self.curgame:
			self.curgame.deal_keydown_event(event)
		else:
			self.on_keydown_event(event)
	
	def on_keydown_event(self, event):
		if event.key == pygame.K_DOWN:
			self.select_game = max(0, min(len(self.game_list) - (self.select_game % 2 + 1), self.select_game + 2))
		elif event.key == pygame.K_UP:
			self.select_game = max(0, min(len(self.game_list) - (self.select_game % 2 + 1), self.select_game - 2))
		elif event.key == pygame.K_LEFT:
			self.select_game = max(0, min(len(self.game_list) - 1, self.select_game - self.select_game % 2))
		elif event.key == pygame.K_RIGHT:
			self.select_game = max(0, min(len(self.game_list) - 1, self.select_game + (self.select_game + 1) % 2))
		elif event.key == pygame.K_RETURN:
			self.start_game(self.select_game)

	def deal_mousebuttondown_event(self, event):
		for customUI in self.custom_mouseUI.values():
			customUI.check_mouse(event.pos, pygame.MOUSEBUTTONDOWN)
		if self.curgame:
			self.curgame.deal_mousebuttondown_event(event)

	def deal_mousebuttonup_event(self, event):
		for customUI in self.custom_mouseUI.values():
			customUI.check_mouse(event.pos, pygame.MOUSEBUTTONUP)
		if self.curgame:
			self.curgame.deal_mousebuttonup_event(event)
		else:
			for i, game_text_ui in self.game_menu.items():
				if game_text_ui.collidepoint(event.pos):
					self.start_game(i)
					break

	def deal_mousemotion_event(self, event):
		for customUI in self.custom_mouseUI.values():
			customUI.check_mouse(event.pos, pygame.MOUSEMOTION)
		if self.curgame:
			self.curgame.deal_mousemotion_event(event)
		else:
			for i, game_text_ui in self.game_menu.items():
				if game_text_ui.collidepoint(event.pos):
					self.select_game = i
					break

	def draw(self):
		self.scene.blit(self.backgroud, (0, 0))
		if self.curgame:
			game_name = get_text_surface(self.curgame.name, 40, BLACK)
			x = GameMenu.SCENE_SIZE[0] // 2 - game_name.get_width() // 2
			self.scene.blit(game_name, (x, 50))
			self.custom_mouseUI["home"].draw(self.scene, (None, 840))
			self.curgame.draw(self.scene)
		else:
			self.scene.blit(get_text_surface("游戏菜单", 40, BLACK), (GameMenu.SCENE_SIZE[0] // 2 - 100, 50))
			self.draw_menu()
		self.draw_fps()

	def draw_menu(self):
		for i, game_text_ui in self.game_menu.items():
			if i == self.select_game:
				game_text_ui.is_hover = True
			else:
				game_text_ui.is_hover = False
			game_text_ui.draw(self.scene)

	def draw_fps(self):
		t = int(time.time())
		if t == self._fps_info[0]:
			self._fps_info[1] += 1
		else:
			self._fps_info = [t, 1, self._fps_info[1]]
		fps_text = get_text_surface("FPS: %d"%self._fps_info[2], 24, GREY)
		self.scene.blit(fps_text, (GameMenu.SCENE_SIZE[0] - 110, 20))

	def quit(self):
		if self.curgame:
			self.curgame.quit()
		pygame.quit()



