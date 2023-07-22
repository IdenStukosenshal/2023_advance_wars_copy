from staticfg import CFGBuilder
#создаем объект класса CFGBuilder
cfg = CFGBuilder().build_from_file('game_function_1','game_function_1.py')
#сохраняем визуализацию
cfg.build_visual('game_function_1','png')