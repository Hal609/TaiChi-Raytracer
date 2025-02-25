import taichi as ti
from taichi.math import reflect, dot, vec3
from taichi import min, max, f32
from helpers import *
from ray import *

@ti.dataclass
class PointLight:
   position: vec3
   colour: vec3
   intensity: f32

   @ti.func
   def calc_contribution(self, point, normal):
      light_dir = norm(self.position - point)
      return dot(normal, light_dir)
   
   @ti.func
   def in_shadow(current_light, point, sphereNum, spheres):
      normal = point - spheres[sphereNum].centre
      result = False
      light_dir = norm(current_light.position - point)
      for k in range(spheres.shape[0]):
         if k != sphereNum:
            if not vec3Comp(intersect_sphere(light_dir, spheres[k], point + 0.01 * normal), vec3((-1, -1, -1))):
               result = True
      return result
   
   @ti.func
   def calc_specular(current_light, point, normal, viewDirection):
      shine = 0.0
      light_dir = norm(current_light.position - point)
      reflected = reflect(light_dir, normal)
      shine = max(0.0, dot(reflected, norm(viewDirection)))**20
      shine = min(1.0, shine)
      return shine
   

@ti.func
def calc_light(lights, sphere, pixel, intersect, cam_pos, spheres):
   normal = norm(intersect - spheres[sphere].centre)
   light = 0.2 # Ambient light
   for l in range(lights.shape[0]):
      if lights[l].in_shadow(intersect, sphere, spheres): break
      light += max(0, lights[l].calc_contribution(intersect, normal) * 0.8) * lights[l].intensity
      light += lights[l].calc_specular(intersect, normal, intersect - ray_to_pixel(pixel[0], pixel[1], cam_pos)) * 0.6 * lights[l].intensity
   return light