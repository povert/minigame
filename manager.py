# -*- coding: utf-8 -*-

import sys,time
import pygame
import my_ui
from defines import *

class Manager:
	
	SCENE_SIZE = (700, 1000)
	FPS_LIMIT = 60

	def __init__(self):
		self.scene = pygame.display.set_mode(Manager.SCENE_SIZE)
		self.clock = pygame.time.Clock()
		self.curgame = None 
		self.game_list = []
		self.game_menu = {}
		self.button_dict = {}
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
				elif event.type == pygame.MOUSEMOTION:
					self.deal_mousemotion_event(event)

			self.draw_background()
			if self.curgame is None:
				self.draw_menu()
			else:
				self.draw_game()
			self.draw_FPS()
			pygame.display.update()
			self.clock.tick(Manager.FPS_LIMIT)
		self.quit()

	def init_run(self):
		self.game_menu = {}
		for i, game in enumerate(self.game_list):
			if i >= 22:		# 先只支持显示22个，后面做的多了在做分页处理
				break
			x = 50 if i % 2 == 0 else Manager.SCENE_SIZE[0] // 2
			y = 120 + i // 2 * 60
			game_text_ui = my_ui.My_TextUI("%s：%s"%(i + 1, game.name), 30, BLACK)
			game_text_ui.set_hover_color(RED)
			game_text_ui.set_hover_size(32)
			game_text_ui.draw(self.scene, x = x, y = y)
			self.game_menu[i] = game_text_ui
		self.button_dict["home"] = my_ui.My_TextUI("返回", 30, BLACK)
		self.button_dict["home"].set_hover_color(RED)
		self.button_dict["home"].set_hover_size(40)
		self._fps_info = [int(time.time()), 0, Manager.FPS_LIMIT]

	def draw_background(self):
		deal_image_func=Function(pygame.transform.scale, args = [Manager.SCENE_SIZE,])
		deal_image_func.args_backward()
		draw_image(self.scene,"./images/background.jpg", deal_image_func = deal_image_func, x = 0, y = 0)

	def draw_menu(self):
		draw_text(self.scene, "菜单列表", 40, BLACK, y = 50)
		for i, game_text_ui in self.game_menu.items():
			if self.select_game == i:
				game_text_ui.set_hover(True)
			else:
				game_text_ui.set_hover(False)
			game_text_ui.draw(self.scene)

	def draw_game(self):
		draw_text(self.scene, self.curgame.name, 40, BLACK, y = 50)
		self.button_dict["home"].draw(self.scene, y = 840)
		self.curgame.draw()
		self.scene.blit(self.curgame.scene, (0, 120))

	def draw_FPS(self):
		t = int(time.time())
		if t == self._fps_info[0]:
			self._fps_info[1] += 1
		else:
			self._fps_info = [t, 1, self._fps_info[1]]
		draw_text(self.scene, "FPS: %d"%self._fps_info[2], 24, GREY, (Manager.SCENE_SIZE[0] - 110), 20)


	def deal_keydown_event(self, event):
		if event.key == pygame.K_ESCAPE:
			if self.curgame:
				self.curgame.end()
				self.curgame = None
			else:
				self.running = False
			return
		if self.curgame:
			self.curgame.deal_keydown_event(event)
			return
		if event.key == pygame.K_DOWN:
			self.select_game = max(0, min(len(self.game_list) - 2, self.select_game + 2))
		elif event.key == pygame.K_UP:
			self.select_game = max(0, min(len(self.game_list) - 2, self.select_game - 2))
		elif event.key == pygame.K_LEFT:
			self.select_game = max(0, min(len(self.game_list) - 1, self.select_game - self.select_game % 2))
		elif event.key == pygame.K_RIGHT:
			self.select_game = max(0, min(len(self.game_list) - 1, self.select_game + (self.select_game + 1) % 2))
		elif event.key == pygame.K_RETURN:
			self.curgame = self.game_list[self.select_game]

	def deal_mousebuttondown_event(self, event):
		if self.curgame:
			if self.button_dict["home"].collidepoint(event.pos):
				self.button_dict["home"].set_hover(False)
				self.curgame.end()
				self.curgame = None
				return
			self.curgame.deal_mousebuttondown_event(event)
			return
		if self.game_menu[self.select_game].collidepoint(event.pos):
			self.curgame = self.game_list[self.select_game]
			self.curgame.start()

	def deal_mousebuttonup_event(self, event):
		if self.curgame:
			self.curgame.deal_mousebuttonup_event(event)
			return
		pass

	def deal_mousemotion_event(self, event):
		if self.curgame:
			self.curgame.deal_mousemotion_event(event)
			self.button_dict["home"].set_hover(self.button_dict["home"].collidepoint(event.pos))
			return
		for i, game_text_ui in self.game_menu.items():
			if game_text_ui.collidepoint(event.pos):
				self.select_game = i

	def quit(self):
		pygame.quit()
		sys.exit()
