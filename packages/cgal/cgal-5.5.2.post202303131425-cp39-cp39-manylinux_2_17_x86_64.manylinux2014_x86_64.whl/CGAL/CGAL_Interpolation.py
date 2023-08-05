# This file was automatically generated by SWIG (https://www.swig.org).
# Version 4.1.0
#
# Do not make changes to this file unless you know what you are doing - modify
# the SWIG interface file instead.

"""SWIG wrapper for the CGAL 2D and Surface Function Interpolation package provided under the GPL-3.0+ license"""

from sys import version_info as _swig_python_version_info
# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _CGAL_Interpolation
else:
    import _CGAL_Interpolation

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


import CGAL.CGAL_Triangulation_2
import CGAL.CGAL_Kernel
import CGAL.CGAL_Triangulation_3
class Double_and_bool(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        _CGAL_Interpolation.Double_and_bool_swiginit(self, _CGAL_Interpolation.new_Double_and_bool(*args))
    first = property(_CGAL_Interpolation.Double_and_bool_first_get, _CGAL_Interpolation.Double_and_bool_first_set)
    second = property(_CGAL_Interpolation.Double_and_bool_second_get, _CGAL_Interpolation.Double_and_bool_second_set)
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
    __swig_destroy__ = _CGAL_Interpolation.delete_Double_and_bool

# Register Double_and_bool in _CGAL_Interpolation:
_CGAL_Interpolation.Double_and_bool_swigregister(Double_and_bool)
class Double_bool_bool(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    first = property(_CGAL_Interpolation.Double_bool_bool_first_get, _CGAL_Interpolation.Double_bool_bool_first_set)
    second = property(_CGAL_Interpolation.Double_bool_bool_second_get, _CGAL_Interpolation.Double_bool_bool_second_set)
    third = property(_CGAL_Interpolation.Double_bool_bool_third_get, _CGAL_Interpolation.Double_bool_bool_third_set)

    def __init__(self, *args):
        _CGAL_Interpolation.Double_bool_bool_swiginit(self, _CGAL_Interpolation.new_Double_bool_bool(*args))

    def deepcopy(self, *args):
        return _CGAL_Interpolation.Double_bool_bool_deepcopy(self, *args)
    __swig_destroy__ = _CGAL_Interpolation.delete_Double_bool_bool

# Register Double_bool_bool in _CGAL_Interpolation:
_CGAL_Interpolation.Double_bool_bool_swigregister(Double_bool_bool)
class Point_2_and_double(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        _CGAL_Interpolation.Point_2_and_double_swiginit(self, _CGAL_Interpolation.new_Point_2_and_double(*args))
    first = property(_CGAL_Interpolation.Point_2_and_double_first_get, _CGAL_Interpolation.Point_2_and_double_first_set)
    second = property(_CGAL_Interpolation.Point_2_and_double_second_get, _CGAL_Interpolation.Point_2_and_double_second_set)
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
    __swig_destroy__ = _CGAL_Interpolation.delete_Point_2_and_double

# Register Point_2_and_double in _CGAL_Interpolation:
_CGAL_Interpolation.Point_2_and_double_swigregister(Point_2_and_double)
class Weighted_point_2_and_double(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        _CGAL_Interpolation.Weighted_point_2_and_double_swiginit(self, _CGAL_Interpolation.new_Weighted_point_2_and_double(*args))
    first = property(_CGAL_Interpolation.Weighted_point_2_and_double_first_get, _CGAL_Interpolation.Weighted_point_2_and_double_first_set)
    second = property(_CGAL_Interpolation.Weighted_point_2_and_double_second_get, _CGAL_Interpolation.Weighted_point_2_and_double_second_set)
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
    __swig_destroy__ = _CGAL_Interpolation.delete_Weighted_point_2_and_double

# Register Weighted_point_2_and_double in _CGAL_Interpolation:
_CGAL_Interpolation.Weighted_point_2_and_double_swigregister(Weighted_point_2_and_double)
class Point_3_and_double(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        _CGAL_Interpolation.Point_3_and_double_swiginit(self, _CGAL_Interpolation.new_Point_3_and_double(*args))
    first = property(_CGAL_Interpolation.Point_3_and_double_first_get, _CGAL_Interpolation.Point_3_and_double_first_set)
    second = property(_CGAL_Interpolation.Point_3_and_double_second_get, _CGAL_Interpolation.Point_3_and_double_second_set)
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
    __swig_destroy__ = _CGAL_Interpolation.delete_Point_3_and_double

# Register Point_3_and_double in _CGAL_Interpolation:
_CGAL_Interpolation.Point_3_and_double_swigregister(Point_3_and_double)
class Data_access_double_2(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self):
        _CGAL_Interpolation.Data_access_double_2_swiginit(self, _CGAL_Interpolation.new_Data_access_double_2())

    def set(self, p, value):
        return _CGAL_Interpolation.Data_access_double_2_set(self, p, value)

    def get(self, p):
        return _CGAL_Interpolation.Data_access_double_2_get(self, p)
    __swig_destroy__ = _CGAL_Interpolation.delete_Data_access_double_2

# Register Data_access_double_2 in _CGAL_Interpolation:
_CGAL_Interpolation.Data_access_double_2_swigregister(Data_access_double_2)
class Data_access_vector_2(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self):
        _CGAL_Interpolation.Data_access_vector_2_swiginit(self, _CGAL_Interpolation.new_Data_access_vector_2())

    def set(self, p, value):
        return _CGAL_Interpolation.Data_access_vector_2_set(self, p, value)

    def get(self, p):
        return _CGAL_Interpolation.Data_access_vector_2_get(self, p)
    __swig_destroy__ = _CGAL_Interpolation.delete_Data_access_vector_2

# Register Data_access_vector_2 in _CGAL_Interpolation:
_CGAL_Interpolation.Data_access_vector_2_swigregister(Data_access_vector_2)

def natural_neighbor_coordinates_2(*args):
    return _CGAL_Interpolation.natural_neighbor_coordinates_2(*args)

def regular_neighbor_coordinates_2(*args):
    return _CGAL_Interpolation.regular_neighbor_coordinates_2(*args)

def surface_neighbors_certified_3(*args):
    return _CGAL_Interpolation.surface_neighbors_certified_3(*args)

def surface_neighbors_3(*args):
    return _CGAL_Interpolation.surface_neighbors_3(*args)

def surface_neighbor_coordinates_certified_3(*args):
    return _CGAL_Interpolation.surface_neighbor_coordinates_certified_3(*args)

def surface_neighbor_coordinates_3(*args):
    return _CGAL_Interpolation.surface_neighbor_coordinates_3(*args)

def linear_interpolation(range, norm, function_values):
    return _CGAL_Interpolation.linear_interpolation(range, norm, function_values)

def quadratic_interpolation(range, norm, p, function_values, gradients):
    return _CGAL_Interpolation.quadratic_interpolation(range, norm, p, function_values, gradients)

def sibson_c1_interpolation(range, norm, p, function_values, gradients):
    return _CGAL_Interpolation.sibson_c1_interpolation(range, norm, p, function_values, gradients)

def sibson_c1_interpolation_square(range, norm, p, function_values, gradients):
    return _CGAL_Interpolation.sibson_c1_interpolation_square(range, norm, p, function_values, gradients)

def farin_c1_interpolation(range, norm, p, function_values, gradients):
    return _CGAL_Interpolation.farin_c1_interpolation(range, norm, p, function_values, gradients)

def sibson_gradient_fitting(range, norm, p, function_values):
    return _CGAL_Interpolation.sibson_gradient_fitting(range, norm, p, function_values)

def sibson_gradient_fitting_nn_2(dt, gradients, function_values):
    return _CGAL_Interpolation.sibson_gradient_fitting_nn_2(dt, gradients, function_values)

