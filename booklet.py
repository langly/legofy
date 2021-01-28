
def get_palette():
    p = []
    for v in colors.colors.values():
        p.append(v)
    return p

def generate_svg(image, colors):
    import svgwrite
    from svgwrite import cm,mm

    height = len(image)
    width  = len(image[0])

    box_side = 8
    hPx = height * box_side
    wPx = width * box_side

    palette = get_palette()

    print(height,width)

    dwg = svgwrite.Drawing('test.svg', (hPx,wPx),viewBox=('0 0 ' + str(hPx) + " " +str(wPx)), debug=True, profile='full')

    for y in range(height):
        dy = y * box_side + ( box_side / 2 )
        for x in range(width):
            dx = x * box_side + ( box_side / 2 )
            ## double check x/y coords here
            idx = image[y][x]
            col = palette[idx]
            dwg.add ( dwg.circle( center = (dx,dy), r = box_side/2, fill=svgwrite.rgb(col[0], col[1], col[2])) )

    dwg.save()

