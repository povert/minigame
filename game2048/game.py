# -*- coding: utf-8 -*-

import numpy
import random
import pygame
import game
import my_ui
from defines import *


class Game(game.Game):

	NUM_COLOR_CONFIG = {
		0: (205, 192, 180),
		2: (238, 228, 218),
		4: (237, 224, 200),
		8: (242, 177, 121),
		16: (245, 149, 99),
		32: (246, 124, 95),
		64: (246, 94, 59),
		128: (237, 207, 114),
		256: (237, 204, 97),
		512: (237, 200, 80),
		1024: (237, 197, 63),
		2048: (237, 194, 46),
		4096: (237, 190, 29),
		8192: (237, 187, 12),
		16384: (237, 183, 0),
		32768: (237, 180, 0),
	}

	NUM_SIZE_CONFIG = {
		0: 42,
		2: 42,
		4: 42,
		8: 42,
		16: 40,
		32: 40,
		64: 40,
		128: 37,
		256: 37,
		512: 37,
		1024: 34,
		2048: 34,
		4096: 34,
		8192: 34,
		16384: 30,
		32768: 30
	}

	def __init__(self, manager):
		super().__init__(manager)
		self.max_score = 0
		self.sum_score = 0
		self.game_array = []
		self.game_surface = pygame.Surface((400, 700))	# 2048游戏数字区域
		self.button_dict = {}
		self.is_fail = False

	@property
	def name(self):
		return "2048"

	def start(self):
		self.button_dict["restart"] = my_ui.My_ButtonUI("./game2048/restart.png", button_size=(60, 60))
		self.game_start()

	def game_start(self):
		self.game_array = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
		self.is_fail = False
		self.max_score = 0
		self.sum_score = 0
		self.game_array[random.randint(0, 3)][random.randint(0, 3)] = 2

	def draw(self):
		self.scene.fill((28, 28, 28))
		self.game_surface.fill((136,119,119))
		self.draw_game_surface()
		self.draw_score()
		self.draw_tips()
		self.scene.blit(self.game_surface, (150, 0))

	def draw_game_surface(self):
		for x in range(4):
			for y in range(4):
				pos_x, pos_y = x * 100 + 10, y * 100 + 110
				num = self.game_array[x][y]
				blank_surface = pygame.Surface((80, 80))
				color = (237, 180, 0) if num > 32768 else Game.NUM_COLOR_CONFIG[num]
				blank_surface.fill(color)
				self.game_surface.blit(blank_surface, (pos_x, pos_y))
				if num!= 0:
					size = 30 if num > 32768 else Game.NUM_SIZE_CONFIG[num]
					text_surface = get_text_surface(str(num), size, BLACK)
					text_rect = text_surface.get_rect(center=(pos_x + 40, pos_y + 40))
					self.game_surface.blit(text_surface, text_rect)
				8

	def draw_score(self):
		source_surface = get_text_surface("分数", 42, WHITE)
		size = 30 if self.sum_score > 32768 else Game.NUM_SIZE_CONFIG[self.sum_score]
		source_value = get_text_surface(str(self.sum_score), size, WHITE)
		width = max(source_surface.get_width(), source_value.get_width()) + 16
		pos_x, pos_y = max(0, (200 - width) // 2) + 10, 530
		source_background = pygame.Surface((width, 140))
		source_background.fill((68, 68, 68))
		self.game_surface.blit(source_background, (pos_x, pos_y))

		pos2_x = pos_x + max(0, (width - source_surface.get_width())) // 2
		pos2_y = pos_y + max(0, (70 - source_surface.get_height())) // 2
		self.game_surface.blit(source_surface, (pos2_x, pos2_y))

		pos3_x = pos_x + max(0, (width - source_value.get_width())) // 2
		pos3_y = 590 + max(0, (70 - source_value.get_height())) // 2 
		self.game_surface.blit(source_value, (pos3_x, pos3_y))


		source_surface = get_text_surface("最高分", 40, WHITE)
		size = 30 if self.sum_score > 32768 else Game.NUM_SIZE_CONFIG[self.sum_score]
		source_value = get_text_surface(str(self.sum_score), size, WHITE)
		width = max(source_surface.get_width(), source_value.get_width()) + 16
		pos_x, pos_y = max(0, (200 - width) // 2) + 190, 530
		source_background = pygame.Surface((width, 140))
		source_background.fill((68, 68, 68))
		self.game_surface.blit(source_background, (pos_x, pos_y))

		pos2_x = pos_x + max(0, (width - source_surface.get_width())) // 2
		pos2_y = pos_y + max(0, (70 - source_surface.get_height())) // 2
		self.game_surface.blit(source_surface, (pos2_x, pos2_y))

		pos3_x = pos_x + max(0, (width - source_value.get_width())) // 2
		pos3_y = 590 + max(0, (70 - source_value.get_height())) // 2 
		self.game_surface.blit(source_value, (pos3_x, pos3_y))


	def draw_tips(self):
		size = 20
		if self.is_fail:
			tips = "游戏结束，(点击右侧按钮重新开始)"
		elif self.max_score <= 256:
			tips = "初试牛刀！"
			size = 30
		elif self.max_score <= 1024:
			tips = "加油，冲刺2048！"
			size = 30
		elif self.max_score <= 2048:
			tips = "完成挑战，(点击右侧按钮重新开始)"
		elif self.max_score <= 4096:
			tips = "登上新台阶，(点击右侧按钮重新开始)"
		elif self.max_score <= 8192:
			tips = "无人能及了，(点击右侧按钮重新开始)"
		else:
			tips = "难以想象的强，(点击右侧按钮重新开始)"
		top_surface = pygame.Surface((400, 80))
		top_surface.fill((93, 71, 139))
		self.game_surface.blit(top_surface, (0, 0))
		tips_surface = get_text_surface(tips, size, WHITE)
		if self.max_score >= 2048 or self.is_fail:
			pos_x, pos_y = max(0, (400 - tips_surface.get_width() - 50) // 2), max(0, (80 - tips_surface.get_height()) // 2)
			self.game_surface.blit(tips_surface, (pos_x, pos_y))
			pos2_x = pos_x + tips_surface.get_width() - 10
			self.button_dict["restart"].set_hover_image("./game2048/restart_click.png")
			self.button_dict["restart"].draw(self.game_surface, pos2_x, 10, absolute_point=(150, 120))
		else:
			pos_x, pos_y = max(0, (400 - tips_surface.get_width()) // 2), max(0, (80 - tips_surface.get_height()) // 2)
			self.game_surface.blit(tips_surface, (pos_x, pos_y))

	def deal_keydown_event(self, event):
		if self.is_fail:
			return
		if event.key == pygame.K_LEFT or event.key == pygame.K_a:
			self.move_left()
		elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
			self.move_right()
		elif event.key == pygame.K_UP or event.key == pygame.K_w:	
			self.move_up()
		elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
			self.move_down()

	def deal_mousemotion_event(self, event):
		for key, button in self.button_dict.items():
			button.set_hover(button.collidepoint(event.pos))

	def deal_mousebuttondown_event(self, event):
		if event.button == 1:
			for key, button in self.button_dict.items():
				if button.collidepoint(event.pos):
					if key == "restart":
						self.game_start()
	
	def move_up(self):
		self.move()

	def move_down(self):
		self.game_array = numpy.fliplr(self.game_array)	# 左右翻转
		self.move()
		self.game_array = numpy.fliplr(self.game_array)	# 左右翻转回来

	def move_left(self):
		self.game_array = numpy.rot90(self.game_array)	# 左右旋转
		self.move()
		self.game_array = numpy.rot90(self.game_array, k=3)	# 在旋转回来

	def move_right(self):
		self.game_array = numpy.rot90(self.game_array, k=3)	# 逆时针旋转90度
		self.move()
		self.game_array = numpy.rot90(self.game_array)	# 做个旋转回来

	def move(self):
		# 通用实现一个上移动的算法，其他移动使用numpy逻辑对数组旋转成左移动再旋转回来
		# 简单来说就是不想多写重复代码，但是没想好通用算法怎么实现好写
		blankpos_list = []
		for i in range(4):
			bottom = 0
			for j in range(1,4):
				if self.game_array[i][j] == 0:
					continue
				if self.game_array[i][bottom] == 0 or self.game_array[i][j] == self.game_array[i][bottom]:
					bottom_temp = bottom
					if self.game_array[i][bottom_temp] != 0:
						bottom += 1
					self.game_array[i][bottom_temp] += self.game_array[i][j]
					self.game_array[i][j] = 0
				else:
					bottom += 1
			# 处理因为判断底部能不能和上一个合并时，最后一个判断不能合并因为跳出循环导致没移动
			if self.game_array[i][bottom] == 0 and bottom < 3:	
				self.game_array[i][bottom] += self.game_array[i][j]
				self.game_array[i][j] = 0

			for j in range(bottom, 4):
				if self.game_array[i][j] == 0:
					blankpos_list.append((i, j))
		if not blankpos_list:
			self.is_fail = True
			return
		i, y = random.choice(blankpos_list)
		value = 2 if random.random() < 0.9 else 4
		self.game_array[i][y] = value



