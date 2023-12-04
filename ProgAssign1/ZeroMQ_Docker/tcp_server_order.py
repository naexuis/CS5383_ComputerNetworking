import os
import sys
import time

import argparse

import random

import zmq

import custom_order_msg
import custom_rpy
import serialize as sz

##################################
#        Driver program
##################################

def driver (args):

    order_context = zmq.Context()
    order_socket = order_context.socket(zmq.REP)
    connect_order_string = "tcp://*:" + str (args.portOrder)
    order_socket.bind(connect_order_string)

    def send_request (cr):
        print ("ZMQ sending custom message via ZMQ's send_serialized method")
        order_socket.send_serialized (cr, sz.serialize_reply_to_frames)

    co = custom_order_msg.CustomOrderMessage ()
    cr = custom_rpy.CustomReply ()

    #count = 0

    while True:
        print ("ZMQ receiving serialized custom ORDER message")
        #  Wait for next request from client
        start_time = time.time ()
        co = order_socket.recv_serialized (sz.deserialize_order_from_frames, copy=True)
        end_time = time.time ()

        print ("Deserialization took {} secs".format (end_time-start_time))
        print ("------ contents of ORDER message after deserializing ----------")
        co.dump ()

        #  Do some 'work'
        time.sleep(1)

        # for every iteration, let us fill up our custom message with some info
        cr.seq_num = co.seq_num # this will be our sequence number
        cr.ts = time.time ()  # current time
        if co.seq_num>=0:
            cr.reply_request = 0  # reply request status GOOD
            cr.reply_status = 0 # reply status GOOD
        else:
            cr.reply_request = 1 # reply request status BAD
            cr.reply_status = 1 # reply status BAD
        print ("-----Iteration: {} contents of ORDER message before serializing ----------".format (co.seq_num))
        cr.dump ()
        #count+=1

        #  Send reply back to client
        #print ("Peer server sending ACK")
        #print ("ZMQ sending dummy ACK message")
        #health_socket.send_string("ACK")

        print(f"Peer server sending the serialized ORDER message")
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
  parser.add_argument ("-pO", "--portOrder", type=int, default=5556, help="Port that order server is listening on (default: 5556)")
  args = parser.parse_args ()

  return args

#------------------------------------------
# main function
def main ():
  """ Main program """

  print("Order Server Demo program for Flatbuffer serialization/deserialization")

  # first parse the command line args
  parsed_args = parseCmdLineArgs ()
    
  # start the driver code
  driver (parsed_args)

#----------------------------------------------
if __name__ == '__main__':
    main ()