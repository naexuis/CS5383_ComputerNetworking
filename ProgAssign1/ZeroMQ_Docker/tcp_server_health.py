import os
import sys
import time

import argparse

import random

import zmq

import custom_health_msg
import custom_rpy
import serialize as sz

##################################
#        Driver program
##################################

def driver (args):

    health_context = zmq.Context()
    health_socket = health_context.socket(zmq.REP)
    connect_health_string = "tcp://*:" + str (args.portHealth)
    health_socket.bind(connect_health_string)

    def send_request (cr):
        print ("ZMQ sending custom message via ZMQ's send_serialized method")
        health_socket.send_serialized (cr, sz.serialize_reply_to_frames)

    cm = custom_health_msg.CustomHealthMessage ()
    cr = custom_rpy.CustomReply ()

    #count = 0

    while True:
        print ("ZMQ receiving serialized custom HEALTH message")
        #  Wait for next request from client
        start_time = time.time ()
        cm = health_socket.recv_serialized (sz.deserialize_from_frames, copy=True)
        end_time = time.time ()
        print ("Deserialization took {} secs".format (end_time-start_time))
        print ("------ contents of HEALTH message after deserializing ----------")
        cm.dump ()
        #print ("Dumping contents of Custom Health Message")
        #print ("  Seq Num: {}".format (cm.seq_num))
        #print ("  Timestamp: {}".format (cm.ts))
        #print ("  Name: {}".format (cm.name))
        #print ("  Dispenser: {}".format (cm.dispenser))
        #print ("  Icemaker: {}".format (cm.icemaker))
        #print ("  Lightbulb: {}".format (cm.lightbulb))
        #print ("  Fridge_temp: {}".format (cm.fridge_temp))
        #print ("  Freezer_temp: {}".format (cm.freezer_temp))
        #print ("  Sensor_status: {}".format (cm.sensor_status))
        
        #  Do some 'work'
        time.sleep(1)

        # for every iteration, let us fill up our custom message with some info
        cr.seq_num = cm.seq_num # this will be our sequence number
        cr.ts = time.time ()  # current time
        if cm.seq_num>=0:
            cr.reply_request = 0  # reply request status GOOD
            cr.reply_status = 0 # reply status GOOD
        else:
            cr.reply_request = 1 # reply request status BAD
            cr.reply_status = 1 # reply status BAD
        print ("-----Iteration: {} contents of HEALTH message before serializing ----------".format (cm.seq_num))
        cr.dump ()
        #count+=1

        #  Send reply back to client
        #print ("Peer server sending ACK")
        #print ("ZMQ sending dummy ACK message")
        #health_socket.send_string("ACK")

        print(f"Peer server sending the serialized HEALTH message")
        start_time = time.time ()
        send_request (cr)
        end_time = time.time ()
        print ("Serialization took {} secs".format (end_time-start_time))

##################################
# Command line parsing
##################################
def parseCmdLineArgs ():
  # parse the command line
  parser = argparse.ArgumentParser ()

  # add optional arguments
  parser.add_argument ("-pH", "--portHealth", type=int, default=5555, help="Port that health server is listening on (default: 5555)")
  args = parser.parse_args ()

  return args

#------------------------------------------
# main function
def main ():
  """ Main program """

  print("Health Server Demo program for Flatbuffer serialization/deserialization")

  # first parse the command line args
  parsed_args = parseCmdLineArgs ()
    
  # start the driver code
  driver (parsed_args)

#----------------------------------------------
if __name__ == '__main__':
    main ()