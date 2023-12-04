# automatically generated by the FlatBuffers compiler, do not modify

# namespace: CustomAppProto

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class Bread(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Bread()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsBread(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # Bread
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Bread
    def Ytype(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int8Flags, o + self._tab.Pos)
        return 0

    # Bread
    def Yquantity(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

def BreadStart(builder):
    builder.StartObject(2)

def Start(builder):
    BreadStart(builder)

def BreadAddYtype(builder, ytype):
    builder.PrependInt8Slot(0, ytype, 0)

def AddYtype(builder, ytype):
    BreadAddYtype(builder, ytype)

def BreadAddYquantity(builder, yquantity):
    builder.PrependFloat32Slot(1, yquantity, 0.0)

def AddYquantity(builder, yquantity):
    BreadAddYquantity(builder, yquantity)

def BreadEnd(builder):
    return builder.EndObject()

def End(builder):
    return BreadEnd(builder)