from __future__ import annotations

import abc
import inspect
import uuid
from typing import ClassVar, Optional, Tuple

import torch

from . import _rust as rc


class GeneralFunctionSpecBase(metaclass=abc.ABCMeta):
    __hash_bytes: ClassVar[bytes]
    """
    Inherit from this base class in order to implement an arbitrary new GeneralFunctionSpec.

    See docs for `get_shape_info`, GeneralFunctionShapeInfo, and `function`.
    """

    def __init_subclass__(cls):
        b = bytearray()
        for _, x in inspect.getmembers(cls, inspect.ismethod):
            if hasattr(x, "__code__"):
                b.extend(x.__code__.co_code)
                b.extend(uuid.UUID("6739c5c8-a9ab-421d-a06c-38f356bed339").bytes)
        b.extend(uuid.UUID("c5b1184c-76ae-430a-87cc-d6afc90569ce").bytes)
        b.extend((cls.__module__ + "." + cls.__name__).encode())
        cls.__hash_bytes = bytes(b)

    @classmethod
    def new(cls, *xs: rc.Circuit, name: Optional[str] = None):
        """This should be overridden if your generalfunction has non-Circuit arguments"""
        return rc.GeneralFunction(*xs, spec=cls(), name=name)

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def path(self) -> Optional[str]:
        """The path of this spec relative to RRFS_DIR if this is stored in rrfs.
        Should be of the form /dir/sub_dir/.../file.py:MyCustomSpec"""
        return None

    def compute_hash_bytes(self) -> bytes:
        """What parts of self should be used for hashing & equality?

        should be implemented if you store data on `self`"""
        return self.__hash_bytes

    @abc.abstractmethod
    def function(self, *tensors: torch.Tensor) -> torch.Tensor:
        """run the actual function on tensors - these tensors shapes correspond to the shapes in ``get_shape_info``"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_shape_info(self, *shapes: rc.Shape) -> rc.GeneralFunctionShapeInfo:
        """This should error (exception) if the shapes are invalid and otherwise return GeneralFunctionShapeInfo"""
        raise NotImplementedError

    def get_device_dtype_override(self, *device_dtypes: rc.TorchDeviceDtypeOp) -> Optional[rc.TorchDeviceDtypeOp]:
        """Use this to check the validity of input dtypes/devices and set output device/dtype. If this returns None, the output inherits device/dtype from children.
        This can error to signal that inputs have invalid dtypes/devices"""
        return None
