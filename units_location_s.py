recon_positions = [(2, 3), (4, 5)]
infantry_positions = []


koord_and_units_dict = dict()

for i in recon_positions:
    koord_and_units_dict[i] = None
for i in infantry_positions:
    koord_and_units_dict[i] = None

koord_and_units_copy = koord_and_units_dict.copy()

# словарь юнитов(value) и их координат(key) для доступа при выборе рамкой и для операций с графом
# копия предыдущего состояния для обновления позиций в графе