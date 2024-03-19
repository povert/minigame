# -*- coding: utf-8 -*-
import copy
import pygame
import game
import objects
from defines import *
from txz.level_config import *

class Game(game.Game):

	def __init__(self, manager):
		super().__init__(manager)
		self.is_win = False
		self.level = 1
		self.background_color = (12,95,53)
		# 自定义一个关卡场景，用来贴关卡图片，实现在逻辑中更新贴图
		self.custom_scene = pygame.Surface((300, 300))

	@property
	def name(self):
		return "推箱子"

	def start(self):
		self.init_level()
		self.init_button()

	def end(self):
		self.custom_mouseUI = {}
		self.level_array = []
		self.target_pos_list = []
		self.move_list = []
		self.poser_index = (0, 0)

	def init_level(self):
		self.custom_scene.fill(self.background_color)
		self.level_array = copy.deepcopy(LEVEL_CONFIG[self.level])
		self.target_pos_list = []
		self.move_list = []
		self.poser_index = (0, 0)
		self.is_win = False
		for y in range(len(self.level_array)):
			for x in range(len(self.level_array[y])):
				if self.level_array[y][x] != NO_FILL:
					array_value = self.level_array[y][x]
					img = LEVEL_IMAGE_DICT[array_value]
					if array_value == TARGET_ON_BLANK: 
						# 正确的点贴图是一个空的点，所以在补一个空白位置的贴图（其他不用补三因为有对应的图片）
						self.custom_scene.blit(LEVEL_IMAGE_DICT[BLANK], ((x+1)*30, (y+1)*30))
					self.custom_scene.blit(img, ((x+1)*30, (y+1)*30))
					if array_value in (TARGET_ON_BLANK, BOX_ON_TARGET, PERSION_ON_TARGET):
						self.target_pos_list.append((x, y))
					if array_value in (PERSION_ON_TARGET, PERSION_ON_BLANK):
						self.poser_index = (x, y)
	
	def init_button(self):
		self.custom_mouseUI = {}
		self.custom_mouseUI["next_level"] = MyButton("%s/img/next.png"%BASEDIR, abs_offset=self.abs_offset)
		self.custom_mouseUI["next_level"].set_hover_image("%s/img/next_click.png"%BASEDIR)
		self.custom_mouseUI["next_level"].set_click_func(self.next_level)
		self.custom_mouseUI["next_level"].set_pos((322 + 150, 200 + 50))
		self.custom_mouseUI["last_level"] = MyButton("%s/img/last.png"%BASEDIR, abs_offset=self.abs_offset)
		self.custom_mouseUI["last_level"].set_hover_image("%s/img/last_click.png"%BASEDIR)
		self.custom_mouseUI["last_level"].set_click_func(self.last_level)
		self.custom_mouseUI["last_level"].set_pos((322 + 150, 200 +110))
		self.custom_mouseUI["restart"] = MyButton("%s/img/restart.png"%BASEDIR, abs_offset=self.abs_offset)
		self.custom_mouseUI["restart"].set_hover_image("%s/img/restart_click.png"%BASEDIR)
		self.custom_mouseUI["restart"].set_click_func(self.restart_level)
		self.custom_mouseUI["restart"].set_pos((322 + 150, 200 + 170))
		self.custom_mouseUI["reback"] = MyButton("%s/img/reback.png"%BASEDIR, abs_offset=self.abs_offset)
		self.custom_mouseUI["reback"].set_hover_image("%s/img/reback_click.png"%BASEDIR)
		self.custom_mouseUI["reback"].set_click_func(self.reback_move)
		self.custom_mouseUI["reback"].set_pos((322 + 150, 200 + 230))
		self.custom_mouseUI["win_next_level"] = MyButton("%s/img/next.png"%BASEDIR, abs_offset=self.abs_offset)
		self.custom_mouseUI["win_next_level"].set_hover_image("%s/img/next_click.png"%BASEDIR)
		self.custom_mouseUI["win_next_level"].set_click_func(self.next_level)
		self.custom_mouseUI["win_next_level"].set_pos((180 + 100, 290 + 75))
		self.custom_mouseUI["win_next_level"].is_show = False
		self.refresh_button()

	def next_level(self):
		self.level += 1
		self.init_level()
		self.refresh_button()

	def last_level(self):
		self.level -= 1
		self.init_level()
		self.refresh_button()

	def restart_level(self):
		self.init_level()
		self.refresh_button()

	def refresh_button(self):
		self.custom_mouseUI["reback"].set_gray(True)
		self.custom_mouseUI["restart"].set_gray(True)
		self.custom_mouseUI["win_next_level"].is_show = False
		if self.level == len(LEVEL_CONFIG) - 1:
			self.custom_mouseUI["next_level"].set_gray(True)
		else:
			self.custom_mouseUI["next_level"].set_gray(False)
		if self.level == 1:
			self.custom_mouseUI["last_level"].set_gray(True)
		else:
			self.custom_mouseUI["last_level"].set_gray(False)

	def on_keydown(self, event):
		if self.is_win:
			return
		if event.key ==pygame.K_LEFT or event.key ==pygame.K_a:
			self.move_left()
		elif event.key ==pygame.K_RIGHT or event.key ==pygame.K_d:
			self.move_right()
		elif event.key ==pygame.K_UP or event.key ==pygame.K_w:
			self.move_up()
		elif event.key ==pygame.K_DOWN or event.key ==pygame.K_s:
			self.move_down()

	def move_left(self):
		x, y = self.poser_index
		if self.level_array[y][x - 1] == WALL:	# 左边是墙
			return
		if self.level_array[y][x - 1] in (BOX_ON_TARGET, BOX_ON_BLANK):	# 左边是箱子
			if self.level_array[y][x - 2] in (WALL, BOX_ON_TARGET, BOX_ON_BLANK):	# 左边的左边是墙或箱子
				return
		reback_array = [(x, y, self.level_array[y][x]), (x - 1, y, self.level_array[y][x - 1]), (x - 2, y, self.level_array[y][x - 2])]
		if self.level_array[y][x] == PERSION_ON_BLANK:	# 人原来在空白位置
			self.level_array[y][x] = BLANK
			self.custom_scene.blit(LEVEL_IMAGE_DICT[BLANK], ((x+1)*30, (y+1)*30))
		elif self.level_array[y][x] == PERSION_ON_TARGET:	# 人原来在目标位置
			self.level_array[y][x] = TARGET_ON_BLANK
			self.custom_scene.blit(LEVEL_IMAGE_DICT[BLANK], ((x+1)*30, (y+1)*30))
			self.custom_scene.blit(LEVEL_IMAGE_DICT[TARGET_ON_BLANK], ((x+1)*30, (y+1)*30))
	
		if self.level_array[y][x - 1] in (BOX_ON_TARGET, BOX_ON_BLANK):	# 左边是箱子			
			if self.level_array[y][x - 1] == BOX_ON_TARGET:	# 箱子原来在目标位置
				self.level_array[y][x - 1] = PERSION_ON_TARGET
				self.custom_scene.blit(LEVEL_IMAGE_DICT[PERSION_ON_TARGET], (x*30, (y+1)*30))
			elif self.level_array[y][x - 1] == BOX_ON_BLANK:	# 箱子原来在空白位置
				self.level_array[y][x - 1] = PERSION_ON_BLANK
				self.custom_scene.blit(LEVEL_IMAGE_DICT[PERSION_ON_BLANK], (x*30, (y+1)*30))
			if self.level_array[y][x - 2] == BLANK:	# 左边的左边是空白位置
				self.level_array[y][x - 2] = BOX_ON_BLANK
				self.custom_scene.blit(LEVEL_IMAGE_DICT[BOX_ON_BLANK], ((x-1)*30, (y+1)*30))
			elif self.level_array[y][x - 2] == TARGET_ON_BLANK:	# 左边的左边是目标位置
				self.level_array[y][x - 2] = BOX_ON_TARGET
				self.custom_scene.blit(LEVEL_IMAGE_DICT[BOX_ON_TARGET], ((x-1)*30, (y+1)*30))
		elif self.level_array[y][x - 1] == TARGET_ON_BLANK:	# 左边是目标位置
			self.level_array[y][x - 1] = PERSION_ON_TARGET
			self.custom_scene.blit(LEVEL_IMAGE_DICT[PERSION_ON_TARGET], (x*30, (y+1)*30))
		elif self.level_array[y][x - 1] == BLANK:	# 左边是空白位置
			self.level_array[y][x - 1] = PERSION_ON_BLANK
			self.custom_scene.blit(LEVEL_IMAGE_DICT[PERSION_ON_BLANK], (x*30, (y+1)*30))
		self.poser_index = (x - 1, y)
		self.record_move(reback_array)
		self.check_win()

	def move_right(self):
		x, y = self.poser_index
		if self.level_array[y][x + 1] == WALL:	# 右边是墙
			return
		if self.level_array[y][x + 1] in (BOX_ON_TARGET, BOX_ON_BLANK):	# 右边是箱子
			if self.level_array[y][x + 2] in (WALL, BOX_ON_TARGET, BOX_ON_BLANK):	# 右边的右边是墙或箱子
				return
		reback_array = [(x, y, self.level_array[y][x]), (x + 1, y, self.level_array[y][x + 1]), (x + 2, y, self.level_array[y][x + 2])]
		if self.level_array[y][x] == PERSION_ON_BLANK:	# 人原来在空白位置
			self.level_array[y][x] = BLANK
			self.custom_scene.blit(LEVEL_IMAGE_DICT[BLANK], ((x+1)*30, (y+1)*30))
		elif self.level_array[y][x] == PERSION_ON_TARGET:	# 人原来在目标位置
			self.level_array[y][x] = TARGET_ON_BLANK
			self.custom_scene.blit(LEVEL_IMAGE_DICT[BLANK], ((x+1)*30, (y+1)*30))
			self.custom_scene.blit(LEVEL_IMAGE_DICT[TARGET_ON_BLANK], ((x+1)*30, (y+1)*30))
	
		if self.level_array[y][x + 1] in (BOX_ON_TARGET, BOX_ON_BLANK):	# 右边是箱子			
			if self.level_array[y][x + 1] == BOX_ON_TARGET:	# 箱子原来在目标位置
				self.level_array[y][x + 1] = PERSION_ON_TARGET
				self.custom_scene.blit(LEVEL_IMAGE_DICT[PERSION_ON_TARGET], ((x+2)*30, (y+1)*30))
			elif self.level_array[y][x + 1] == BOX_ON_BLANK:	# 箱子原来在空白位置
				self.level_array[y][x + 1] = PERSION_ON_BLANK
				self.custom_scene.blit(LEVEL_IMAGE_DICT[PERSION_ON_BLANK], ((x+2)*30, (y+1)*30))
			if self.level_array[y][x + 2] == BLANK:	# 右边的右边是空白位置
				self.level_array[y][x + 2] = BOX_ON_BLANK
				self.custom_scene.blit(LEVEL_IMAGE_DICT[BOX_ON_BLANK], ((x+3)*30, (y+1)*30))
			elif self.level_array[y][x + 2] == TARGET_ON_BLANK:	# 右边的右边是目标位置
				self.level_array[y][x + 2] = BOX_ON_TARGET
				self.custom_scene.blit(LEVEL_IMAGE_DICT[BOX_ON_TARGET], ((x+3)*30, (y+1)*30))
		elif self.level_array[y][x + 1] == TARGET_ON_BLANK:	# 右边是目标位置
			self.level_array[y][x + 1] = PERSION_ON_TARGET
			self.custom_scene.blit(LEVEL_IMAGE_DICT[PERSION_ON_TARGET], ((x+2)*30, (y+1)*30))
		elif self.level_array[y][x + 1] == BLANK:	# 右边是空白位置
			self.level_array[y][x + 1] = PERSION_ON_BLANK
			self.custom_scene.blit(LEVEL_IMAGE_DICT[PERSION_ON_BLANK], ((x+2)*30, (y+1)*30))
		self.poser_index = (x + 1, y)
		self.record_move(reback_array)
		self.check_win()

	def move_up(self):
		x, y = self.poser_index
		if self.level_array[y - 1][x] == WALL:	# 上边是墙
			return
		if self.level_array[y - 1][x] in (BOX_ON_TARGET, BOX_ON_BLANK):	# 上边是箱子
			if self.level_array[y - 2][x] in (WALL, BOX_ON_TARGET, BOX_ON_BLANK):	# 上边的上边是墙或箱子
				return
		reback_array = [(x, y, self.level_array[y][x]), (x, y - 1, self.level_array[y - 1][x]), (x, y - 2, self.level_array[y - 2][x])]
		if self.level_array[y][x] == PERSION_ON_BLANK:	# 人原来在空白位置
			self.level_array[y][x] = BLANK
			self.custom_scene.blit(LEVEL_IMAGE_DICT[BLANK], ((x+1)*30, (y+1)*30))
		elif self.level_array[y][x] == PERSION_ON_TARGET:	# 人原来在目标位置
			self.level_array[y][x] = TARGET_ON_BLANK
			self.custom_scene.blit(LEVEL_IMAGE_DICT[BLANK], ((x+1)*30, (y+1)*30))
			self.custom_scene.blit(LEVEL_IMAGE_DICT[TARGET_ON_BLANK], ((x+1)*30, (y+1)*30))
	
		if self.level_array[y - 1][x] in (BOX_ON_TARGET, BOX_ON_BLANK):	# 上边是箱子			
			if self.level_array[y - 1][x] == BOX_ON_TARGET:	# 箱子原来在目标位置
				self.level_array[y - 1][x] = PERSION_ON_TARGET
				self.custom_scene.blit(LEVEL_IMAGE_DICT[PERSION_ON_TARGET], ((x+1)*30, y*30))
			elif self.level_array[y - 1][x] == BOX_ON_BLANK:	# 箱子原来在空白位置
				self.level_array[y - 1][x] = PERSION_ON_BLANK
				self.custom_scene.blit(LEVEL_IMAGE_DICT[PERSION_ON_BLANK], ((x+1)*30, y*30))
			if self.level_array[y - 2][x] == BLANK:	# 上边的上边是空白位置
				self.level_array[y - 2][x] = BOX_ON_BLANK
				self.custom_scene.blit(LEVEL_IMAGE_DICT[BOX_ON_BLANK], ((x+1)*30, (y-1)*30))
			elif self.level_array[y - 2][x] == TARGET_ON_BLANK:	# 上边的上边是目标位置
				self.level_array[y - 2][x] = BOX_ON_TARGET
				self.custom_scene.blit(LEVEL_IMAGE_DICT[BOX_ON_TARGET], ((x+1)*30, (y-1)*30))
		elif self.level_array[y - 1][x] == TARGET_ON_BLANK:	# 上边是目标位置
			self.level_array[y - 1][x] = PERSION_ON_TARGET
			self.custom_scene.blit(LEVEL_IMAGE_DICT[PERSION_ON_TARGET], ((x+1)*30, y*30))	
		elif self.level_array[y - 1][x] == BLANK:	# 上边是空白位置
			self.level_array[y - 1][x] = PERSION_ON_BLANK
			self.custom_scene.blit(LEVEL_IMAGE_DICT[PERSION_ON_BLANK], ((x+1)*30, y*30))
		self.poser_index = (x, y - 1)
		self.record_move(reback_array)
		self.check_win()

	def move_down(self):
		x, y = self.poser_index
		if self.level_array[y + 1][x] == WALL:	# 下边是墙
			return
		if self.level_array[y + 1][x] in (BOX_ON_TARGET, BOX_ON_BLANK):	# 下边是箱子
			if self.level_array[y + 2][x] in (WALL, BOX_ON_TARGET, BOX_ON_BLANK):	# 下边的下边是墙或箱子
				return
		reward_array = [(x, y, self.level_array[y][x]), (x, y + 1, self.level_array[y + 1][x]), (x, y + 2, self.level_array[y + 2][x])]
		if self.level_array[y][x] == PERSION_ON_BLANK:	# 人原来在空白位置		
			self.level_array[y][x] = BLANK
			self.custom_scene.blit(LEVEL_IMAGE_DICT[BLANK], ((x+1)*30, (y+1)*30))
		elif self.level_array[y][x] == PERSION_ON_TARGET:	# 人原来在目标位置
			self.level_array[y][x] = TARGET_ON_BLANK
			self.custom_scene.blit(LEVEL_IMAGE_DICT[BLANK], ((x+1)*30, (y+1)*30))
			self.custom_scene.blit(LEVEL_IMAGE_DICT[TARGET_ON_BLANK], ((x+1)*30, (y+1)*30))
	
		if self.level_array[y + 1][x] in (BOX_ON_TARGET, BOX_ON_BLANK):	# 下边是箱子			
			if self.level_array[y + 1][x] == BOX_ON_TARGET:	# 箱子原来在目标位置
				self.level_array[y + 1][x] = PERSION_ON_TARGET
				self.custom_scene.blit(LEVEL_IMAGE_DICT[PERSION_ON_TARGET], ((x+1)*30, (y+2)*30))
			elif self.level_array[y + 1][x] == BOX_ON_BLANK:	# 箱子原来在空白位置
				self.level_array[y + 1][x] = PERSION_ON_BLANK
				self.custom_scene.blit(LEVEL_IMAGE_DICT[PERSION_ON_BLANK], ((x+1)*30, (y+2)*30))
			if self.level_array[y + 2][x] == BLANK:	# 下边的下边是空白位置
				self.level_array[y + 2][x] = BOX_ON_BLANK
				self.custom_scene.blit(LEVEL_IMAGE_DICT[BOX_ON_BLANK], ((x+1)*30, (y+3)*30))
			elif self.level_array[y + 2][x] == TARGET_ON_BLANK:	# 下边的下边是目标位置
				self.level_array[y + 2][x] = BOX_ON_TARGET
				self.custom_scene.blit(LEVEL_IMAGE_DICT[BOX_ON_TARGET], ((x+1)*30, (y+3)*30))
		elif self.level_array[y + 1][x] == TARGET_ON_BLANK:	# 下边是目标位置
			self.level_array[y + 1][x] = PERSION_ON_TARGET	
			self.custom_scene.blit(LEVEL_IMAGE_DICT[PERSION_ON_TARGET], ((x+1)*30, (y+2)*30))
		elif self.level_array[y + 1][x] == BLANK:	# 下边是空白位置
			self.level_array[y + 1][x] = PERSION_ON_BLANK
			self.custom_scene.blit(LEVEL_IMAGE_DICT[PERSION_ON_BLANK], ((x+1)*30, (y+2)*30))
		self.poser_index = (x, y + 1)		
		self.record_move(reward_array)
		self.check_win()

	def record_move(self, move):
		if self.custom_mouseUI["reback"].is_gray:
			self.custom_mouseUI["reback"].set_gray(False)
		if self.custom_mouseUI["restart"].is_gray:
			self.custom_mouseUI["restart"].set_gray(False)
		self.move_list.append(move)

	def reback_move(self):
		reback_array = self.move_list.pop()
		for x, y, value in reback_array:
			self.level_array[y][x] = value
			img = LEVEL_IMAGE_DICT[value]
			if value == TARGET_ON_BLANK:
				self.custom_scene.blit(LEVEL_IMAGE_DICT[BLANK], ((x+1)*30, (y+1)*30))
			self.custom_scene.blit(img, ((x+1)*30, (y+1)*30))
			if value in (PERSION_ON_TARGET, PERSION_ON_BLANK):
				self.poser_index = (x, y)
		if not self.move_list:
			self.custom_mouseUI["restart"].set_gray(True)
			self.custom_mouseUI["reback"].set_gray(True)

	def check_win(self):
		for x, y in self.target_pos_list:
			if self.level_array[y][x] != BOX_ON_TARGET:
				return
		self.is_win = True
		self.custom_mouseUI["reback"].set_gray(True)

	def custom_draw(self):
		if self.is_win:
			self.draw_win()

	def draw_win(self):
		win_image = pygame.image.load("%s/img/guoguan.png"%BASEDIR)
		self.scene.blit(win_image, (180, 290))
		self.custom_mouseUI["win_next_level"].is_show = True
		if self.level == len(LEVEL_CONFIG) - 1:
			self.custom_mouseUI["win_next_level"].set_gray(True)
		self.custom_mouseUI["win_next_level"].draw(self.scene)

	def draw_background(self):
		self.scene.fill(self.background_color)
		self.scene.blit(self.custom_scene, (150, 200))

class MyButton(objects.MyUIImage):

	def __init__(self, image_path, image_size = None, abs_offset = (0, 0)):
		super().__init__(image_path, image_size, abs_offset)
		self.is_gray = False
		self.gray_image = None

	def draw(self, surface, pos=None, abs_offset=None):
		if not self.is_gray:
			return super().draw(surface, pos, abs_offset)
		image_surface = self.gray_image
		image_size = self.size
		if image_size:
			image_surface = pygame.transform.scale(image_surface, image_size)
		if pos is None and self.image_rect:
			x, y = self.image_rect.x, self.image_rect.y
		else:
			x, y = pos if pos else (0, 0)
		image_rect = image_surface.get_rect(topleft=(x, y))
		surface.blit(image_surface, image_rect)
		self.image_rect = image_rect
		self.abs_offset = abs_offset if abs_offset else self.abs_offset

	def set_gray(self, is_gray):
		self.is_gray = is_gray
		if self.is_gray and not self.gray_image:
			self.gengerate_gray_image()
	
	def gengerate_gray_image(self):
		button_image = get_image_surface(self.image_path)
		size = self.size if self.size else button_image.get_size()
		gray_image = pygame.Surface(size, pygame.SRCALPHA)
		# 遍历原图像的每个像素
		for x in range(button_image.get_width()):
			for y in range(button_image.get_height()):
				# 获取原图像该像素的RGB值
				pixel = button_image.get_at((x, y))
				# 计算灰度值（简单的灰度算法：0.299*R + 0.587*G + 0.114*B）
				gray_value = int(0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2])
				# 在灰度图像上设置该像素的灰度值
				gray_image.set_at((x, y), (gray_value, gray_value, gray_value, pixel[3]))
		self.gray_image = gray_image

	def on_click_func(self):
		if self.is_gray:
			return
		self.click_func()
