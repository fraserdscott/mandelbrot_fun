import cmath
import numpy as np
import cv2

def mandelbrot(z, c):
    return z**2 + c


def orbit(c):
    z0 = 0
    z = mandelbrot(z0, c)
    visited = [c]
    # Keep iterating and check if it ever blows up
    for iter in range(100):
        z = mandelbrot(z, c)
        if abs(z) > 2:
            return None
        if z in visited:
            return visited
        
        visited.append(z)
    return visited


def period(c):
    z0 = c
    z = mandelbrot(z0, c)
    visited = set([c])
    for iter in range(1000):
        z = mandelbrot(z, c)
        if abs(z) > 2:
            return None
        if z in visited:
            return z
        
        visited.add(z)

    return None


def repelling_period(c):
    z0 = 0
    z = mandelbrot(z0, c)
    visited = [c]
    for iter in range(1000):
        z = mandelbrot(z, c)
        if abs(z) > 2:
            return None
        # then its periodic
        if z in visited:
            cycle_start = visited.index(z)
            cycle = visited[cycle_start:]

            rate_of_change = np.mean([y-x for (x,y) in zip(cycle, cycle[1:])])

            if np.abs(rate_of_change*z) > 1:
                return z
            return None
        
        visited.append(z)

    return None

def fixup(p):
    return (int(p.real*(h//3) + h//2), int(p.imag*(h//3) + h//2))


def draw_orbit(image, visited):
    cv2.circle(image, fixup(c), 1, (0,0,255))
    color = (255,255,0)
    pts = np.array([fixup(p) for p in visited], np.int32)
    cv2.polylines(image,np.array([pts]),False, color)
    
    

#np.random.randint(low=1, high=255)
h = 500
window_name = 'Image'

image = np.zeros((h,h,3), np.uint8)
cv2.circle(image, (0 + h//2, 0 + h//2), 3, (255,255,255))

rect = 1
for x in np.linspace(-2,2,200):
    for y in np.linspace(-2,2,200):
        c = complex(x,y)
        visited = orbit(c)
        if visited:
            z = repelling_period(c)
            if z:
                #cv2.circle(image, fixup(z), 3, (0,255,255))
                cv2.circle(image, fixup(c), 3, (0,0,255))
                #draw_orbit(image, visited)
            else:
                cv2.circle(image, fixup(c), 1, (255,255,255))

cv2.imshow(window_name, image)

#lol = complex(-1.0606060606060606,+0.030303030303030276)
#draw_orbit(image, orbit(complex(-1.0606060606060606,+0.030303030303030276)))











