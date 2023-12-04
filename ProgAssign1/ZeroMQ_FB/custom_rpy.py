from typing import List
from dataclasses import dataclass

@dataclass
class CustomReply:
  """ Our message in native representation"""
  seq_num: int  # a sequence number
  ts: float    # timestamp
  reply_request: int
  reply_status: int


  def __init__ (self):
    pass
  
  def dump (self):
    print ("Dumping contents of Custom Reply")
    print ("  Seq Num: {}".format (self.seq_num))
    print ("  Timestamp: {}".format (self.ts))
    print ("  Reply_request: {}".format (self.reply_request))
    print ("  reply_status: {}".format (self.reply_status))