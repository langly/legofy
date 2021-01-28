#!/usr/bin/env python3
import colors
import numpy as np

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
    min_idx = None

    for (i,c) in enumerate(colors.colors):
        val = colors.colors[c]
        d = calc3D_dist(col,val)

        if ( d < min_distance ):
            min_distance    = d
            min_color       = c
            min_idx         = i

    return (colors.colors[min_color],min_idx)

def quantize_image(filename):
    with Image.open("cat_small.jpeg").convert('RGB') as im:
        orignal_size = im.size
        new_size = list(map(lambda x: int(x * scale), orignal_size))
        im.resize(new_size)

        pix = im.load()

        print(orignal_size)

        (width,height) = orignal_size
        print(width,height)

        ### XXX: Make sure I access this in the correct way that does not crash the cache.
        prev_val = None
        prev_res = None

        image = []

        for y in range(0,height):
            row = []
            for x in range(0,width):
                in_val = pix[x,y]
                if not prev_val or not (in_val == prev_val):
                    (prev_res,prev_idx) = quantize(in_val)
                    prev_val = in_val
                    pix[x,y] = prev_res
                else:
                    pix[x,y] = prev_res

                row.append(prev_idx)

            image.append(row)
            row = []

        im.save('converted.jpeg')
        return image

from booklet import generate_svg

image = quantize_image('cat_small.jpeg')
generate_svg(image, colors.colors)
