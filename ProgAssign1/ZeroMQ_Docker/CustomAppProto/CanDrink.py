# automatically generated by the FlatBuffers compiler, do not modify

# namespace: CustomAppProto

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class CanDrink(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = CanDrink()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsCanDrink(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # CanDrink
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # CanDrink
    def Ctype(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int8Flags, o + self._tab.Pos)
        return 0

    # CanDrink
    def Cquantity(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

def CanDrinkStart(builder):
    builder.StartObject(2)

def Start(builder):
    CanDrinkStart(builder)

def CanDrinkAddCtype(builder, ctype):
    builder.PrependInt8Slot(0, ctype, 0)

def AddCtype(builder, ctype):
    CanDrinkAddCtype(builder, ctype)

def CanDrinkAddCquantity(builder, cquantity):
    builder.PrependFloat32Slot(1, cquantity, 0.0)

def AddCquantity(builder, cquantity):
    CanDrinkAddCquantity(builder, cquantity)

def CanDrinkEnd(builder):
    return builder.EndObject()

def End(builder):
    return CanDrinkEnd(builder)
