import taichi as ti
from taichi.math import vec3

norm = ti.math.normalize

VIEW_Z = 3.2
RESOLUTION = (1280, 720)
VOID_COLOUR = vec3(0.17, 0.17, 0.2)

@ti.func
def vec3Comp(v1, v2):
   return v1.x == v2.x and v1.y == v2.y and v1.z == v2.z

@ti.func
def nullVector(v):
   return vec3Comp(v, vec3((-1, -1, -1)))

@ti.func
def pixel_to_coord(i, j):
   aspect = RESOLUTION[0]/RESOLUTION[1]
   x = aspect * ((i / RESOLUTION[0]) - 0.5)
   y = (j / RESOLUTION[1]) - 0.5
   return x, y