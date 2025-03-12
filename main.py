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
        candidate = intersect_sphere(ray, spheres[k])
        if not nullVector(candidate):
            intersect = candidate
            hitSphereNum = k
            break
    return intersect, hitSphereNum

@ti.kernel
def paint(t: float):
    cam_pos = cam_start + vec3(0.004, 0.004, 0.008) * t
    for i, j in pixels:
        ray = ray_to_pixel(i, j, cam_pos)
        col = vec3(0.0, 0.0, 0.0)
        contrib = 1.0
        # Iterate for up to 3 reflection bounces:
        for depth in range(3):
            intersect, k = closestRayIntersect(ray)
            if k == -1:
                # If no object is hit, add background colour and exit.
                col += VOID_COLOUR * contrib
                break

            light_intensity = calc_light(lights, k, (i, j), intersect, cam_pos, spheres)
            # Add the hit's colour (modulated by lighting and a base factor)
            col += spheres[k].colour * light_intensity * 0.9 * contrib

            # Prepare for the next reflection bounce:
            normal = norm(intersect - spheres[k].centre)
            # If the surface is non-reflective, exit early.
            if spheres[k].reflectivity <= 0:
                break

            # Compute the reflected ray. A small offset (0.1 * normal) helps avoid self-intersections.
            new_direction = ti.math.reflect(ray.direction, normal)
            ray = Ray(intersect + 0.1 * normal, new_direction + 0.1 * normal)
            # Decrease the contribution based on the object's reflectivity.
            contrib *= spheres[k].reflectivity

        f[i, j].rgb = col

gui = ti.GUI("Ray-Trace Renderer", res=RESOLUTION)

spheres = get_spheres()
lights = get_lights()

i = 0
while gui.running:
    paint(i * 0.03)
    gui.set_image(f)
    gui.show()
    i += 1