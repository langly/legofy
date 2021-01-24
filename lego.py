#!/usr/bin/env python3
import colors

from PIL import Image
import math

scale = 0.1225 / 2.0

def calc3D_dist(c, o):
    l = zip(c,o)
    m = map(lambda x : math.pow(x[0] - x[1],2), l)
    dist = math.sqrt(sum(m))

    return dist


### We should move the colours into a kd tree or similar for perf reasons.
def quantize(col):
    min_distance = 1000
    min_color = None

    for c in colors.colors:
        val = colors.colors[c]
        d = calc3D_dist(col,val)

        if ( d < min_distance ):
            min_distance = d
            min_color = c

    return colors.colors[min_color]

with Image.open("cat_small.jpeg").convert('RGB') as im:
    orignal_size = im.size
    new_size = list(map(lambda x: int(x * scale), orignal_size))
    im.resize(new_size)

    pix = im.load()

    print(orignal_size)

    (width,height) = orignal_size
    print(width,height)

    ### XXX: Make sure I access this in the correct way that does not crash the cache.
    for y in range(0,height):
        print(y)
        for x in range(0,width):
            val = quantize(pix[x,y])
            pix[x,y] = val

    im.save('converted.jpeg')
