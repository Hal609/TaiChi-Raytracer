import taichi as ti
from taichi.math import vec3

from sphere_class import Sphere
from lighting import PointLight
from helpers import *

def get_spheres():
   spheres = Sphere.field(shape=3)

   spheres[0] = Sphere(
      radius = 0.4,
      centre = vec3((0.5, 0.32, 3.0)),
      colour = vec3((1, 0.1, 0.1)),
      specular = 20,
      reflectivity = 0.15
   )
   spheres[1] = Sphere(
      radius = 0.2,
      centre = vec3((-0.25, 0.15, 2.7)),
      colour = vec3((0.1, 0.1, 1)),
      specular = 10,
      reflectivity = 0.05
   )
   spheres[2] = Sphere(
      radius = 3,
      centre = vec3((0, -3, 3.4)),
      colour = vec3((0.5, 0.5, 0.5)),
      specular = 20,
      reflectivity = 0.15
   )

   return spheres

def get_lights():
   lights = PointLight.field(shape=2)

   lights[0] = PointLight(
      position = vec3((6.0, 13.5, 8.0)),
      colour = vec3((1.0, 1.0, 1.0)), 
      intensity = 1.0
   )

   lights[1] = PointLight(
      position = vec3((-1.0, 1.35, -1.0)),
      colour = vec3((1.0, 1.0, 1.0)), 
      intensity = 0.3
   )

   return lights