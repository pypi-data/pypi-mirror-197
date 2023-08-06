"""
Tensor binary operations mixin.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .tensor import Tensor  # just for type hints; otherwise use _t.Tensor

import returnn.frontend_api as _frontend_api
from ._tensor_mixin_base import _TensorMixinBase


class _TensorBinOpsMixin(_TensorMixinBase):

    # _TensorMixin.__eq__ is disabled as per the following error in some TF tests:
    # AssertionError: unhashable type: 'Tensor'.
    # See CI https://github.com/rwth-i6/returnn/actions/runs/4406240591
    """
    def __eq__(self: Tensor, other: Union[_frontend_api.RawTensorTypes, Tensor]) -> Tensor:
        return self.raw_frontend.compare(self, "==", other)
    """

    def __ne__(self: Tensor, other: Union[_frontend_api.RawTensorTypes, Tensor]) -> Tensor:
        return self.raw_frontend.compare(self, "!=", other)

    def __lt__(self: Tensor, other: Union[_frontend_api.RawTensorTypes, Tensor]) -> Tensor:
        return self.raw_frontend.compare(self, "<", other)

    def __le__(self: Tensor, other: Union[_frontend_api.RawTensorTypes, Tensor]) -> Tensor:
        return self.raw_frontend.compare(self, "<=", other)

    def __gt__(self: Tensor, other: Union[_frontend_api.RawTensorTypes, Tensor]) -> Tensor:
        return self.raw_frontend.compare(self, ">", other)

    def __ge__(self: Tensor, other: Union[_frontend_api.RawTensorTypes, Tensor]) -> Tensor:
        return self.raw_frontend.compare(self, ">=", other)

    def __add__(self: Tensor, other: Union[_frontend_api.RawTensorTypes, Tensor]) -> Tensor:
        return self.raw_frontend.combine(self, "+", other)

    def __radd__(self: Tensor, other: Union[_frontend_api.RawTensorTypes, Tensor]) -> Tensor:
        return self.raw_frontend.combine(other, "+", self)

    def __sub__(self: Tensor, other: Union[_frontend_api.RawTensorTypes, Tensor]) -> Tensor:
        return self.raw_frontend.combine(self, "-", other)

    def __rsub__(self: Tensor, other: Union[_frontend_api.RawTensorTypes, Tensor]) -> Tensor:
        return self.raw_frontend.combine(other, "-", self)

    def __mul__(self: Tensor, other: Union[_frontend_api.RawTensorTypes, Tensor]) -> Tensor:
        return self.raw_frontend.combine(self, "*", other)

    def __rmul__(self: Tensor, other: Union[_frontend_api.RawTensorTypes, Tensor]) -> Tensor:
        return self.raw_frontend.combine(other, "*", self)

    def __truediv__(self: Tensor, other: Union[_frontend_api.RawTensorTypes, Tensor]) -> Tensor:
        return self.raw_frontend.combine(self, "/", other)

    def __rtruediv__(self: Tensor, other: Union[_frontend_api.RawTensorTypes, Tensor]) -> Tensor:
        return self.raw_frontend.combine(other, "/", self)

    def __floordiv__(self: Tensor, other: Union[_frontend_api.RawTensorTypes, Tensor]) -> Tensor:
        return self.raw_frontend.combine(self, "//", other)

    def __rfloordiv__(self: Tensor, other: Union[_frontend_api.RawTensorTypes, Tensor]) -> Tensor:
        return self.raw_frontend.combine(other, "//", self)

    def __mod__(self: Tensor, other: Union[_frontend_api.RawTensorTypes, Tensor]) -> Tensor:
        return self.raw_frontend.combine(self, "%", other)

    def __rmod__(self: Tensor, other: Union[_frontend_api.RawTensorTypes, Tensor]) -> Tensor:
        return self.raw_frontend.combine(other, "%", self)

    def __pow__(self: Tensor, other: Union[_frontend_api.RawTensorTypes, Tensor]) -> Tensor:
        return self.raw_frontend.combine(self, "**", other)

    def __rpow__(self: Tensor, other: Union[_frontend_api.RawTensorTypes, Tensor]) -> Tensor:
        return self.raw_frontend.combine(other, "**", self)

    def __and__(self: Tensor, other: Union[_frontend_api.RawTensorTypes, Tensor]) -> Tensor:
        return self.raw_frontend.combine(self, "logical_and", other)

    def __rand__(self: Tensor, other: Union[_frontend_api.RawTensorTypes, Tensor]) -> Tensor:
        return self.raw_frontend.combine(other, "logical_and", self)

    def __or__(self: Tensor, other: Union[_frontend_api.RawTensorTypes, Tensor]) -> Tensor:
        return self.raw_frontend.combine(self, "logical_or", other)

    def __ror__(self: Tensor, other: Union[_frontend_api.RawTensorTypes, Tensor]) -> Tensor:
        return self.raw_frontend.combine(other, "logical_or", self)
