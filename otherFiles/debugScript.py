"""Onni Kolkka 
150832953 (student number)
created 10.12.2022 21.02
"""
import threading
import time
import tkinter
from collections import namedtuple
from copy import copy
import queue
from ctypes import windll

#region test 1
Colour = namedtuple('Colour', 'r,g,b')
Colour.copy = lambda self: copy(self)

black = Colour(0, 0, 0)
white = Colour(255, 255, 255)  # Colour ranges are not enforced.


class Bitmap():
    def __init__(self, width=40, height=40, background=white):
        assert width > 0 and height > 0 and type(background) == Colour
        self.width = width
        self.height = height
        self.background = background
        self.map = [[background] * width] * height

    def fillrect(self, x, y, width, height, colour=black):
        assert x >= 0 and y >= 0 and width > 0 and height > 0 and type(colour) == Colour
        for h in range(height):
            for w in range(width):
                self.map[y + h][x + w] = colour.copy()

    def chardisplay(self):
        txt = [''.join(' ' if bit == self.background else '@'
                       for bit in row)
               for row in self.map]
        # Boxing
        txt = ['|' + row + '|' for row in txt]
        txt.insert(0, '+' + '-' * self.width + '+')
        txt.append('+' + '-' * self.width + '+')
        print('\n'.join(reversed(txt)))

    def set(self, x, y, colour=black):
        assert type(colour) == Colour
        self.map[y][x] = colour

    def get(self, x, y):
        return self.map[y][x]


def main1():
    # String masquerading as ppm file (version P3)

    import io
    ppmfileout = io.StringIO('')

    def writeppmp3(self, f):
        self.writeppm(f, ppmformat='P3')

    def writeppm(self, f, ppmformat='P6'):
        assert ppmformat in ['P3', 'P6'], 'Format wrong'
        magic = ppmformat + ' '
        comment = '# generated from Bitmap.writeppm\n'
        maxval = max(max(max(bit) for bit in row) for row in self.map)
        assert ppmformat == 'P3' or 0 <= maxval < 256, 'R,G,B must fit in a byte'
        fwrite = f.write
        if ppmformat == 'P6':
            fwrite = lambda s: f.write(bytes(s, 'UTF-8'))
            maxval = 128
        else:
            fwrite = f.write
            numsize = len(str(maxval))
        # fwrite(magic)
        # fwrite(comment)
        fwrite(magic +'%i %i %i ' % (self.canv_width, self.canv_height, maxval))
        import time
        start_time = time.time()
        """for h in range(self.height):
            for w in range(self.width):
                r, g, b = self.get(w, h)
                if ppmformat == 'P3':
                    fwrite('   %*i %*i %*i' % (numsize, r, numsize, g, numsize, b))
                    #string.__add__('   %*i %*i %*i' % (numsize, r, numsize, g, numsize, b))
                else:
                    fwrite('%c%c%c' % (r, g, b))
                    #string.__add__('%c%c%c' % (r, g, b))
            if ppmformat == 'P3':
                fwrite('\n')
                #string.__add__('\n')
        #fwrite(string)"""
        if ppmformat == 'P3':
            for h in range(self.canv_height):
                for w in range(self.canv_width):
                    r, g, b = self.get(w, h)
                    fwrite('   %*i %*i %*i' % (numsize, r, numsize, g, numsize, b))
                        # string.__add__('   %*i %*i %*i' % (numsize, r, numsize, g, numsize, b))
                fwrite('\n')
        else:
            f.write((bytes('%c%c%c' % (111,118,121), 'UTF-8') * self.canv_width * self.canv_height))
        # fwrite(string)
        print("--- %s seconds ---" % (time.time() - start_time))

    Bitmap.writeppmp3 = writeppmp3
    Bitmap.writeppm = writeppm

    # Draw something simple
    bitmap = Bitmap(1920,1080, black)
    bitmap.fillrect(1, 0, 1, 2, white)
    bitmap.set(3, 3, Colour(127, 0, 63))

    # Write a P6 file
    ppmfileout = open('tmp.ppm', 'wb+')
    print(len(ppmfileout.read()))
    bitmap.writeppm(ppmfileout)
    ppmfileout.close()


class ANSI():
    def background(code):
        return "\33[{code}m".format(code=code)

    def style_text(code):
        return "\33[{code}m".format(code=code)

    def color_text(code):
        return "\33[{code}m".format(code=code)
# endregion

#region test 2
def main2():
    a=[(0,)]*(int(1e7))
    b=[0]*(int(9e7))

    for i in range(int(1e7)):
        a[i]=((1,2,3),(4,5,6),(7,8,9))

    for i in range(int(9e7)):
        b[i]=(i%9+1)

    t=-time.time()
    s=0
    for i in a:
        s+=i[0][0] + i[1][0] + i[2][0]+ \
           i[0][1] + i[1][1] + i[2][1]+ \
           i[0][2] + i[1][2] + i[2][2]
    print(t+time.time())
    print(s)
    print()

    t=-time.time()
    s=0
    for i in range(len(a)):
        s+=a[i][0][0] + a[i][1][0] + a[i][2][0]+ \
           a[i][0][1] + a[i][1][1] + a[i][2][1]+ \
           a[i][0][2] + a[i][1][2] + a[i][2][2]
    print(t+time.time())
    print(s)
    print()

    t=-time.time()
    s=0
    for i in range(0,len(b),3):
        s+=b[i+0] + b[i+1] + b[i+2]
    print(t+time.time())
    print(s)
    print()
    t=-time.time()
    s=0
    for i in b:
        s+=i
    print(t+time.time())
    print(s)
# endregion

# region test 3
def input():
    pass

#endregion

if __name__ == '__main__':
    test3()
