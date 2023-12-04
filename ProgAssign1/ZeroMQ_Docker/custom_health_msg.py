from typing import List
from dataclasses import dataclass

@dataclass
class CustomHealthMessage:
  """ Our message in native representation"""
  seq_num: int  # a sequence number
  ts: float    # timestamp
  name: str    # some name
  dispenser: int
  icemaker: int
  lightbulb: int
  fridge_temp: int
  freezer_temp: int
  sensor_status: int

  def __init__ (self):
    pass
  
  def dump (self):
    print ("Dumping contents of Custom Message")
    print ("  Seq Num: {}".format (self.seq_num))
    print ("  Timestamp: {}".format (self.ts))
    print ("  Name: {}".format (self.name))
    print ("  Dispenser: {}".format (self.dispenser))
    print ("  Icemaker: {}".format (self.icemaker))
    print ("  Lightbulb: {}".format (self.lightbulb))
    print ("  Fridge_temp: {}".format (self.fridge_temp))
    print ("  Freezer_temp: {}".format (self.freezer_temp))
    print ("  Sensor_status: {}".format (self.sensor_status))

