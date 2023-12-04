import replyMessage_pb2 as _replyMessage_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MilkTypes(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    MILK_TYPE_NOT_IN_USE: _ClassVar[MilkTypes]
    MILK_ONE_PERCENT: _ClassVar[MilkTypes]
    MILK_TWO_PERCENT: _ClassVar[MilkTypes]
    MILK_FAT_FREE: _ClassVar[MilkTypes]
    MILK_WHOLE: _ClassVar[MilkTypes]
    MILK_OAT: _ClassVar[MilkTypes]
    MILK_ALMOND: _ClassVar[MilkTypes]
    MILK_CASHEW: _ClassVar[MilkTypes]

class BreadTypes(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    BREAD_TYPE_NOT_IN_USE: _ClassVar[BreadTypes]
    BREAD_WHOLE_WHEAT: _ClassVar[BreadTypes]
    BREAD_RYE: _ClassVar[BreadTypes]
    BREAD_PUMPERNICKEL: _ClassVar[BreadTypes]

class MeatTypes(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    MEAT_TYPE_NOT_IN_USE: _ClassVar[MeatTypes]
    MEAT_PORK: _ClassVar[MeatTypes]
    MEAT_MUTTON: _ClassVar[MeatTypes]
    MEAT_CHICKEN: _ClassVar[MeatTypes]
    MEAT_STEAK: _ClassVar[MeatTypes]
MILK_TYPE_NOT_IN_USE: MilkTypes
MILK_ONE_PERCENT: MilkTypes
MILK_TWO_PERCENT: MilkTypes
MILK_FAT_FREE: MilkTypes
MILK_WHOLE: MilkTypes
MILK_OAT: MilkTypes
MILK_ALMOND: MilkTypes
MILK_CASHEW: MilkTypes
BREAD_TYPE_NOT_IN_USE: BreadTypes
BREAD_WHOLE_WHEAT: BreadTypes
BREAD_RYE: BreadTypes
BREAD_PUMPERNICKEL: BreadTypes
MEAT_TYPE_NOT_IN_USE: MeatTypes
MEAT_PORK: MeatTypes
MEAT_MUTTON: MeatTypes
MEAT_CHICKEN: MeatTypes
MEAT_STEAK: MeatTypes

class Veggies(_message.Message):
    __slots__ = ["tomato", "cucumber", "carrots", "broccoli", "onions", "potatoes"]
    TOMATO_FIELD_NUMBER: _ClassVar[int]
    CUCUMBER_FIELD_NUMBER: _ClassVar[int]
    CARROTS_FIELD_NUMBER: _ClassVar[int]
    BROCCOLI_FIELD_NUMBER: _ClassVar[int]
    ONIONS_FIELD_NUMBER: _ClassVar[int]
    POTATOES_FIELD_NUMBER: _ClassVar[int]
    tomato: float
    cucumber: float
    carrots: float
    broccoli: float
    onions: float
    potatoes: float
    def __init__(self, tomato: _Optional[float] = ..., cucumber: _Optional[float] = ..., carrots: _Optional[float] = ..., broccoli: _Optional[float] = ..., onions: _Optional[float] = ..., potatoes: _Optional[float] = ...) -> None: ...

class Cans(_message.Message):
    __slots__ = ["coke", "pepsi", "beer"]
    COKE_FIELD_NUMBER: _ClassVar[int]
    PEPSI_FIELD_NUMBER: _ClassVar[int]
    BEER_FIELD_NUMBER: _ClassVar[int]
    coke: float
    pepsi: float
    beer: float
    def __init__(self, coke: _Optional[float] = ..., pepsi: _Optional[float] = ..., beer: _Optional[float] = ...) -> None: ...

class Bottles(_message.Message):
    __slots__ = ["sprite", "wine", "gingerale"]
    SPRITE_FIELD_NUMBER: _ClassVar[int]
    WINE_FIELD_NUMBER: _ClassVar[int]
    GINGERALE_FIELD_NUMBER: _ClassVar[int]
    sprite: float
    wine: float
    gingerale: float
    def __init__(self, sprite: _Optional[float] = ..., wine: _Optional[float] = ..., gingerale: _Optional[float] = ...) -> None: ...

class Drinks(_message.Message):
    __slots__ = ["cans", "bottles"]
    CANS_FIELD_NUMBER: _ClassVar[int]
    BOTTLES_FIELD_NUMBER: _ClassVar[int]
    cans: Cans
    bottles: Bottles
    def __init__(self, cans: _Optional[_Union[Cans, _Mapping]] = ..., bottles: _Optional[_Union[Bottles, _Mapping]] = ...) -> None: ...

class Milk(_message.Message):
    __slots__ = ["type", "quantity"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    type: MilkTypes
    quantity: float
    def __init__(self, type: _Optional[_Union[MilkTypes, str]] = ..., quantity: _Optional[float] = ...) -> None: ...

class Bread(_message.Message):
    __slots__ = ["type", "quantity"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    type: BreadTypes
    quantity: float
    def __init__(self, type: _Optional[_Union[BreadTypes, str]] = ..., quantity: _Optional[float] = ...) -> None: ...

class Meat(_message.Message):
    __slots__ = ["type", "quantity"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    type: MeatTypes
    quantity: float
    def __init__(self, type: _Optional[_Union[MeatTypes, str]] = ..., quantity: _Optional[float] = ...) -> None: ...

class Order(_message.Message):
    __slots__ = ["seq_no", "ts", "veggies", "drinks", "milk", "bread", "meat"]
    SEQ_NO_FIELD_NUMBER: _ClassVar[int]
    TS_FIELD_NUMBER: _ClassVar[int]
    VEGGIES_FIELD_NUMBER: _ClassVar[int]
    DRINKS_FIELD_NUMBER: _ClassVar[int]
    MILK_FIELD_NUMBER: _ClassVar[int]
    BREAD_FIELD_NUMBER: _ClassVar[int]
    MEAT_FIELD_NUMBER: _ClassVar[int]
    seq_no: int
    ts: float
    veggies: Veggies
    drinks: Drinks
    milk: _containers.RepeatedCompositeFieldContainer[Milk]
    bread: _containers.RepeatedCompositeFieldContainer[Bread]
    meat: _containers.RepeatedCompositeFieldContainer[Meat]
    def __init__(self, seq_no: _Optional[int] = ..., ts: _Optional[float] = ..., veggies: _Optional[_Union[Veggies, _Mapping]] = ..., drinks: _Optional[_Union[Drinks, _Mapping]] = ..., milk: _Optional[_Iterable[_Union[Milk, _Mapping]]] = ..., bread: _Optional[_Iterable[_Union[Bread, _Mapping]]] = ..., meat: _Optional[_Iterable[_Union[Meat, _Mapping]]] = ...) -> None: ...
