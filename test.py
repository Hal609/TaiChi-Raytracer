import taichi as ti

ti.init(arch=ti.gpu)

x = ti.Vector([0, 1, 2])
y = ti.Vector([3, 4, 5])
z = ti.min(3, 21.2)
print(z)  # [0, 1, 1]  

