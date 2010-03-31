#import numpy
import random
import operator
from itertools import permutations

magnitude = 1000

class Box(object):
    """A rectangular prism"""
    def __init__(self, x=None, y=None, z=None, *args, **kwargs):
        self.x = x if x else random.randint(1, magnitude)
        self.y = y if y else random.randint(1, magnitude)
        self.z = z if z else random.randint(1, magnitude)
        self.tu = (self.x, self.y, self.z)
        self.li = [self.x, self.y, self.z]
        self.di = {'x': self.x, 'y': self.y, 'z': self.z}

    def __repr__(self):
        return "Box%s" % str(self.tu)

    def __add__(self, other):
        """With two lengths in common, we add the 3rds.
        
        If 3 lengths are common, we return 3 different boxes to choose"""
        l1 = sorted(self.tu)
        copy = sorted(self.tu)
        l2 = sorted(other.tu)
        common = []
        for v in l1:
            if v in l2:
                common.append(l2.pop(l2.index(v)))
                copy.pop(copy.index(v))

        if len(common) < 2:
            return "Not a box"

        if len(common) == 2:
            return Box(*(common+[copy[0]+l2[0]]))

        if len(common) == 3:
            return (
                    Box(*(common[0]*2, common[1], common[2])),
                    Box(*(common[0], common[1]*2, common[2])),
                    Box(*(common[0], common[1], common[2]*2)),
            )

    def __sub__(self, other):
        l1 = sorted(self.tu)
        copy = sorted(self.tu)
        l2 = sorted(other.tu)
        common = []
        for v in l1:
            if v in l2:
                common.append(l2.pop(l2.index(v)))
                copy.pop(copy.index(v))

        if len(common) < 2:
            return "Not a box"

        if len(common) == 2:
            return Box(*(common+[copy[0]-l2[0]]))

        if len(common) == 3:
            return None

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

class Container(Box):
    """A Box with a cost"""
    def __init__(self, *args, **kwargs):
        super(Container, self).__init__(*args, **kwargs)
        self.cost = kwargs['cost']

    def __repr__(self):
        return "[Container%s, cost=%s]" % (str(self.tu), self.cost)

    def cost_per(self):
        return float(self.cost)/(reduce(operator.mul, self.tu))

class BoxList(object):
    """A list of Boxes"""
    def __init__(self, li):
        self.li = li

    def total_volume(self):
        return reduce(operator.add, [i.volume() for i in self.li])

    def sorted(self, comp, **kwargs):
        return sorted(self.li, comp, **kwargs)

    def sorted_volume(self,**kwargs):
        return self.sorted(lambda x, y: cmp(x.volume(), y.volume()))

    def sorted_x(self, **kwargs):
        return self.sorted(lambda x, y: cmp(x.x, y.x))


class ContainerList(BoxList):
    """A list of Containers"""
    def sorted_cost(self, **kwargs):
        return self.sorted(lambda x, y: cmp(x.cost, y.cost))


def min_cost_required(container_list, item_list):
    """Takes a list of containers and a list of items and returns the minimum cost"""
    pass


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
