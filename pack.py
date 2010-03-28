#import numpy
import random
import operator
from itertools import permutations

magnitude = 1000

class Box(object):
    """A rectangular prism"""
    def __init__(self, x=None, y=None, z=None):
        self.x = x if x else random.randint(1, magnitude)
        self.y = y if y else random.randint(1, magnitude)
        self.z = z if z else random.randint(1, magnitude)
        self.tu = (self.x, self.y, self.z)
        self.li = [self.x, self.y, self.z]
        self.di = {'x': self.x, 'y': self.y, 'z': self.z}

    def __repr__(self):
        return "Box%s" % str(self.tu)

    def __add__(self, other):
        if self.num_common >= 2:
            pass

    def __floordiv__(self, other):
        return self.x/other.x, self.y/other.y, self.z/other.z

    def __mul__(self, tup):
        if 0 in tup:
            return None
        return Box(self.x*tup[0], self.y*tup[1], self.z*tup[2])

    def __div__(self, other):
        return self.__floordiv__(other)

    def num_common(self, other):
        num = 0
        di = other.di.copy()
        for i in self.tu:
            if i in di.values():
                for k in di:
                    if di[k] == i:
                        num += 1
                        del di[k]
                        break
        return num

    def permutations(self):
        return permutations(self.tu)

    def upermutations(self):
        total=[]
        for a in self.permutations():
            if a not in total:
                total.append(a)
                yield Box(*a)

    def fill_with(self, other):
        for b in other.upermutations():
            m = (self.x/b.x, self.y/b.y, self.z/b.z)
            yield (b, m)

    def volume(self):
        return self.x * self.y * self.z



if __name__ == '__main__':
    container = Box()
    i = Box(25,35,10)
    print container
    print "filling with ", i
    for box, mult in container.fill_with(i):
        print box, '*', mult, '=', box*mult, 'for volume =', (box*mult).volume(), 'number = ', reduce(operator.mul,mult)

"""
>>> from pack import *
>>> b = Box(854, 566, 651)
>>> i = Box(10, 15, 20)
>>> i.volume()
3000
import operator
>>> for box, mult in b.fill_with(i):
...     print box, '*', mult, '=', box*mult, 'for volume =', (box*mult).volume(), 'number = ', reduce(operator.mul,mult)
...
Box(10, 15, 20) * (85, 37, 32) = Box(850, 555, 640) for volume = 301920000 number =  100640
Box(10, 20, 15) * (85, 28, 43) = Box(850, 560, 645) for volume = 307020000 number =  102340
Box(15, 10, 20) * (56, 56, 32) = Box(840, 560, 640) for volume = 301056000 number =  100352
Box(15, 20, 10) * (56, 28, 65) = Box(840, 560, 650) for volume = 305760000 number =  101920
Box(20, 10, 15) * (42, 56, 43) = Box(840, 560, 645) for volume = 303408000 number =  101136
Box(20, 15, 10) * (42, 37, 65) = Box(840, 555, 650) for volume = 303030000 number =  101010
"""
