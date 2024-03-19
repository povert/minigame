# -*- coding: utf-8 -*-

import game
import objects
from defines import get_text_surface

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

	def start(self):
		self.custom_mouseUI = {}
		self.custom_mouseUI["text"] = objects.MyUIText("Effect Text", 30, abs_offset=self.abs_offset)
		self.custom_mouseUI["text"].set_hover_color((255, 0, 0))
		self.custom_mouseUI["text"].set_click_color((0, 255, 0))
		self.custom_mouseUI["text"].set_click_func(self.click_text)
		self.custom_mouseUI["text"].set_pos((200, 200))
		self.custom_mouseUI["image"] = objects.MyUIImage("./images/background.jpg", (120, 120), abs_offset=self.abs_offset)
		self.custom_mouseUI["image"].set_hover_image("./images/test.webp")
		self.custom_mouseUI["image"].set_hover_size((200, 200))
		self.custom_mouseUI["image"].set_click_func(self.click_image)

	def click_text(self):
		self.key_text = "click text"

	def click_image(self):
		self.key_text = "click image"

	def on_keydown(self, event):
		self.key_text = "按键%s"%str(event.key)

	def custom_draw(self):
		self.scene.blit(get_text_surface("当前操作：%s"%self.key_text, 30, (0, 0, 0)), (220, 300))

		


