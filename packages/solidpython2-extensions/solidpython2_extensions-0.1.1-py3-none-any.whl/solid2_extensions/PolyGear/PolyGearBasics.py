from solid2.core.object_base import OpenSCADObject, OpenSCADConstant
from solid2.core.scad_import import extra_scad_include
from pathlib import Path

extra_scad_include(f"{Path(__file__).parent.parent / 'scad/PolyGear/PolyGearBasics.scad'}", use_not_include=False)

class phi_b1(OpenSCADObject):
    def __init__(self, r0=None, rb=None, s0=None, flank=None, type=None, **kwargs):
       super().__init__("phi_b1", {"r0" : r0, "rb" : rb, "s0" : s0, "flank" : flank, "type" : type, **kwargs})

class phi_bi(OpenSCADObject):
    def __init__(self, i=None, n=None, r0=None, rb=None, s0=None, flank=None, type=None, **kwargs):
       super().__init__("phi_bi", {"i" : i, "n" : n, "r0" : r0, "rb" : rb, "s0" : s0, "flank" : flank, "type" : type, **kwargs})

class prof(OpenSCADObject):
    def __init__(self, at=None, z=None, i=None, n=None, r0=None, rb=None, s0=None, c=None, flank=None, type=None, **kwargs):
       super().__init__("prof", {"at" : at, "z" : z, "i" : i, "n" : n, "r0" : r0, "rb" : rb, "s0" : s0, "c" : c, "flank" : flank, "type" : type, **kwargs})

class linearized_prof(OpenSCADObject):
    def __init__(self, t=None, z=None, i=None, n=None, r0=None, rb=None, s0=None, c=None, flank=None, type=None, **kwargs):
       super().__init__("linearized_prof", {"t" : t, "z" : z, "i" : i, "n" : n, "r0" : r0, "rb" : rb, "s0" : s0, "c" : c, "flank" : flank, "type" : type, **kwargs})

class f_r0_add(OpenSCADObject):
    def __init__(self, r0=None, m=None, add=None, **kwargs):
       super().__init__("f_r0_add", {"r0" : r0, "m" : m, "add" : add, **kwargs})

class f_r0_ded(OpenSCADObject):
    def __init__(self, r0=None, m=None, ded=None, **kwargs):
       super().__init__("f_r0_ded", {"r0" : r0, "m" : m, "ded" : ded, **kwargs})

class gear_section(OpenSCADObject):
    def __init__(self, n=None, m=None, z=None, pressure_angle=None, helix_angle=None, backlash=None, add=None, ded=None, x=None, type=None, _fn=None, **kwargs):
       super().__init__("gear_section", {"n" : n, "m" : m, "z" : z, "pressure_angle" : pressure_angle, "helix_angle" : helix_angle, "backlash" : backlash, "add" : add, "ded" : ded, "x" : x, "type" : type, "_fn" : _fn, **kwargs})

class split_quad(OpenSCADObject):
    def __init__(self, q=None, flip=None, **kwargs):
       super().__init__("split_quad", {"q" : q, "flip" : flip, **kwargs})

class make_side_faces(OpenSCADObject):
    def __init__(self, npts=None, nlayers=None, **kwargs):
       super().__init__("make_side_faces", {"npts" : npts, "nlayers" : nlayers, **kwargs})

class make_cap_faces(OpenSCADObject):
    def __init__(self, Npts=None, Nlayers=None, Nteeth=None, **kwargs):
       super().__init__("make_cap_faces", {"Npts" : Npts, "Nlayers" : Nlayers, "Nteeth" : Nteeth, **kwargs})

