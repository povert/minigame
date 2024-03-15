# -*- coding: utf-8 -*-

import game
from defines import *

def register_game(manager):
	mygame = Game(manager)
	manager.add_game(mygame)

'''
测试游戏功能，按下任意键会显示按下的键，写游戏逻辑也可以在这里测试pygame的功能
'''

class Game(game.Game):

	def __init__(self, manager):
		super().__init__(manager)
		self.key_text = ""

	@property
	def name(self):
		return "Test Game"

	def deal_keydown_event(self, event):
		self.key_text = str(event.key)
	
	def draw(self):
		self.scene.fill(WHITE)
		draw_text(self.scene, self.key_text, 50, BLACK)


