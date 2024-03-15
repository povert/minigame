# -*- coding: utf-8 -*-

import game2048.game

def register_game(manager):
	mygame = game2048.game.Game(manager)
	manager.add_game(mygame)