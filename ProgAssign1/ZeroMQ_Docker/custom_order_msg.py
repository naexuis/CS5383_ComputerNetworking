from enum import IntEnum
from typing import List
from dataclasses import dataclass

class VegType (IntEnum):
    TOMATO = 0, 
    CUCUMBER = 1, 
    POTATO = 2,
    CARROT = 3,
    SPINACH = 4,
    LETTUCE = 5,
    BROCCOLI = 6,
    CAULIFLOWER = 7,
    BOK_CHOY = 8,
    ONION = 9,
    GARLIC = 10,
    GREEN_BEANS = 11,
    PEAS = 12

class CanType (IntEnum):
    COCA_COLA = 0, 
    PEPSI = 1, 
    DIET_COKE = 2,
    DR_PEPPER = 3,
    MOUNTAIN_DEW = 4,
    SPRITE = 5,
    DEIT_PEPSI = 6,
    COKE_ZERO = 7,
    DIET_DR_PEPPER = 8,
    FANTA = 9,
    SIERRA_MIST = 10,
    SUNKIST = 11,
    TAB = 12

class BottleType (IntEnum):
    COCA_COLA = 0, 
    PEPSI = 1, 
    DIET_COKE = 2,
    DR_PEPPER = 3,
    MOUNTAIN_DEW = 4,
    SPRITE = 5,
    DEIT_PEPSI = 6,
    COKE_ZERO = 7,
    DIET_DR_PEPPER = 8,

class MilkType (IntEnum):
    ONEPERCENT = 0, 
    TWOPERCENT = 1, 
    FATFREE = 2,
    WHOLE = 3,
    ALMOND = 4,
    CASHEW = 5,
    OAT = 6

class BreadType (IntEnum):
    AREPA = 0, 
    BAGUETTE = 1, 
    BAGEL = 2,
    BRIOCHE = 3,
    CIABATTA = 4,
    CHALLAH = 5,
    ENGLISH_MUFFIN = 6,
    FOCACCIA = 7,
    HOKKAIDO = 8,
    IRISH_SODA_BREAD = 9,
    MULTIGRAIN = 10,
    NAAN = 11,
    PARATHA = 12,
    PITA = 13,
    RYE_BREAD = 14,
    SOURDOUGH = 15,
    WHITE_BREAD = 16,
    WHOLE_WHEAT_BREAD = 17,

class MeatType (IntEnum):
    PORK = 0, 
    CHICKEN = 1, 
    BEEF = 2,
    LAMB = 3,
    GOAT = 4,
    TURKEY = 5,
    DUCK = 6,
    BUFFALO = 7,
    GOOSE = 8,
    RABBIT = 9,

@dataclass
class Veg:
  """ Our message in native representation"""
  vtype: VegType
  vquantity: float

VegList = List[Veg]


@dataclass
class CanDrink:
  """ Our message in native representation"""
  ctype: CanType
  cquantity: float

CanDrinkList = List[CanDrink]


@dataclass
class BottleDrink:
  """ Our message in native representation"""
  btype: BottleType
  bquantity: float

BottleDrinkList = List[BottleDrink]


@dataclass
class Milk:
  """ Our message in native representation"""
  mtype: MilkType
  quantity: float

MilkList = List[Milk]


@dataclass
class Bread:
  """ Our message in native representation"""
  ytype: BreadType
  yquantity: float

BreadList = List[Bread]

@dataclass
class Meat:
  """ Our message in native representation"""
  xtype: MeatType
  xquantity: float

MeatList = List[Meat]


@dataclass
class CustomOrderMessage:
  """ Our message in native representation"""
  seq_num: int  # a sequence number
  ts: float    # timestamp
  vl: VegList # vector of veg
  cl: CanDrinkList # vector of candrinks
  bl: BottleDrinkList # vector of bottledrinks
  ml: MilkList # vector of milk
  yl: BreadList # vector of bread
  xl: MeatList # vector of meat

  def __init__ (self):
      self.vl = []
      self.cl = []
      self.bl = []
      self.ml = []
      self.yl = []
      self.xl = []

  
  def dump (self):
    print ("Dumping contents of Custom Order Message")
    print ("  Seq Num: {}".format (self.seq_num))
    print ("  Timestamp: {}".format (self.ts))
    print ("  Veg: {}".format (self.vl))
    print ("  Can Drinks: {}".format (self.cl))
    print ("  Bottle Drinks: {}".format (self.bl))
    print ("  Milk: {}".format (self.ml))
    print ("  Bread: {}".format (self.yl))
    print ("  Meat: {}".format (self.xl))