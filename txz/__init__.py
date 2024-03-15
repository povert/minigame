# -*- coding: utf-8 -*-

import txz.game

'''
游戏思路：
	使用一个矩阵来表示游戏地图，每个格子不同值代表不同情况，比如空格子为0，墙为1，箱子为2等
	记录下玩家的位置，然后根据玩家位置和移动操作来跟新游戏地图，比如玩家向下推箱子，则玩家原来位置变成空格子，箱子原来位置变成玩家位置，箱子向下移动一格

	关于回退操作，可以记录玩家移动前会变动的3个格子（玩家原来位置，箱子原来位置，箱子移动后位置），然后回退时将这3个格子恢复原状即可（玩家位置变回原来位置，箱子位置变回原来位置，箱子位置变回移动后位置）
	用一个栈来记录玩家的移动历史，每当玩家移动后，将移动前后的3个格子记录到栈中，当玩家需要回退时，从栈中取出最后的3个格子，将其恢复即可

'''

def register_game(manager):
	mygame = txz.game.Game(manager)
	manager.add_game(mygame)