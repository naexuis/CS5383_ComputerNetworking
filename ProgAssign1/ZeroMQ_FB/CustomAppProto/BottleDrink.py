# automatically generated by the FlatBuffers compiler, do not modify

# namespace: CustomAppProto

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class BottleDrink(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = BottleDrink()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsBottleDrink(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # BottleDrink
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # BottleDrink
    def Btype(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int8Flags, o + self._tab.Pos)
        return 0

    # BottleDrink
    def Bquantity(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

def BottleDrinkStart(builder):
    builder.StartObject(2)

def Start(builder):
    BottleDrinkStart(builder)

def BottleDrinkAddBtype(builder, btype):
    builder.PrependInt8Slot(0, btype, 0)

def AddBtype(builder, btype):
    BottleDrinkAddBtype(builder, btype)

def BottleDrinkAddBquantity(builder, bquantity):
    builder.PrependFloat32Slot(1, bquantity, 0.0)

def AddBquantity(builder, bquantity):
    BottleDrinkAddBquantity(builder, bquantity)

def BottleDrinkEnd(builder):
    return builder.EndObject()

def End(builder):
    return BottleDrinkEnd(builder)
