"""The origional design of CodedLocation caused deserialization by pydantic BaseModel to not initialize
correctly and be missing the _code attribute.

https://github.com/GNS-Science/nzshm-common-py/issues/76

"""

from dataclasses import dataclass

import pytest
from pydantic import BaseModel

from nzshm_common import CodedLocation


def test_deserialize_pydantic_bug():
    """This test reproduces the origional fault for documentation purposes."""

    @dataclass(init=False)
    class DummyCodedLocation:
        a: int

        def __init__(self, a):
            self.a = 1
            self.b = str(self.a)

    class DummyMyModel(BaseModel):
        location: DummyCodedLocation

    loc = DummyCodedLocation(a=1)
    model = DummyMyModel(location=loc)
    data = model.model_dump()
    model_deser = DummyMyModel(**data)

    with pytest.raises(AttributeError):
        model_deser.b


def test_deserialize_pydantic_76():
    """Test that we can deserialize a BaseClass with a CodedLocation member."""

    class MyModel(BaseModel):
        location: CodedLocation

    loc = CodedLocation(-45.27, 175.2, 0.1)
    model = MyModel(location=loc)
    data = model.model_dump()

    model_deser = MyModel(**data)
    assert model.location == model_deser.location
    assert model_deser.location._code
    assert model_deser.location.grid_res
    assert model_deser.location.display_places
