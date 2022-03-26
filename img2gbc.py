# a tool to convert colorful pictures to GB Studio-compatible colorized backgrounds
# made by NalaFala/Yousurname/Y0UR-U5ERNAME
# Pillow library required (py -m pip install Pillow)
# works better on some images than others depending on the method used
# not intended to be used on grayscale images or images with not many colors

from PIL import Image
from math import dist
import time

# function definitions

def paldist(a, b):
    #p1 = (getcols(a)*4)[:4] # euclidean distance method
    #p2 = (getcols(b)*4)[:4]
    p1 = getcols(a) # average method
    p2 = getcols(b)
    cds = [min([dist(i, j) for j in p2]) for i in p1]
    #return sqrt(cds[0]**2 + cds[1]**2 + cds[2]**2 + cds[3]**2) # euclidean distance method
    return sum(cds) / len(cds) # average method

i2xy = lambda i: (i // 18, i % 18)
xy2i = lambda x, y: x * 18 + y

i1 = lambda x: x[1]

getcols = lambda x: [i[1] for i in x.getcolors()]

def groupimg(g):
    global tiles

    gi = Image.new('RGB', (len(g) * 8, 1))

    for c, i in enumerate(g):
        gi.paste(tiles[i], (c*8, 0))

    return gi.quantize(4).convert('RGB')

def realpal(i): # to prevent using pure black
    palimage = Image.new('P', (16, 16))
    palimage.putpalette(flat(getcols(i)) * 64)
    return palimage

rgb2hex = lambda x: '%02x%02x%02x' % x

flat = lambda z: [x for y in z for x in y]


# program start
file = input('File Location: ')
method = input('Method (A, B, C, D, or E): ').upper()
if method not in ['A', 'B', 'C', 'D', 'E']: method = 'A'; print('Defaulting to method A')

start = time.time()

with Image.open(file) as im:

    # resize image
    out = im.resize((160, 144)).convert('RGB')
    im.close()

    # divide image up into 8x8 tiles
    tiles = []
    for i in range(20):
        for j in range(18):
            tiles.append(out.crop((i*8, j*8, i*8+8, j*8+8)))
    
    # apply palettes of 4 colors to each tile
    tiles4 = tiles.copy()
    for i in range(len(tiles4)):
        tiles4[i] = tiles4[i].quantize(4).convert('RGB')

    # natural selection (closest palettes get merged)
    tilegroups = [] # replace with [[i] for i in range(360)] and delete round 1 to go directly to round 2
    
    if method in 'DE':
        # choose 8 tiles whose palettes are farthest from each other
        #tilegroups = [sorted([(c, min([paldist(i, j) for j in tiles4])) for c, i in enumerate(tiles4)], key=i1)[-1][0]] # find most unique tile palette (use range(7) instead of range(6))
        tilegroups = sorted(flat([[([c, c2], paldist(i, j)) for c2, j in enumerate(tiles4) if j != i] for c, i in enumerate(tiles4)]), key=i1)[-1][0]
        for i in range(6): tilegroups.append(sorted([(x, min([paldist(tiles4[j], tiles4[x]) for j in tilegroups])) for x in range(360) if x not in tilegroups], key=i1)[-1][0])
        
        print('Done with round 1')
        
        tilegroups = [[i] for i in tilegroups]

        # put all other tiles in the group of the nearest palette
        for i in range(360):
            if i not in flat(tilegroups):
                tilegroups[sorted([(c, paldist(tiles4[j[0]] if method == 'E' else groupimg(j), tiles4[i])) for c, j in enumerate(tilegroups)], key=i1)[0][0]].append(i)

        print('Done with round 2')
    else:
        # round 1 (tile x tile)
        for t in sorted([[c, sorted([[c2, paldist(i, j)] for c2, j in enumerate(tiles4)], key=i1)[1]] for c, i in enumerate(tiles4)], key=i1):
            s = t[0]
            m = t[1][0]
            if True in [s in i for i in tilegroups]: # already in a group
                pass
            elif True in [m in i for i in tilegroups]: # mate is already in a group
                tilegroups[[m in i for i in tilegroups].index(True)].append(s)
            else:
                tilegroups.append([s, m])
        
        print('Done with round 1')

        #moved = []

        while len(tilegroups) > 8:
            # round 2 (group x tile)

            if method in 'AB':
                tilegroups.sort(key=len)

                tg = tilegroups[1:]

                # force tiles out of small groups until there are 8 groups, causes images to look blocky sometimes
                for i in tilegroups[0]:                                 # method B is blockier but can have more accurate colors
                    tg.sort(key=lambda x: paldist(groupimg(x) if method == 'A' else realpal(groupimg(x)).convert('RGB'), tiles4[i].convert('RGB')))
                    tg[0].append(i)
                
                tilegroups = tg
                print(len(tilegroups) - 8, 'cycles left')
            elif method == 'C':
                '''
                incredibly slow method that stops at a certain number of groups

                tl = sorted(range(360), key=lambda x: min([paldist(tiles4[x], realpal(groupimg(i)).convert('RGB')) for i in [y for y in tilegroups if x not in y]]))
                tl = [z for z in tl if z not in moved][0]

                moved.append(tl)
                if len(moved) == 360: moved = []

                # put tiles in the closest group that is not their own
                gr = sorted([[tilegroups.index(i), paldist(tiles4[tl], realpal(groupimg(i)).convert('RGB'))] for i in [y for y in tilegroups if tl not in y]], key=i1)[0][0]
                tilegroups = [[j for j in i if j != tl] for i in tilegroups]
                tilegroups[gr].append(tl)

                tilegroups = [i for i in tilegroups if i]
                '''

                # group x group, works better on images with less colors
                tg = tilegroups.copy()
                tilegroups.sort(key=lambda x: min([paldist(groupimg(x), groupimg(i)) for i in [y for y in tg if x not in y]]))
                tl = tilegroups[0]
                tilegroups = tilegroups[1:]
                for i in tl:
                    tilegroups.sort(key=lambda x: paldist(groupimg(x), tiles4[i]))
                    tilegroups[0].append(i)

                #tilegroups.sort(key=lambda x: paldist(groupimg(x), groupimg(tl)))
                #tilegroups[0] += tl

                print(len(tilegroups) - 8, 'cycles left')
        
        print('Done with round 2')

    print('Loading output images...')

    g = Image.new('RGB', (160, 144))
    for i in tilegroups:
        for j in i:                           # without realpal here the image will have black pixels
            g.paste(tiles[j].copy().quantize(4, palette=realpal(groupimg(i))), tuple(x * 8 for x in i2xy(j)))

    #g.show()

    o = Image.new('RGB', (160, 144))

    for i in tilegroups:
        for j in i:
            t = tiles[j].copy().quantize(4, palette=realpal(groupimg(i)))
            t.putpalette([224, 248, 207, 134, 192, 108, 48, 104, 80, 7, 24, 33] * 64, 'RGB')
            t = t.convert('RGB')
            o.paste(t, tuple(x * 8 for x in i2xy(j)))
    
    #o.show()
    
    print(f'Done! {time.time() - start} s')

    loc_g = input('Colorized image file location (no input to not save): ')
    if loc_g: g.save(loc_g, 'png'); print('Saved to ' + loc_g)

    loc_o = input('Uncolorized image file location (no input to not save): ')
    if loc_o: o.save(loc_o, 'png'); print('Saved to ' + loc_o)

    # output palette data
    for c, i in enumerate(tilegroups):
        print(f'Palette {c + 1}:', '["' + '", "'.join(([rgb2hex(x[1]) for x in groupimg(i).getcolors()] + ['000000']*3)[:4]) + '"]')
    
    # output colorization data
    for y in range(18):
        print(('[' + ' '*17)[y] + ', '.join([str([xy2i(x, y) in i for i in tilegroups].index(True)) for x in range(20)]) + (','*17 + ']')[y])
