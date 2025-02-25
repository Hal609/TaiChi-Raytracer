import math
import taichi as ti

@ti.dataclass
class Sphere:
   radius: ti.f32
   centre: ti.math.vec3
   colour: ti.math.vec3

   @ti.func
   def area(self):
      # a function to run in taichi scope
      return 4 * math.pi * self.radius * self.radius

   def is_zero_sized(self):
      # a python scope function
      return self.radius == 0.0