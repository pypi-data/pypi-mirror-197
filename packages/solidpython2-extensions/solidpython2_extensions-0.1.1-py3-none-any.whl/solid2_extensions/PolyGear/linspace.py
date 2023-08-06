from solid2.core.object_base import OpenSCADObject, OpenSCADConstant
from solid2.core.scad_import import extra_scad_include
from pathlib import Path

extra_scad_include(f"{Path(__file__).parent.parent / 'scad/PolyGear/linspace.scad'}", use_not_include=False)

class back(OpenSCADObject):
    def __init__(self, list=None, **kwargs):
       super().__init__("back", {"list" : list, **kwargs})

class pop_back(OpenSCADObject):
    def __init__(self, list=None, **kwargs):
       super().__init__("pop_back", {"list" : list, **kwargs})

class front(OpenSCADObject):
    def __init__(self, list=None, **kwargs):
       super().__init__("front", {"list" : list, **kwargs})

class pop_front(OpenSCADObject):
    def __init__(self, list=None, **kwargs):
       super().__init__("pop_front", {"list" : list, **kwargs})

class range(OpenSCADObject):
    def __init__(self, r=None, **kwargs):
       super().__init__("range", {"r" : r, **kwargs})

class indx(OpenSCADObject):
    def __init__(self, l=None, **kwargs):
       super().__init__("indx", {"l" : l, **kwargs})

class reverse(OpenSCADObject):
    def __init__(self, list=None, **kwargs):
       super().__init__("reverse", {"list" : list, **kwargs})

class flatten(OpenSCADObject):
    def __init__(self, list=None, **kwargs):
       super().__init__("flatten", {"list" : list, **kwargs})

class linspace(OpenSCADObject):
    def __init__(self, start=None, stop=None, n=None, **kwargs):
       super().__init__("linspace", {"start" : start, "stop" : stop, "n" : n, **kwargs})

class _linspace(OpenSCADObject):
    def __init__(self, start=None, stop=None, n=None, **kwargs):
       super().__init__("_linspace", {"start" : start, "stop" : stop, "n" : n, **kwargs})

class polar_linspace(OpenSCADObject):
    def __init__(self, w1=None, w2=None, n=None, cw=None, ccw=None, **kwargs):
       super().__init__("polar_linspace", {"w1" : w1, "w2" : w2, "n" : n, "cw" : cw, "ccw" : ccw, **kwargs})

class _polar_linspace(OpenSCADObject):
    def __init__(self, w1=None, w2=None, n=None, cw=None, ccw=None, **kwargs):
       super().__init__("_polar_linspace", {"w1" : w1, "w2" : w2, "n" : n, "cw" : cw, "ccw" : ccw, **kwargs})

