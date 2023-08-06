from solid2.core.object_base import OpenSCADObject, OpenSCADConstant
from solid2.core.scad_import import extra_scad_include
from pathlib import Path

extra_scad_include(f"{Path(__file__).parent.parent / 'scad/PolyGear/shortcuts.scad'}", use_not_include=False)

class T(OpenSCADObject):
    def __init__(self, x=None, y=None, z=None, **kwargs):
       super().__init__("T", {"x" : x, "y" : y, "z" : z, **kwargs})

class TK(OpenSCADObject):
    def __init__(self, x=None, y=None, z=None, **kwargs):
       super().__init__("TK", {"x" : x, "y" : y, "z" : z, **kwargs})

class Tx(OpenSCADObject):
    def __init__(self, x=None, **kwargs):
       super().__init__("Tx", {"x" : x, **kwargs})

class Ty(OpenSCADObject):
    def __init__(self, y=None, **kwargs):
       super().__init__("Ty", {"y" : y, **kwargs})

class Tz(OpenSCADObject):
    def __init__(self, z=None, **kwargs):
       super().__init__("Tz", {"z" : z, **kwargs})

class TKx(OpenSCADObject):
    def __init__(self, x=None, **kwargs):
       super().__init__("TKx", {"x" : x, **kwargs})

class TKy(OpenSCADObject):
    def __init__(self, y=None, **kwargs):
       super().__init__("TKy", {"y" : y, **kwargs})

class TKz(OpenSCADObject):
    def __init__(self, z=None, **kwargs):
       super().__init__("TKz", {"z" : z, **kwargs})

class R(OpenSCADObject):
    def __init__(self, x=None, y=None, z=None, **kwargs):
       super().__init__("R", {"x" : x, "y" : y, "z" : z, **kwargs})

class Rx(OpenSCADObject):
    def __init__(self, x=None, **kwargs):
       super().__init__("Rx", {"x" : x, **kwargs})

class Ry(OpenSCADObject):
    def __init__(self, y=None, **kwargs):
       super().__init__("Ry", {"y" : y, **kwargs})

class Rz(OpenSCADObject):
    def __init__(self, z=None, **kwargs):
       super().__init__("Rz", {"z" : z, **kwargs})

class M(OpenSCADObject):
    def __init__(self, x=None, y=None, z=None, **kwargs):
       super().__init__("M", {"x" : x, "y" : y, "z" : z, **kwargs})

class Mx(OpenSCADObject):
    def __init__(self, **kwargs):
       super().__init__("Mx", {**kwargs})

class My(OpenSCADObject):
    def __init__(self, **kwargs):
       super().__init__("My", {**kwargs})

class Mz(OpenSCADObject):
    def __init__(self, **kwargs):
       super().__init__("Mz", {**kwargs})

class RK(OpenSCADObject):
    def __init__(self, x=None, y=None, z=None, **kwargs):
       super().__init__("RK", {"x" : x, "y" : y, "z" : z, **kwargs})

class RKx(OpenSCADObject):
    def __init__(self, x=None, **kwargs):
       super().__init__("RKx", {"x" : x, **kwargs})

class RKy(OpenSCADObject):
    def __init__(self, y=None, **kwargs):
       super().__init__("RKy", {"y" : y, **kwargs})

class RKz(OpenSCADObject):
    def __init__(self, z=None, **kwargs):
       super().__init__("RKz", {"z" : z, **kwargs})

class MK(OpenSCADObject):
    def __init__(self, x=None, y=None, z=None, **kwargs):
       super().__init__("MK", {"x" : x, "y" : y, "z" : z, **kwargs})

class MKx(OpenSCADObject):
    def __init__(self, **kwargs):
       super().__init__("MKx", {**kwargs})

class MKy(OpenSCADObject):
    def __init__(self, **kwargs):
       super().__init__("MKy", {**kwargs})

class MKz(OpenSCADObject):
    def __init__(self, **kwargs):
       super().__init__("MKz", {**kwargs})

class S(OpenSCADObject):
    def __init__(self, x=None, y=None, z=None, **kwargs):
       super().__init__("S", {"x" : x, "y" : y, "z" : z, **kwargs})

class Sx(OpenSCADObject):
    def __init__(self, x=None, **kwargs):
       super().__init__("Sx", {"x" : x, **kwargs})

class Sy(OpenSCADObject):
    def __init__(self, y=None, **kwargs):
       super().__init__("Sy", {"y" : y, **kwargs})

class Sz(OpenSCADObject):
    def __init__(self, z=None, **kwargs):
       super().__init__("Sz", {"z" : z, **kwargs})

class Skew(OpenSCADObject):
    def __init__(self, x=None, y=None, z=None, a=None, b=None, c=None, **kwargs):
       super().__init__("Skew", {"x" : x, "y" : y, "z" : z, "a" : a, "b" : b, "c" : c, **kwargs})

class skew(OpenSCADObject):
    def __init__(self, x=None, y=None, z=None, a=None, b=None, c=None, **kwargs):
       super().__init__("skew", {"x" : x, "y" : y, "z" : z, "a" : a, "b" : b, "c" : c, **kwargs})

class SkX(OpenSCADObject):
    def __init__(self, x=None, **kwargs):
       super().__init__("SkX", {"x" : x, **kwargs})

class SkY(OpenSCADObject):
    def __init__(self, y=None, **kwargs):
       super().__init__("SkY", {"y" : y, **kwargs})

class SkZ(OpenSCADObject):
    def __init__(self, z=None, **kwargs):
       super().__init__("SkZ", {"z" : z, **kwargs})

class SkewX(OpenSCADObject):
    def __init__(self, x=None, **kwargs):
       super().__init__("SkewX", {"x" : x, **kwargs})

class SkewY(OpenSCADObject):
    def __init__(self, y=None, **kwargs):
       super().__init__("SkewY", {"y" : y, **kwargs})

class SkewZ(OpenSCADObject):
    def __init__(self, z=None, **kwargs):
       super().__init__("SkewZ", {"z" : z, **kwargs})

class LiEx(OpenSCADObject):
    def __init__(self, h=None, tw=None, sl=None, sc=None, C=None, **kwargs):
       super().__init__("LiEx", {"h" : h, "tw" : tw, "sl" : sl, "sc" : sc, "C" : C, **kwargs})

class D(OpenSCADObject):
    def __init__(self, **kwargs):
       super().__init__("D", {**kwargs})

class U(OpenSCADObject):
    def __init__(self, **kwargs):
       super().__init__("U", {**kwargs})

class I(OpenSCADObject):
    def __init__(self, **kwargs):
       super().__init__("I", {**kwargs})

class rotN(OpenSCADObject):
    def __init__(self, r=None, N=None, offs=None, M=None, **kwargs):
       super().__init__("rotN", {"r" : r, "N" : N, "offs" : offs, "M" : M, **kwargs})

class forN(OpenSCADObject):
    def __init__(self, r=None, N=None, offs=None, M=None, **kwargs):
       super().__init__("forN", {"r" : r, "N" : N, "offs" : offs, "M" : M, **kwargs})

class forX(OpenSCADObject):
    def __init__(self, dx=None, N=None, **kwargs):
       super().__init__("forX", {"dx" : dx, "N" : N, **kwargs})

class forY(OpenSCADObject):
    def __init__(self, dy=None, M=None, **kwargs):
       super().__init__("forY", {"dy" : dy, "M" : M, **kwargs})

class forZ(OpenSCADObject):
    def __init__(self, dz=None, M=None, **kwargs):
       super().__init__("forZ", {"dz" : dz, "M" : M, **kwargs})

class forXY(OpenSCADObject):
    def __init__(self, dx=None, N=None, dy=None, M=None, **kwargs):
       super().__init__("forXY", {"dx" : dx, "N" : N, "dy" : dy, "M" : M, **kwargs})

class Sq(OpenSCADObject):
    def __init__(self, x=None, y=None, center=None, **kwargs):
       super().__init__("Sq", {"x" : x, "y" : y, "center" : center, **kwargs})

class Ci(OpenSCADObject):
    def __init__(self, r=None, d=None, **kwargs):
       super().__init__("Ci", {"r" : r, "d" : d, **kwargs})

class CiH(OpenSCADObject):
    def __init__(self, r=None, w=None, d=None, **kwargs):
       super().__init__("CiH", {"r" : r, "w" : w, "d" : d, **kwargs})

class CiS(OpenSCADObject):
    def __init__(self, r=None, w1=None, w2=None, d=None, **kwargs):
       super().__init__("CiS", {"r" : r, "w1" : w1, "w2" : w2, "d" : d, **kwargs})

class Cy(OpenSCADObject):
    def __init__(self, r=None, h=None, C=None, r1=None, r2=None, d=None, d1=None, d2=None, **kwargs):
       super().__init__("Cy", {"r" : r, "h" : h, "C" : C, "r1" : r1, "r2" : r2, "d" : d, "d1" : d1, "d2" : d2, **kwargs})

class Cu(OpenSCADObject):
    def __init__(self, x=None, y=None, z=None, C=None, **kwargs):
       super().__init__("Cu", {"x" : x, "y" : y, "z" : z, "C" : C, **kwargs})

class CuR(OpenSCADObject):
    def __init__(self, x=None, y=None, z=None, r=None, C=None, **kwargs):
       super().__init__("CuR", {"x" : x, "y" : y, "z" : z, "r" : r, "C" : C, **kwargs})

class CyR(OpenSCADObject):
    def __init__(self, r=None, h=None, r_=None, d=None, r1=None, r2=None, d1=None, d2=None, C=None, **kwargs):
       super().__init__("CyR", {"r" : r, "h" : h, "r_" : r_, "d" : d, "r1" : r1, "r2" : r2, "d1" : d1, "d2" : d2, "C" : C, **kwargs})

class CyH(OpenSCADObject):
    def __init__(self, r=None, h=None, w=None, C=None, r1=None, r2=None, d=None, d1=None, d2=None, **kwargs):
       super().__init__("CyH", {"r" : r, "h" : h, "w" : w, "C" : C, "r1" : r1, "r2" : r2, "d" : d, "d1" : d1, "d2" : d2, **kwargs})

class CyS(OpenSCADObject):
    def __init__(self, r=None, h=None, w1=None, w2=None, C=None, r1=None, r2=None, d=None, d1=None, d2=None, **kwargs):
       super().__init__("CyS", {"r" : r, "h" : h, "w1" : w1, "w2" : w2, "C" : C, "r1" : r1, "r2" : r2, "d" : d, "d1" : d1, "d2" : d2, **kwargs})

class Ri(OpenSCADObject):
    def __init__(self, R=None, r=None, h=None, C=None, D=None, d=None, **kwargs):
       super().__init__("Ri", {"R" : R, "r" : r, "h" : h, "C" : C, "D" : D, "d" : d, **kwargs})

class RiS(OpenSCADObject):
    def __init__(self, R=None, r=None, h=None, w1=None, w2=None, C=None, D=None, d=None, **kwargs):
       super().__init__("RiS", {"R" : R, "r" : r, "h" : h, "w1" : w1, "w2" : w2, "C" : C, "D" : D, "d" : d, **kwargs})

class RiH(OpenSCADObject):
    def __init__(self, R=None, r=None, h=None, w=None, C=None, D=None, d=None, **kwargs):
       super().__init__("RiH", {"R" : R, "r" : r, "h" : h, "w" : w, "C" : C, "D" : D, "d" : d, **kwargs})

class Pie(OpenSCADObject):
    def __init__(self, r=None, h=None, w1=None, w2=None, C=None, d=None, **kwargs):
       super().__init__("Pie", {"r" : r, "h" : h, "w1" : w1, "w2" : w2, "C" : C, "d" : d, **kwargs})

class Sp(OpenSCADObject):
    def __init__(self, r=None, **kwargs):
       super().__init__("Sp", {"r" : r, **kwargs})

class SpH(OpenSCADObject):
    def __init__(self, r=None, w1=None, w2=None, **kwargs):
       super().__init__("SpH", {"r" : r, "w1" : w1, "w2" : w2, **kwargs})

class To(OpenSCADObject):
    def __init__(self, R=None, r=None, r1=None, w=None, w1=None, w2=None, **kwargs):
       super().__init__("To", {"R" : R, "r" : r, "r1" : r1, "w" : w, "w1" : w1, "w2" : w2, **kwargs})

class Col(OpenSCADObject):
    def __init__(self, r=None, g=None, b=None, t=None, **kwargs):
       super().__init__("Col", {"r" : r, "g" : g, "b" : b, "t" : t, **kwargs})

class cube_rounded(OpenSCADObject):
    def __init__(self, size=None, r=None, center=None, **kwargs):
       super().__init__("cube_rounded", {"size" : size, "r" : r, "center" : center, **kwargs})

class circle_half(OpenSCADObject):
    def __init__(self, r=None, w=None, d=None, **kwargs):
       super().__init__("circle_half", {"r" : r, "w" : w, "d" : d, **kwargs})

class circle_sector(OpenSCADObject):
    def __init__(self, r=None, w1=None, w2=None, d=None, **kwargs):
       super().__init__("circle_sector", {"r" : r, "w1" : w1, "w2" : w2, "d" : d, **kwargs})

class cylinder_half(OpenSCADObject):
    def __init__(self, r=None, h=None, center=None, r1=None, r2=None, d=None, d1=None, d2=None, **kwargs):
       super().__init__("cylinder_half", {"r" : r, "h" : h, "center" : center, "r1" : r1, "r2" : r2, "d" : d, "d1" : d1, "d2" : d2, **kwargs})

class cylinder_sector(OpenSCADObject):
    def __init__(self, r=None, h=None, w1=None, w2=None, center=None, r1=None, r2=None, d=None, d1=None, d2=None, **kwargs):
       super().__init__("cylinder_sector", {"r" : r, "h" : h, "w1" : w1, "w2" : w2, "center" : center, "r1" : r1, "r2" : r2, "d" : d, "d1" : d1, "d2" : d2, **kwargs})

class cylinder_sector_(OpenSCADObject):
    def __init__(self, r=None, h=None, w1=None, w2=None, center=None, **kwargs):
       super().__init__("cylinder_sector_", {"r" : r, "h" : h, "w1" : w1, "w2" : w2, "center" : center, **kwargs})

class cylinder_rounded(OpenSCADObject):
    def __init__(self, r=None, h=None, r_=None, d=None, r1=None, r2=None, d1=None, d2=None, center=None, **kwargs):
       super().__init__("cylinder_rounded", {"r" : r, "h" : h, "r_" : r_, "d" : d, "r1" : r1, "r2" : r2, "d1" : d1, "d2" : d2, "center" : center, **kwargs})

class ring(OpenSCADObject):
    def __init__(self, R=None, r=None, h=None, center=None, D=None, d=None, **kwargs):
       super().__init__("ring", {"R" : R, "r" : r, "h" : h, "center" : center, "D" : D, "d" : d, **kwargs})

class ring_half(OpenSCADObject):
    def __init__(self, R=None, r=None, h=None, w=None, center=None, D=None, d=None, **kwargs):
       super().__init__("ring_half", {"R" : R, "r" : r, "h" : h, "w" : w, "center" : center, "D" : D, "d" : d, **kwargs})

class ring_sector(OpenSCADObject):
    def __init__(self, R=None, r=None, h=None, w1=None, w2=None, center=None, D=None, d=None, **kwargs):
       super().__init__("ring_sector", {"R" : R, "r" : r, "h" : h, "w1" : w1, "w2" : w2, "center" : center, "D" : D, "d" : d, **kwargs})

class sphere_half(OpenSCADObject):
    def __init__(self, r=None, w1=None, w2=None, **kwargs):
       super().__init__("sphere_half", {"r" : r, "w1" : w1, "w2" : w2, **kwargs})

class torus(OpenSCADObject):
    def __init__(self, R=None, r=None, r1=None, w=None, w1=None, w2=None, **kwargs):
       super().__init__("torus", {"R" : R, "r" : r, "r1" : r1, "w" : w, "w1" : w1, "w2" : w2, **kwargs})

class place_in_rect(OpenSCADObject):
    def __init__(self, dx=None, dy=None, **kwargs):
       super().__init__("place_in_rect", {"dx" : dx, "dy" : dy, **kwargs})

class measure(OpenSCADObject):
    def __init__(self, s=None, x=None, y=None, z=None, **kwargs):
       super().__init__("measure", {"s" : s, "x" : x, "y" : y, "z" : z, **kwargs})

class Rg(OpenSCADObject):
    def __init__(self, N=None, **kwargs):
       super().__init__("Rg", {"N" : N, **kwargs})

