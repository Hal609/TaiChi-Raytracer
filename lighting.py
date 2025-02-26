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
      normal = norm(point - spheres[sphereNum].centre)
      light_ray = Ray(origin = point + 0.01 * normal,
                      direction = norm(current_light.position - point))
      result = False
      for k in range(spheres.shape[0]):
         if k != sphereNum and not nullVector(intersect_sphere(light_ray, spheres[k])): result = True
         
      return result
   
   @ti.func
   def calc_specular(current_light, point, normal, viewRay, sphere):
      shine = 0.0
      light_dir = norm(current_light.position - point)
      reflected = reflect(light_dir, normal)
      shine = max(0.0, dot(reflected, norm(viewRay)))**sphere.specular
      shine = min(1.0, shine)
      return shine
   

@ti.func
def calc_light(lights, sphereNum, pixel, intersect, cam_pos, spheres):
   normal = norm(intersect - spheres[sphereNum].centre)
   # Ambient light
   light = 0.2
   for l in range(lights.shape[0]):
      # Do not compute light if point is in shadow relative to this light
      if lights[l].in_shadow(intersect, sphereNum, spheres): break
      # Add point light contribution
      light += max(0, lights[l].calc_contribution(intersect, normal) * 0.8) * lights[l].intensity
      # Add specular highlight
      vecToIntersect = intersect - ray_to_pixel(pixel[0], pixel[1], cam_pos).direction
      specular = lights[l].calc_specular(intersect, normal, vecToIntersect, spheres[sphereNum])
      light += specular * 0.6 * lights[l].intensity
   return light