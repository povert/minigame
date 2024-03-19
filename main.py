# -*- coding: utf-8 -*-

import importlib
import pygame
import gamemenu


game_list = [		# 增加游戏模块
	"test_game",
]

def register_game(manager):
	for game_mod in game_list:
		module = importlib.import_module(game_mod)
		if not module:
			continue
		if hasattr(module, "register_game"):
			module.register_game(manager)

# 先初始化pygame，这样各个game模块就可以直接使用pygame载入对应图片等资源
pygame.init()
# 增加Game配置
game_menu = gamemenu.GameMenu()
register_game(game_menu)
game_menu.run()
