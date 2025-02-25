import taichi as ti
from taichi.math import vec3
from helpers import *

@ti.dataclass
class Ray:
   origin: vec3
   direction: vec3

   @ti.func
   def size(self):
      return (self.direction.x**2 + self.direction.y**2 + self.direction.z**2)**0.5


@ti.func
def ray_to_pixel(i, j, cam_pos):
   x, y = pixel_to_coord(i, j)
   return vec3((x + cam_pos.x, y + cam_pos.y, cam_pos.z + VIEW_Z))


@ti.func
def intersect_sphere(ray_direction, sphereToCheck, ray_origin):
   val = ti.Vector((-1.0, -1.0, -1.0))

   oc = ray_origin - sphereToCheck.centre
   a = ti.cast(ti.math.dot(ray_direction, ray_direction), ti.f32)
   b = 2 * ti.math.dot(oc, ray_direction)
   c = ti.math.dot(oc, oc) - sphereToCheck.radius**2
   discriminant = b**2 - 4 * a * c
   if (discriminant >= 0):
      sqrtDiscriminant = discriminant**0.5
      t0 = (-b - sqrtDiscriminant) / (2.0 * a)
      t1 = (-b + sqrtDiscriminant) / (2.0 * a)

      if t0 > t1:
         t0, t1 = t1, t0

      if t0 >= 0:
         val = ray_origin + ray_direction * t0
      elif t1 >= 0:
         val = ray_origin + ray_direction * t1

   return val