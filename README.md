# 介绍
使用pygame写的一些小游戏集合

main.py是主程序，在这里配置有哪些游戏
manager.py是游戏管理器，负责管理游戏的运行，game.py是游戏基类，所有游戏都继承自这个类
test_game.py是测试游戏，可以用来测试游戏的运行效果
my_ui.py是自定义实现一部分悬浮和点击效果的UI组件
defines.py是一些常量定义和通用逻辑

每一个游戏的具体实现思路在各个游戏的__init__.py文件中或者游戏的主文件中

# 安装依赖
pip install pygame

# 运行游戏
cd minigame  
python3 main.py