from solid2.core.object_base import OpenSCADObject, OpenSCADConstant
from solid2.core.scad_import import extra_scad_include
from pathlib import Path

extra_scad_include(f"{Path(__file__).parent.parent / 'scad/PolyGear/PolyGear.scad'}", use_not_include=False)

class PGDemo(OpenSCADObject):
    def __init__(self, **kwargs):
       super().__init__("PGDemo", {**kwargs})

class spur_gear(OpenSCADObject):
    def __init__(self, n=None, m=None, z=None, pressure_angle=None, helix_angle=None, backlash=None, w=None, a0=None, b0=None, tol=None, chamfer=None, chamfer_shift=None, add=None, ded=None, x=None, type=None, _fn=None, **kwargs):
       super().__init__("spur_gear", {"n" : n, "m" : m, "z" : z, "pressure_angle" : pressure_angle, "helix_angle" : helix_angle, "backlash" : backlash, "w" : w, "a0" : a0, "b0" : b0, "tol" : tol, "chamfer" : chamfer, "chamfer_shift" : chamfer_shift, "add" : add, "ded" : ded, "x" : x, "type" : type, "_fn" : _fn, **kwargs})

class bevel_gear(OpenSCADObject):
    def __init__(self, n=None, m=None, w=None, cone_angle=None, pressure_angle=None, helix_angle=None, backlash=None, z=None, a0=None, b0=None, tol=None, add=None, ded=None, x=None, type=None, _fn=None, **kwargs):
       super().__init__("bevel_gear", {"n" : n, "m" : m, "w" : w, "cone_angle" : cone_angle, "pressure_angle" : pressure_angle, "helix_angle" : helix_angle, "backlash" : backlash, "z" : z, "a0" : a0, "b0" : b0, "tol" : tol, "add" : add, "ded" : ded, "x" : x, "type" : type, "_fn" : _fn, **kwargs})

class bevel_pair(OpenSCADObject):
    def __init__(self, n1=None, n2=None, m=None, w=None, axis_angle=None, pressure_angle=None, helix_angle=None, backlash=None, only=None, a0=None, b0=None, tol=None, add=None, ded=None, x=None, type=None, _fn=None, **kwargs):
       super().__init__("bevel_pair", {"n1" : n1, "n2" : n2, "m" : m, "w" : w, "axis_angle" : axis_angle, "pressure_angle" : pressure_angle, "helix_angle" : helix_angle, "backlash" : backlash, "only" : only, "a0" : a0, "b0" : b0, "tol" : tol, "add" : add, "ded" : ded, "x" : x, "type" : type, "_fn" : _fn, **kwargs})

class constant(OpenSCADObject):
    def __init__(self, helix=None, _fn=None, **kwargs):
       super().__init__("constant", {"helix" : helix, "_fn" : _fn, **kwargs})

class zerol(OpenSCADObject):
    def __init__(self, helix=None, _fn=None, **kwargs):
       super().__init__("zerol", {"helix" : helix, "_fn" : _fn, **kwargs})

class spiral(OpenSCADObject):
    def __init__(self, helix=None, _fn=None, **kwargs):
       super().__init__("spiral", {"helix" : helix, "_fn" : _fn, **kwargs})

class herringbone(OpenSCADObject):
    def __init__(self, helix=None, _fn=None, **kwargs):
       super().__init__("herringbone", {"helix" : helix, "_fn" : _fn, **kwargs})

class bevel_gear_z_offset(OpenSCADObject):
    def __init__(self, n=None, m=None, cone_angle=None, ded=None, **kwargs):
       super().__init__("bevel_gear_z_offset", {"n" : n, "m" : m, "cone_angle" : cone_angle, "ded" : ded, **kwargs})

