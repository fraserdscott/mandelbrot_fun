import cmath
import numpy as np
import cv2

def mandelbrot(z, c):
    return z**2 + c


def in_mandelbrot(c):
    z0 = 0
    z = mandelbrot(z0, c)
    # Keep iterating and check if it ever blows up
    for iter in range(100):
        z = mandelbrot(z, c)
        if abs(z) > 2:
            return False
        
    return True


def orbit(c):
    z = mandelbrot(0, c)
    visited = set([c])
    for iter in range(1000):
        z = mandelbrot(z, c)
        if abs(z) > 2:
            return "OUT"
        if z in visited:
            if z==c:
                return "PERIODIC"
            return "PREPERIODIC"
        
        visited.add(z)

    return "IN"


def fixup(p):
    return (int(p.real*(h//3) + h//2), int(p.imag*(h//3) + h//2))
    

#np.random.randint(low=1, high=255)
h = 500
window_name = 'Image'

image = np.zeros((h,h,3), np.uint8)
cv2.circle(image, (0 + h//2, 0 + h//2), 3, (255,255,255))

rect = 1
for x in np.linspace(-2,2,300):
    for y in np.linspace(-2,2,300):
        c = complex(x,y)
        
        orbit_type = orbit(c)
        if orbit_type == "IN":
            cv2.circle(image, fixup(c), 1, (0,0,0)) # black
        elif orbit_type == "PERIODIC":
            cv2.circle(image, fixup(c), 1, (0,0,255)) #red
        elif orbit_type == "PREPERIODIC":
            cv2.circle(image, fixup(c), 1, (255,0,0)) #blue
        else:
            cv2.circle(image, fixup(c), 1, (255,255,255)) #white

cv2.imshow(window_name, image)


# the code does not find cycles for the border points and the rest are apparenlty preperdioc
