import sokoban
a=sokoban.Warehouse()
a.load_warehouse("./warehouses/warehouse_03.txt")
print((3,4) in a.targets)
