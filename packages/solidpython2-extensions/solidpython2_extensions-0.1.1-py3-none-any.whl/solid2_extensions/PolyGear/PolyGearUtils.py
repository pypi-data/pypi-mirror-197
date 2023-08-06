from solid2.core.object_base import OpenSCADObject, OpenSCADConstant
from solid2.core.scad_import import extra_scad_include
from pathlib import Path

extra_scad_include(f"{Path(__file__).parent.parent / 'scad/PolyGear/PolyGearUtils.scad'}", use_not_include=False)

d2r = OpenSCADConstant('d2r')
r2d = OpenSCADConstant('r2d')
class draw(OpenSCADObject):
    def __init__(self, pts=None, size=None, **kwargs):
       super().__init__("draw", {"pts" : pts, "size" : size, **kwargs})

class radius(OpenSCADObject):
    def __init__(self, x=None, y=None, **kwargs):
       super().__init__("radius", {"x" : x, "y" : y, **kwargs})

class _polar2cartesian(OpenSCADObject):
    def __init__(self, r=None, theta=None, **kwargs):
       super().__init__("_polar2cartesian", {"r" : r, "theta" : theta, **kwargs})

class _cartesian2polar(OpenSCADObject):
    def __init__(self, x=None, y=None, **kwargs):
       super().__init__("_cartesian2polar", {"x" : x, "y" : y, **kwargs})

class polar2cartesian(OpenSCADObject):
    def __init__(self, pts=None, **kwargs):
       super().__init__("polar2cartesian", {"pts" : pts, **kwargs})

class cartesian2polar(OpenSCADObject):
    def __init__(self, pts=None, **kwargs):
       super().__init__("cartesian2polar", {"pts" : pts, **kwargs})

class polar(OpenSCADObject):
    def __init__(self, r=None, theta=None, **kwargs):
       super().__init__("polar", {"r" : r, "theta" : theta, **kwargs})

class inv(OpenSCADObject):
    def __init__(self, a=None, **kwargs):
       super().__init__("inv", {"a" : a, **kwargs})

class lst_repeat(OpenSCADObject):
    def __init__(self, item=None, times=None, **kwargs):
       super().__init__("lst_repeat", {"item" : item, "times" : times, **kwargs})

class Tpts(OpenSCADObject):
    def __init__(self, pts=None, x=None, y=None, z=None, **kwargs):
       super().__init__("Tpts", {"pts" : pts, "x" : x, "y" : y, "z" : z, **kwargs})

class Txpts(OpenSCADObject):
    def __init__(self, pts=None, x=None, **kwargs):
       super().__init__("Txpts", {"pts" : pts, "x" : x, **kwargs})

class Typts(OpenSCADObject):
    def __init__(self, pts=None, y=None, **kwargs):
       super().__init__("Typts", {"pts" : pts, "y" : y, **kwargs})

class Tzpts(OpenSCADObject):
    def __init__(self, pts=None, z=None, **kwargs):
       super().__init__("Tzpts", {"pts" : pts, "z" : z, **kwargs})

class find_circle(OpenSCADObject):
    def __init__(self, p1=None, p2=None, p3=None, **kwargs):
       super().__init__("find_circle", {"p1" : p1, "p2" : p2, "p3" : p3, **kwargs})

class make_arc(OpenSCADObject):
    def __init__(self, p1=None, p2=None, p3=None, n=None, **kwargs):
       super().__init__("make_arc", {"p1" : p1, "p2" : p2, "p3" : p3, "n" : n, **kwargs})

class make_arc_no_extremes(OpenSCADObject):
    def __init__(self, p1=None, p2=None, p3=None, n=None, **kwargs):
       super().__init__("make_arc_no_extremes", {"p1" : p1, "p2" : p2, "p3" : p3, "n" : n, **kwargs})

class make_circle(OpenSCADObject):
    def __init__(self, p1=None, p2=None, p3=None, n=None, **kwargs):
       super().__init__("make_circle", {"p1" : p1, "p2" : p2, "p3" : p3, "n" : n, **kwargs})

class p2p3(OpenSCADObject):
    def __init__(self, p2=None, z=None, res=None, **kwargs):
       super().__init__("p2p3", {"p2" : p2, "z" : z, "res" : res, **kwargs})

class reverse_lst(OpenSCADObject):
    def __init__(self, lst=None, **kwargs):
       super().__init__("reverse_lst", {"lst" : lst, **kwargs})

class rotate_lst(OpenSCADObject):
    def __init__(self, lst=None, n=None, **kwargs):
       super().__init__("rotate_lst", {"lst" : lst, "n" : n, **kwargs})

class constrain_angle(OpenSCADObject):
    def __init__(self, x=None, **kwargs):
       super().__init__("constrain_angle", {"x" : x, **kwargs})

class cum_sum(OpenSCADObject):
    def __init__(self, lst=None, i=None, **kwargs):
       super().__init__("cum_sum", {"lst" : lst, "i" : i, **kwargs})

class cum_avg(OpenSCADObject):
    def __init__(self, lst=None, **kwargs):
       super().__init__("cum_avg", {"lst" : lst, **kwargs})

class fold_on_sphere(OpenSCADObject):
    def __init__(self, pts=None, R=None, C=None, **kwargs):
       super().__init__("fold_on_sphere", {"pts" : pts, "R" : R, "C" : C, **kwargs})

