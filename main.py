import taichi as ti
from taichi.math import vec3

from sphere_class import *
from lighting import *
from ray import *
from setup_scene import *
from helpers import RESOLUTION, VOID_COLOUR, norm

ti.init(arch=ti.gpu)

pixels = ti.field(dtype=float, shape=RESOLUTION)
f = ti.Vector.field(n=3, dtype=float, shape=RESOLUTION)

origin = vec3((0, 0, 0))
cam_start = vec3((0, 0.0, -1.0))
viewHeight: float = 1
 
@ti.kernel
def paint(t: float):
    cam_pos = cam_start + vec3(0.002, 0.002, 0.004) * t
    for i, j in pixels:
      f[i, j].rgb = VOID_COLOUR
      for k in range(spheres.shape[0]):
         light_strength = 0.0
         intersect = intersect_sphere(ray_to_pixel(i, j, cam_pos), spheres[k], cam_pos)
         if not vec3Comp(intersect, vec3((-1, -1, -1))):
            light_strength += calc_light(lights, k, (i, j), intersect, cam_pos, spheres)
            f[i, j].rgb = spheres[k].colour * light_strength
            break

gui = ti.GUI("Ray-Trace Renderer", res=RESOLUTION)

spheres = get_spheres()
lights = get_lights()

i = 0
while gui.running:
    paint(i * 0.03)
    gui.set_image(f)
    gui.show()
    i += 1