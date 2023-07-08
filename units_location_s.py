recon_positions = [(2, 3), (4, 5)]
infantry_positions = []


list_all_units = set()

for i in recon_positions:
    list_all_units.add(i)
for i in infantry_positions:
    list_all_units.add(i)

print(list_all_units)