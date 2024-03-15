# -*- coding: utf-8 -*-
import copy
import pygame
import game
import my_ui
from defines import *
from txz.level_config import *

class Game(game.Game):

	def __init__(self, manager):
		super().__init__(manager)
		self.init_custom_scene()
		self.is_win = False
		self.level = 1
		self.is_change = False
		self.button_dict = {}

	def init_custom_scene(self):
		# 自定义场景，因为该游戏贴图能更好贴合游戏画面
		self.custom_scene = pygame.Surface((400, 300))
		x = (self.scene.get_width() - self.custom_scene.get_width()) // 2
		y = (self.scene.get_height() - self.custom_scene.get_height()) // 2
		absolute_point = (x + self.absolute_point[0], y + self.absolute_point[1])
		self.absolute_point = absolute_point

	@property
	def name(self):
		return "推箱子"

	def start(self):
		self.scene.fill((12,95,53))
		self.custom_scene.fill((12,95,53))
		self.init_level()

	def init_level(self):
		self.custom_scene.fill((12,95,53))
		self.level_array = copy.deepcopy(LEVEL_CONFIG[self.level])
		self.target_pos_list = []
		self.move_list = []
		self.poser_index = (0, 0)
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
		self.button_dict = {}
		self.button_dict["next_level"] = MyButton("%s/img/next.png"%BASEDIR)
		self.button_dict["next_level"].set_hover_image("%s/img/next_click.png"%BASEDIR)
		if self.level == len(LEVEL_CONFIG) - 1:
			self.button_dict["next_level"].set_gray(True)
		self.button_dict["next_level"].draw(self.custom_scene, 322, 50, self.absolute_point)
		self.button_dict["last_level"] = MyButton("%s/img/last.png"%BASEDIR)
		self.button_dict["last_level"].set_hover_image("%s/img/last_click.png"%BASEDIR)
		if self.level == 1:
			self.button_dict["last_level"].set_gray(True)
		self.button_dict["last_level"].draw(self.custom_scene, 322, 110, self.absolute_point)
		self.button_dict["restart"] = MyButton("%s/img/restart.png"%BASEDIR)
		self.button_dict["restart"].set_hover_image("%s/img/restart_click.png"%BASEDIR)
		self.button_dict["restart"].set_gray(True)
		self.button_dict["restart"].draw(self.custom_scene, 322, 170, self.absolute_point)
		self.button_dict["reback"] = MyButton("%s/img/reback.png"%BASEDIR)
		self.button_dict["reback"].set_hover_image("%s/img/reback_click.png"%BASEDIR)
		self.button_dict["reback"].set_gray(True)
		self.button_dict["reback"].draw(self.custom_scene, 322, 230, self.absolute_point)
		draw_surface(self.scene, self.custom_scene)

	def deal_keydown_event(self, event):
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

	def deal_mousebuttondown_event(self, event):
		if self.is_win:
			return
		for key, button in self.button_dict.items():
			if button.is_gray:
				continue
			if not button.collidepoint(event.pos):
				continue
			if key in ("next_level", "win_next_level"):
				self.level += 1
				self.init_level()
			elif key in ("last_level", "win_last_level"):
				self.level -= 1
				self.init_level()
			elif key == "restart":
				self.init_level()
			elif key == "reback":
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
					self.button_dict["restart"].set_gray(True)
					self.button_dict["reback"].set_gray(True)
					self.button_dict["restart"].draw(self.custom_scene)
					self.button_dict["reback"].draw(self.custom_scene)
				self.flush()

	def deal_mousemotion_event(self, event):
		for key, button in self.button_dict.items():
			if button.is_gray:
				continue
			is_collidepoint = button.collidepoint(event.pos)
			if is_collidepoint and not button.is_hover:
				button.set_hover(True)
				self.flush()
				button.draw(self.custom_scene)
			elif not is_collidepoint and button.is_hover:
				button.set_hover(False)
				self.flush()
				button.draw(self.custom_scene)

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
		self.flush()

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
		self.flush()

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
		self.flush()

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
		self.flush()

	def record_move(self, move):
		if self.button_dict["reback"].is_gray:
			self.button_dict["reback"].set_gray(False)
			self.button_dict["reback"].draw(self.custom_scene)
		if self.button_dict["restart"].is_gray:
			self.button_dict["restart"].set_gray(False)
			self.button_dict["restart"].draw(self.custom_scene)
		self.move_list.append(move)

	def check_win(self):
		for x, y in self.target_pos_list:
			if self.level_array[y][x] != BOX_ON_TARGET:
				return
		self.win = True
		self.button_dict["reback"].set_gray(True)
		self.button_dict["reback"].draw(self.custom_scene)
		self.draw_win() 

	def flush(self):
		self.is_change = True

	def draw(self):
		if self.is_change:
			draw_surface(self.scene, self.custom_scene)
			self.is_change = False

	def draw_win(self):
		draw_image(self.custom_scene, "%s/img/guoguan.png"%BASEDIR, 30, 90)
		self.button_dict["win_next_level"] = MyButton("%s/img/next.png"%BASEDIR)
		self.button_dict["win_next_level"].set_hover_image("%s/img/next_click.png"%BASEDIR)
		if self.level == len(LEVEL_CONFIG) - 1:
			self.button_dict["win_next_level"].set_gray(True)
		self.button_dict["win_next_level"].draw(self.custom_scene, 180, 160, self.absolute_point)
		self.button_dict["win_last_level"] = MyButton("%s/img/last.png"%BASEDIR)
		self.button_dict["win_last_level"].set_hover_image("%s/img/last_click.png"%BASEDIR)
		if self.level == 1:
			self.button_dict["win_last_level"].set_gray(True)
		self.button_dict["win_last_level"].draw(self.custom_scene, 75, 160, self.absolute_point)

class MyButton(my_ui.My_ButtonUI):

	def __init__(self, image_path, button_size = None):
		super().__init__(image_path, button_size)
		self.is_gray = False
		self.gray_image = None

	def set_gray(self, is_gray):
		self.is_gray = is_gray
		if self.is_gray and not self.gray_image:
			self.gengerate_gray_image()
	
	def gengerate_gray_image(self):
		gray_image = pygame.Surface(self.button_image.get_size(), pygame.SRCALPHA)
		# 遍历原图像的每个像素
		for x in range(self.button_image.get_width()):
			for y in range(self.button_image.get_height()):
				# 获取原图像该像素的RGB值
				pixel = self.button_image.get_at((x, y))
				# 计算灰度值（简单的灰度算法：0.299*R + 0.587*G + 0.114*B）
				gray_value = int(0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2])
				# 在灰度图像上设置该像素的灰度值
				gray_image.set_at((x, y), (gray_value, gray_value, gray_value, pixel[3]))
		self.gray_image = gray_image

	@property
	def image(self):
		if self.is_gray:
			return self.gray_image
		return super().image