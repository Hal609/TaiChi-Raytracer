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

cam_start = vec3((0, 0.0, -2.0))
 
@ti.func
def closestRayIntersect(ray):
   intersect = vec3(-1, -1, -1)
   hitSphereNum = -1
   for k in range(spheres.shape[0]):
      intersect = intersect_sphere(ray, spheres[k])
      if not nullVector(intersect):
         hitSphereNum = k
         break

   return intersect, hitSphereNum

@ti.func
def calcReflection(rayIn, sphere, point):
   normal = norm(point - sphere.centre)
   rayOut = Ray(point + 0.1* normal, ti.math.reflect(rayIn.direction, normal) + 0.1* normal)
   intersect, k = closestRayIntersect(rayOut)
   return intersect, k

@ti.kernel
def paint(t: float):
    cam_pos = cam_start + vec3(0.004, 0.004, 0.008) * t
    for i, j in pixels:
      ray = ray_to_pixel(i, j, cam_pos)
      intersect, k = closestRayIntersect(ray)
      light_intensity = calc_light(lights, k, (i, j), intersect, cam_pos, spheres)
      f[i, j].rgb = spheres[k].colour * light_intensity * 0.9 if (k != -1) else VOID_COLOUR

      # Reflection
      reflection, k_reflect = calcReflection(ray, spheres[k], intersect)
      if not nullVector(reflection) and (k_reflect != k):
         f[i, j].rgb += spheres[k_reflect].colour * spheres[k].reflectivity

gui = ti.GUI("Ray-Trace Renderer", res=RESOLUTION)

spheres = get_spheres()
lights = get_lights()

i = 0
while gui.running:
    paint(i * 0.03)
    gui.set_image(f)
    gui.show()
    i += 1