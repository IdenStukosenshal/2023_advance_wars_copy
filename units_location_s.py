recon_positions = [(0, 0), (2, 3), (4, 5)]
infantry_positions = []


set_all_units = set()

for i in recon_positions:
    set_all_units.add(i)
for i in infantry_positions:
    set_all_units.add(i)

print("координаты всех юнитов", set_all_units)