# This file was automatically generated by SWIG (https://www.swig.org).
# Version 4.1.0
#
# Do not make changes to this file unless you know what you are doing - modify
# the SWIG interface file instead.

"""SWIG wrapper for the CGAL Polygon Mesh Processing package provided under the GPL-3.0+ license"""

from sys import version_info as _swig_python_version_info
# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _CGAL_Polygon_mesh_processing
else:
    import _CGAL_Polygon_mesh_processing

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)


def _swig_setattr_nondynamic_instance_variable(set):
    def set_instance_attr(self, name, value):
        if name == "this":
            set(self, name, value)
        elif name == "thisown":
            self.this.own(value)
        elif hasattr(self, name) and isinstance(getattr(type(self), name), property):
            set(self, name, value)
        else:
            raise AttributeError("You cannot add instance attributes to %s" % self)
    return set_instance_attr


def _swig_setattr_nondynamic_class_variable(set):
    def set_class_attr(cls, name, value):
        if hasattr(cls, name) and not isinstance(getattr(cls, name), property):
            set(cls, name, value)
        else:
            raise AttributeError("You cannot add class attributes to %s" % cls)
    return set_class_attr


def _swig_add_metaclass(metaclass):
    """Class decorator for adding a metaclass to a SWIG wrapped class - a slimmed down version of six.add_metaclass"""
    def wrapper(cls):
        return metaclass(cls.__name__, cls.__bases__, cls.__dict__.copy())
    return wrapper


class _SwigNonDynamicMeta(type):
    """Meta class to enforce nondynamic attributes (no new attributes) for a class"""
    __setattr__ = _swig_setattr_nondynamic_class_variable(type.__setattr__)


import CGAL.CGAL_Kernel
import CGAL.CGAL_Polyhedron_3
class Polygon_mesh_slicer(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, poly):
        _CGAL_Polygon_mesh_processing.Polygon_mesh_slicer_swiginit(self, _CGAL_Polygon_mesh_processing.new_Polygon_mesh_slicer(poly))

    def slice(self, plane, out):
        return _CGAL_Polygon_mesh_processing.Polygon_mesh_slicer_slice(self, plane, out)
    __swig_destroy__ = _CGAL_Polygon_mesh_processing.delete_Polygon_mesh_slicer

# Register Polygon_mesh_slicer in _CGAL_Polygon_mesh_processing:
_CGAL_Polygon_mesh_processing.Polygon_mesh_slicer_swigregister(Polygon_mesh_slicer)
class Side_of_triangle_mesh(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, poly):
        _CGAL_Polygon_mesh_processing.Side_of_triangle_mesh_swiginit(self, _CGAL_Polygon_mesh_processing.new_Side_of_triangle_mesh(poly))

    def bounded_side(self, p):
        return _CGAL_Polygon_mesh_processing.Side_of_triangle_mesh_bounded_side(self, p)
    __swig_destroy__ = _CGAL_Polygon_mesh_processing.delete_Side_of_triangle_mesh

# Register Side_of_triangle_mesh in _CGAL_Polygon_mesh_processing:
_CGAL_Polygon_mesh_processing.Side_of_triangle_mesh_swigregister(Side_of_triangle_mesh)
class Integer_triple(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    first = property(_CGAL_Polygon_mesh_processing.Integer_triple_first_get, _CGAL_Polygon_mesh_processing.Integer_triple_first_set)
    second = property(_CGAL_Polygon_mesh_processing.Integer_triple_second_get, _CGAL_Polygon_mesh_processing.Integer_triple_second_set)
    third = property(_CGAL_Polygon_mesh_processing.Integer_triple_third_get, _CGAL_Polygon_mesh_processing.Integer_triple_third_set)

    def __init__(self, *args):
        _CGAL_Polygon_mesh_processing.Integer_triple_swiginit(self, _CGAL_Polygon_mesh_processing.new_Integer_triple(*args))

    def deepcopy(self, *args):
        return _CGAL_Polygon_mesh_processing.Integer_triple_deepcopy(self, *args)
    __swig_destroy__ = _CGAL_Polygon_mesh_processing.delete_Integer_triple

# Register Integer_triple in _CGAL_Polygon_mesh_processing:
_CGAL_Polygon_mesh_processing.Integer_triple_swigregister(Integer_triple)
class Facet_pair(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        _CGAL_Polygon_mesh_processing.Facet_pair_swiginit(self, _CGAL_Polygon_mesh_processing.new_Facet_pair(*args))
    first = property(_CGAL_Polygon_mesh_processing.Facet_pair_first_get, _CGAL_Polygon_mesh_processing.Facet_pair_first_set)
    second = property(_CGAL_Polygon_mesh_processing.Facet_pair_second_get, _CGAL_Polygon_mesh_processing.Facet_pair_second_set)
    def __len__(self):
        return 2
    def __repr__(self):
        return str((self.first, self.second))
    def __getitem__(self, index): 
        if not (index % 2):
            return self.first
        else:
            return self.second
    def __setitem__(self, index, val):
        if not (index % 2):
            self.first = val
        else:
            self.second = val
    __swig_destroy__ = _CGAL_Polygon_mesh_processing.delete_Facet_pair

# Register Facet_pair in _CGAL_Polygon_mesh_processing:
_CGAL_Polygon_mesh_processing.Facet_pair_swigregister(Facet_pair)
class Halfedge_pair(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        _CGAL_Polygon_mesh_processing.Halfedge_pair_swiginit(self, _CGAL_Polygon_mesh_processing.new_Halfedge_pair(*args))
    first = property(_CGAL_Polygon_mesh_processing.Halfedge_pair_first_get, _CGAL_Polygon_mesh_processing.Halfedge_pair_first_set)
    second = property(_CGAL_Polygon_mesh_processing.Halfedge_pair_second_get, _CGAL_Polygon_mesh_processing.Halfedge_pair_second_set)
    def __len__(self):
        return 2
    def __repr__(self):
        return str((self.first, self.second))
    def __getitem__(self, index): 
        if not (index % 2):
            return self.first
        else:
            return self.second
    def __setitem__(self, index, val):
        if not (index % 2):
            self.first = val
        else:
            self.second = val
    __swig_destroy__ = _CGAL_Polygon_mesh_processing.delete_Halfedge_pair

# Register Halfedge_pair in _CGAL_Polygon_mesh_processing:
_CGAL_Polygon_mesh_processing.Halfedge_pair_swigregister(Halfedge_pair)
class SwigPyIterator(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _CGAL_Polygon_mesh_processing.delete_SwigPyIterator

    def value(self):
        return _CGAL_Polygon_mesh_processing.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _CGAL_Polygon_mesh_processing.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _CGAL_Polygon_mesh_processing.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _CGAL_Polygon_mesh_processing.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _CGAL_Polygon_mesh_processing.SwigPyIterator_equal(self, x)

    def copy(self):
        return _CGAL_Polygon_mesh_processing.SwigPyIterator_copy(self)

    def next(self):
        return _CGAL_Polygon_mesh_processing.SwigPyIterator_next(self)

    def __next__(self):
        return _CGAL_Polygon_mesh_processing.SwigPyIterator___next__(self)

    def previous(self):
        return _CGAL_Polygon_mesh_processing.SwigPyIterator_previous(self)

    def advance(self, n):
        return _CGAL_Polygon_mesh_processing.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _CGAL_Polygon_mesh_processing.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _CGAL_Polygon_mesh_processing.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _CGAL_Polygon_mesh_processing.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _CGAL_Polygon_mesh_processing.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _CGAL_Polygon_mesh_processing.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _CGAL_Polygon_mesh_processing.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self

# Register SwigPyIterator in _CGAL_Polygon_mesh_processing:
_CGAL_Polygon_mesh_processing.SwigPyIterator_swigregister(SwigPyIterator)
class Point_3_Vector(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def iterator(self):
        return _CGAL_Polygon_mesh_processing.Point_3_Vector_iterator(self)
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        return _CGAL_Polygon_mesh_processing.Point_3_Vector___nonzero__(self)

    def __bool__(self):
        return _CGAL_Polygon_mesh_processing.Point_3_Vector___bool__(self)

    def __len__(self):
        return _CGAL_Polygon_mesh_processing.Point_3_Vector___len__(self)

    def __getslice__(self, i, j):
        return _CGAL_Polygon_mesh_processing.Point_3_Vector___getslice__(self, i, j)

    def __setslice__(self, *args):
        return _CGAL_Polygon_mesh_processing.Point_3_Vector___setslice__(self, *args)

    def __delslice__(self, i, j):
        return _CGAL_Polygon_mesh_processing.Point_3_Vector___delslice__(self, i, j)

    def __delitem__(self, *args):
        return _CGAL_Polygon_mesh_processing.Point_3_Vector___delitem__(self, *args)

    def __getitem__(self, *args):
        return _CGAL_Polygon_mesh_processing.Point_3_Vector___getitem__(self, *args)

    def __setitem__(self, *args):
        return _CGAL_Polygon_mesh_processing.Point_3_Vector___setitem__(self, *args)

    def pop(self):
        return _CGAL_Polygon_mesh_processing.Point_3_Vector_pop(self)

    def append(self, x):
        return _CGAL_Polygon_mesh_processing.Point_3_Vector_append(self, x)

    def empty(self):
        return _CGAL_Polygon_mesh_processing.Point_3_Vector_empty(self)

    def size(self):
        return _CGAL_Polygon_mesh_processing.Point_3_Vector_size(self)

    def swap(self, v):
        return _CGAL_Polygon_mesh_processing.Point_3_Vector_swap(self, v)

    def begin(self):
        return _CGAL_Polygon_mesh_processing.Point_3_Vector_begin(self)

    def end(self):
        return _CGAL_Polygon_mesh_processing.Point_3_Vector_end(self)

    def rbegin(self):
        return _CGAL_Polygon_mesh_processing.Point_3_Vector_rbegin(self)

    def rend(self):
        return _CGAL_Polygon_mesh_processing.Point_3_Vector_rend(self)

    def clear(self):
        return _CGAL_Polygon_mesh_processing.Point_3_Vector_clear(self)

    def get_allocator(self):
        return _CGAL_Polygon_mesh_processing.Point_3_Vector_get_allocator(self)

    def pop_back(self):
        return _CGAL_Polygon_mesh_processing.Point_3_Vector_pop_back(self)

    def erase(self, *args):
        return _CGAL_Polygon_mesh_processing.Point_3_Vector_erase(self, *args)

    def __init__(self, *args):
        _CGAL_Polygon_mesh_processing.Point_3_Vector_swiginit(self, _CGAL_Polygon_mesh_processing.new_Point_3_Vector(*args))

    def push_back(self, x):
        return _CGAL_Polygon_mesh_processing.Point_3_Vector_push_back(self, x)

    def front(self):
        return _CGAL_Polygon_mesh_processing.Point_3_Vector_front(self)

    def back(self):
        return _CGAL_Polygon_mesh_processing.Point_3_Vector_back(self)

    def assign(self, n, x):
        return _CGAL_Polygon_mesh_processing.Point_3_Vector_assign(self, n, x)

    def resize(self, *args):
        return _CGAL_Polygon_mesh_processing.Point_3_Vector_resize(self, *args)

    def insert(self, *args):
        return _CGAL_Polygon_mesh_processing.Point_3_Vector_insert(self, *args)

    def reserve(self, n):
        return _CGAL_Polygon_mesh_processing.Point_3_Vector_reserve(self, n)

    def capacity(self):
        return _CGAL_Polygon_mesh_processing.Point_3_Vector_capacity(self)
    __swig_destroy__ = _CGAL_Polygon_mesh_processing.delete_Point_3_Vector

# Register Point_3_Vector in _CGAL_Polygon_mesh_processing:
_CGAL_Polygon_mesh_processing.Point_3_Vector_swigregister(Point_3_Vector)
class Int_Vector(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def iterator(self):
        return _CGAL_Polygon_mesh_processing.Int_Vector_iterator(self)
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        return _CGAL_Polygon_mesh_processing.Int_Vector___nonzero__(self)

    def __bool__(self):
        return _CGAL_Polygon_mesh_processing.Int_Vector___bool__(self)

    def __len__(self):
        return _CGAL_Polygon_mesh_processing.Int_Vector___len__(self)

    def __getslice__(self, i, j):
        return _CGAL_Polygon_mesh_processing.Int_Vector___getslice__(self, i, j)

    def __setslice__(self, *args):
        return _CGAL_Polygon_mesh_processing.Int_Vector___setslice__(self, *args)

    def __delslice__(self, i, j):
        return _CGAL_Polygon_mesh_processing.Int_Vector___delslice__(self, i, j)

    def __delitem__(self, *args):
        return _CGAL_Polygon_mesh_processing.Int_Vector___delitem__(self, *args)

    def __getitem__(self, *args):
        return _CGAL_Polygon_mesh_processing.Int_Vector___getitem__(self, *args)

    def __setitem__(self, *args):
        return _CGAL_Polygon_mesh_processing.Int_Vector___setitem__(self, *args)

    def pop(self):
        return _CGAL_Polygon_mesh_processing.Int_Vector_pop(self)

    def append(self, x):
        return _CGAL_Polygon_mesh_processing.Int_Vector_append(self, x)

    def empty(self):
        return _CGAL_Polygon_mesh_processing.Int_Vector_empty(self)

    def size(self):
        return _CGAL_Polygon_mesh_processing.Int_Vector_size(self)

    def swap(self, v):
        return _CGAL_Polygon_mesh_processing.Int_Vector_swap(self, v)

    def begin(self):
        return _CGAL_Polygon_mesh_processing.Int_Vector_begin(self)

    def end(self):
        return _CGAL_Polygon_mesh_processing.Int_Vector_end(self)

    def rbegin(self):
        return _CGAL_Polygon_mesh_processing.Int_Vector_rbegin(self)

    def rend(self):
        return _CGAL_Polygon_mesh_processing.Int_Vector_rend(self)

    def clear(self):
        return _CGAL_Polygon_mesh_processing.Int_Vector_clear(self)

    def get_allocator(self):
        return _CGAL_Polygon_mesh_processing.Int_Vector_get_allocator(self)

    def pop_back(self):
        return _CGAL_Polygon_mesh_processing.Int_Vector_pop_back(self)

    def erase(self, *args):
        return _CGAL_Polygon_mesh_processing.Int_Vector_erase(self, *args)

    def __init__(self, *args):
        _CGAL_Polygon_mesh_processing.Int_Vector_swiginit(self, _CGAL_Polygon_mesh_processing.new_Int_Vector(*args))

    def push_back(self, x):
        return _CGAL_Polygon_mesh_processing.Int_Vector_push_back(self, x)

    def front(self):
        return _CGAL_Polygon_mesh_processing.Int_Vector_front(self)

    def back(self):
        return _CGAL_Polygon_mesh_processing.Int_Vector_back(self)

    def assign(self, n, x):
        return _CGAL_Polygon_mesh_processing.Int_Vector_assign(self, n, x)

    def resize(self, *args):
        return _CGAL_Polygon_mesh_processing.Int_Vector_resize(self, *args)

    def insert(self, *args):
        return _CGAL_Polygon_mesh_processing.Int_Vector_insert(self, *args)

    def reserve(self, n):
        return _CGAL_Polygon_mesh_processing.Int_Vector_reserve(self, n)

    def capacity(self):
        return _CGAL_Polygon_mesh_processing.Int_Vector_capacity(self)
    __swig_destroy__ = _CGAL_Polygon_mesh_processing.delete_Int_Vector

# Register Int_Vector in _CGAL_Polygon_mesh_processing:
_CGAL_Polygon_mesh_processing.Int_Vector_swigregister(Int_Vector)
class Polygon_Vector(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def iterator(self):
        return _CGAL_Polygon_mesh_processing.Polygon_Vector_iterator(self)
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        return _CGAL_Polygon_mesh_processing.Polygon_Vector___nonzero__(self)

    def __bool__(self):
        return _CGAL_Polygon_mesh_processing.Polygon_Vector___bool__(self)

    def __len__(self):
        return _CGAL_Polygon_mesh_processing.Polygon_Vector___len__(self)

    def __getslice__(self, i, j):
        return _CGAL_Polygon_mesh_processing.Polygon_Vector___getslice__(self, i, j)

    def __setslice__(self, *args):
        return _CGAL_Polygon_mesh_processing.Polygon_Vector___setslice__(self, *args)

    def __delslice__(self, i, j):
        return _CGAL_Polygon_mesh_processing.Polygon_Vector___delslice__(self, i, j)

    def __delitem__(self, *args):
        return _CGAL_Polygon_mesh_processing.Polygon_Vector___delitem__(self, *args)

    def __getitem__(self, *args):
        return _CGAL_Polygon_mesh_processing.Polygon_Vector___getitem__(self, *args)

    def __setitem__(self, *args):
        return _CGAL_Polygon_mesh_processing.Polygon_Vector___setitem__(self, *args)

    def pop(self):
        return _CGAL_Polygon_mesh_processing.Polygon_Vector_pop(self)

    def append(self, x):
        return _CGAL_Polygon_mesh_processing.Polygon_Vector_append(self, x)

    def empty(self):
        return _CGAL_Polygon_mesh_processing.Polygon_Vector_empty(self)

    def size(self):
        return _CGAL_Polygon_mesh_processing.Polygon_Vector_size(self)

    def swap(self, v):
        return _CGAL_Polygon_mesh_processing.Polygon_Vector_swap(self, v)

    def begin(self):
        return _CGAL_Polygon_mesh_processing.Polygon_Vector_begin(self)

    def end(self):
        return _CGAL_Polygon_mesh_processing.Polygon_Vector_end(self)

    def rbegin(self):
        return _CGAL_Polygon_mesh_processing.Polygon_Vector_rbegin(self)

    def rend(self):
        return _CGAL_Polygon_mesh_processing.Polygon_Vector_rend(self)

    def clear(self):
        return _CGAL_Polygon_mesh_processing.Polygon_Vector_clear(self)

    def get_allocator(self):
        return _CGAL_Polygon_mesh_processing.Polygon_Vector_get_allocator(self)

    def pop_back(self):
        return _CGAL_Polygon_mesh_processing.Polygon_Vector_pop_back(self)

    def erase(self, *args):
        return _CGAL_Polygon_mesh_processing.Polygon_Vector_erase(self, *args)

    def __init__(self, *args):
        _CGAL_Polygon_mesh_processing.Polygon_Vector_swiginit(self, _CGAL_Polygon_mesh_processing.new_Polygon_Vector(*args))

    def push_back(self, x):
        return _CGAL_Polygon_mesh_processing.Polygon_Vector_push_back(self, x)

    def front(self):
        return _CGAL_Polygon_mesh_processing.Polygon_Vector_front(self)

    def back(self):
        return _CGAL_Polygon_mesh_processing.Polygon_Vector_back(self)

    def assign(self, n, x):
        return _CGAL_Polygon_mesh_processing.Polygon_Vector_assign(self, n, x)

    def resize(self, *args):
        return _CGAL_Polygon_mesh_processing.Polygon_Vector_resize(self, *args)

    def insert(self, *args):
        return _CGAL_Polygon_mesh_processing.Polygon_Vector_insert(self, *args)

    def reserve(self, n):
        return _CGAL_Polygon_mesh_processing.Polygon_Vector_reserve(self, n)

    def capacity(self):
        return _CGAL_Polygon_mesh_processing.Polygon_Vector_capacity(self)
    __swig_destroy__ = _CGAL_Polygon_mesh_processing.delete_Polygon_Vector

# Register Polygon_Vector in _CGAL_Polygon_mesh_processing:
_CGAL_Polygon_mesh_processing.Polygon_Vector_swigregister(Polygon_Vector)
class Polylines(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def iterator(self):
        return _CGAL_Polygon_mesh_processing.Polylines_iterator(self)
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        return _CGAL_Polygon_mesh_processing.Polylines___nonzero__(self)

    def __bool__(self):
        return _CGAL_Polygon_mesh_processing.Polylines___bool__(self)

    def __len__(self):
        return _CGAL_Polygon_mesh_processing.Polylines___len__(self)

    def __getslice__(self, i, j):
        return _CGAL_Polygon_mesh_processing.Polylines___getslice__(self, i, j)

    def __setslice__(self, *args):
        return _CGAL_Polygon_mesh_processing.Polylines___setslice__(self, *args)

    def __delslice__(self, i, j):
        return _CGAL_Polygon_mesh_processing.Polylines___delslice__(self, i, j)

    def __delitem__(self, *args):
        return _CGAL_Polygon_mesh_processing.Polylines___delitem__(self, *args)

    def __getitem__(self, *args):
        return _CGAL_Polygon_mesh_processing.Polylines___getitem__(self, *args)

    def __setitem__(self, *args):
        return _CGAL_Polygon_mesh_processing.Polylines___setitem__(self, *args)

    def pop(self):
        return _CGAL_Polygon_mesh_processing.Polylines_pop(self)

    def append(self, x):
        return _CGAL_Polygon_mesh_processing.Polylines_append(self, x)

    def empty(self):
        return _CGAL_Polygon_mesh_processing.Polylines_empty(self)

    def size(self):
        return _CGAL_Polygon_mesh_processing.Polylines_size(self)

    def swap(self, v):
        return _CGAL_Polygon_mesh_processing.Polylines_swap(self, v)

    def begin(self):
        return _CGAL_Polygon_mesh_processing.Polylines_begin(self)

    def end(self):
        return _CGAL_Polygon_mesh_processing.Polylines_end(self)

    def rbegin(self):
        return _CGAL_Polygon_mesh_processing.Polylines_rbegin(self)

    def rend(self):
        return _CGAL_Polygon_mesh_processing.Polylines_rend(self)

    def clear(self):
        return _CGAL_Polygon_mesh_processing.Polylines_clear(self)

    def get_allocator(self):
        return _CGAL_Polygon_mesh_processing.Polylines_get_allocator(self)

    def pop_back(self):
        return _CGAL_Polygon_mesh_processing.Polylines_pop_back(self)

    def erase(self, *args):
        return _CGAL_Polygon_mesh_processing.Polylines_erase(self, *args)

    def __init__(self, *args):
        _CGAL_Polygon_mesh_processing.Polylines_swiginit(self, _CGAL_Polygon_mesh_processing.new_Polylines(*args))

    def push_back(self, x):
        return _CGAL_Polygon_mesh_processing.Polylines_push_back(self, x)

    def front(self):
        return _CGAL_Polygon_mesh_processing.Polylines_front(self)

    def back(self):
        return _CGAL_Polygon_mesh_processing.Polylines_back(self)

    def assign(self, n, x):
        return _CGAL_Polygon_mesh_processing.Polylines_assign(self, n, x)

    def resize(self, *args):
        return _CGAL_Polygon_mesh_processing.Polylines_resize(self, *args)

    def insert(self, *args):
        return _CGAL_Polygon_mesh_processing.Polylines_insert(self, *args)

    def reserve(self, n):
        return _CGAL_Polygon_mesh_processing.Polylines_reserve(self, n)

    def capacity(self):
        return _CGAL_Polygon_mesh_processing.Polylines_capacity(self)
    __swig_destroy__ = _CGAL_Polygon_mesh_processing.delete_Polylines

# Register Polylines in _CGAL_Polygon_mesh_processing:
_CGAL_Polygon_mesh_processing.Polylines_swigregister(Polylines)
CGAL_VERSION_NR = _CGAL_Polygon_mesh_processing.CGAL_VERSION_NR
CGAL_SVN_REVISION = _CGAL_Polygon_mesh_processing.CGAL_SVN_REVISION
CGAL_RELEASE_DATE = _CGAL_Polygon_mesh_processing.CGAL_RELEASE_DATE

def fair(*args):
    return _CGAL_Polygon_mesh_processing.fair(*args)

def refine(*args):
    return _CGAL_Polygon_mesh_processing.refine(*args)

def triangulate_face(face, P):
    return _CGAL_Polygon_mesh_processing.triangulate_face(face, P)

def triangulate_faces(*args):
    return _CGAL_Polygon_mesh_processing.triangulate_faces(*args)

def isotropic_remeshing(*args):
    return _CGAL_Polygon_mesh_processing.isotropic_remeshing(*args)

def split_long_edges(halfedge_range, max_length, P):
    return _CGAL_Polygon_mesh_processing.split_long_edges(halfedge_range, max_length, P)

def triangulate_hole(P, h, output):
    return _CGAL_Polygon_mesh_processing.triangulate_hole(P, h, output)

def triangulate_and_refine_hole(*args):
    return _CGAL_Polygon_mesh_processing.triangulate_and_refine_hole(*args)

def triangulate_refine_and_fair_hole(*args):
    return _CGAL_Polygon_mesh_processing.triangulate_refine_and_fair_hole(*args)

def triangulate_hole_polyline(*args):
    return _CGAL_Polygon_mesh_processing.triangulate_hole_polyline(*args)

def does_self_intersect(P):
    return _CGAL_Polygon_mesh_processing.does_self_intersect(P)

def self_intersections(P, out):
    return _CGAL_Polygon_mesh_processing.self_intersections(P, out)

def do_intersect(*args):
    return _CGAL_Polygon_mesh_processing.do_intersect(*args)

def is_outward_oriented(P):
    return _CGAL_Polygon_mesh_processing.is_outward_oriented(P)

def reverse_face_orientations(*args):
    return _CGAL_Polygon_mesh_processing.reverse_face_orientations(*args)

def orient_polygon_soup(points, polygons):
    return _CGAL_Polygon_mesh_processing.orient_polygon_soup(points, polygons)

def stitch_borders(*args):
    return _CGAL_Polygon_mesh_processing.stitch_borders(*args)

def polygon_soup_to_polygon_mesh(points, polygons, P):
    return _CGAL_Polygon_mesh_processing.polygon_soup_to_polygon_mesh(points, polygons, P)

def remove_isolated_vertices(P):
    return _CGAL_Polygon_mesh_processing.remove_isolated_vertices(P)

def compute_face_normal(*args):
    return _CGAL_Polygon_mesh_processing.compute_face_normal(*args)

def compute_face_normals(P, out):
    return _CGAL_Polygon_mesh_processing.compute_face_normals(P, out)

def compute_vertex_normal(*args):
    return _CGAL_Polygon_mesh_processing.compute_vertex_normal(*args)

def compute_vertex_normals(P, out):
    return _CGAL_Polygon_mesh_processing.compute_vertex_normals(P, out)

def connected_component(seed_face, P, out):
    return _CGAL_Polygon_mesh_processing.connected_component(seed_face, P, out)

def connected_components(P):
    return _CGAL_Polygon_mesh_processing.connected_components(P)

def keep_large_connected_components(P, threshold_components_to_keep):
    return _CGAL_Polygon_mesh_processing.keep_large_connected_components(P, threshold_components_to_keep)

def keep_largest_connected_components(P, nb_components_to_keep):
    return _CGAL_Polygon_mesh_processing.keep_largest_connected_components(P, nb_components_to_keep)

def keep_connected_components(*args):
    return _CGAL_Polygon_mesh_processing.keep_connected_components(*args)

def remove_connected_components(*args):
    return _CGAL_Polygon_mesh_processing.remove_connected_components(*args)

def face_area(face, P):
    return _CGAL_Polygon_mesh_processing.face_area(face, P)

def area(*args):
    return _CGAL_Polygon_mesh_processing.area(*args)

def volume(P):
    return _CGAL_Polygon_mesh_processing.volume(P)

def edge_length(hedge, P):
    return _CGAL_Polygon_mesh_processing.edge_length(hedge, P)

def face_border_length(hedge, P):
    return _CGAL_Polygon_mesh_processing.face_border_length(hedge, P)

def bbox(P):
    return _CGAL_Polygon_mesh_processing.bbox(P)

def corefine(A, B):
    return _CGAL_Polygon_mesh_processing.corefine(A, B)

def corefine_and_compute_union(A, B, out):
    return _CGAL_Polygon_mesh_processing.corefine_and_compute_union(A, B, out)

def corefine_and_compute_intersection(A, B, out):
    return _CGAL_Polygon_mesh_processing.corefine_and_compute_intersection(A, B, out)

def corefine_and_compute_difference(A, B, out):
    return _CGAL_Polygon_mesh_processing.corefine_and_compute_difference(A, B, out)

def clip(*args):
    return _CGAL_Polygon_mesh_processing.clip(*args)

def border_halfedges(facet_range, P, out):
    return _CGAL_Polygon_mesh_processing.border_halfedges(facet_range, P, out)

