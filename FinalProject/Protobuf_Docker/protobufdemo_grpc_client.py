#  Author: Aniruddha Gokhale
#  Created: Fall 2023
#
#  Purpose: demonstrate serialization of a user-defined data structure using
#  Protocol Buffers combined with gRPC. Note that here we
#  are more interested in how a serialized packet gets sent over the network
#  and retrieved. To that end, we really don't care even if the client and
#  server were both on the same machine or remote to each other.

# This one implements the client functionality
#

# Note that this code mimics what we did with FlatBufs+ZeroMQ but this time
# we mix Protocol Buffers and gRPC

# The different packages we need in this Python driver code
import os
import sys
import time  # needed for timing measurements and sleep

import random  # random number generator
import argparse  # argument parser

import logging

import grpc   # for gRPC

# import generated packages
import healthMessage_pb2 as hpb
import healthMessage_pb2_grpc as hpb_grpc

import orderMessage_pb2 as opb
import orderMessage_pb2_grpc as opb_grpc


##################################
#        Driver program
##################################

def driver (args):

  # first obtain a peer and initialize it
  print ("Driver program: create handle to the client and then run the code")
  try:

    # Use the insecure channel to establish connection with server
    print ("Instantiate insecure channel")
    connect_health_string = args.addrHealth + ":" + str (args.portHealth)
    channel = grpc.insecure_channel (connect_health_string)

    print ("Obtain a proxy object to the server")
    stub = hpb_grpc.HealthServiceStub (channel)

    # now send the serialized custom message for the number of desired iterations
    print ("Allocate the Request object that we will then populate in every iteration")
    req = hpb.HealthMessage ()

    # Counter is used to keep track of each iteration message that is sent and or recieved.
    counter = 0

    # We are going to collect the latency data into a list which will be writen to a text file.
    resLST =  []

    # Add header to lists to that when the list are writen to the text file, the file
    #   can then be imported using pandas with the correct column labels
    resLST.append(['iterStep', 'process', 'time'])

    for i in range (args.iters):
      # for every iteration, let us fill up our custom message with some info
      req.seq_no = i # this will be our sequence number
      req.ts = time.time ()  # current time
      req.name = "LG" # assigned name
      req.dispenser = random.randint(1, 3) # sensor status
      req.icemaker = random.randint(1,100) # efficiency
      req.lightbulb = random.randint(1, 2) # sensor status
      req.fridge_temp = random.randint(1, 100) # internal fridge temp deg C
      req.freezer_temp = random.randint(-40, 40) # internal freezer temp deg C
      if ((req.freezer_temp >=-10) or (req.freezer_temp  <= 20)):
          req.sensor_status = 2 # sensor status
      else:
          req.sensor_status = 1 # sensor status

      # for every iteration, let us fill up our custom message with some info
      # req.seq_no = i # this will be our sequence number
      # req.ts = time.time ()  # current time
      # req.name = name # assigned name
      print ("-----Iteration: {} contents of message before sending\n{} ----------".format (i, req))

      # now let the client send the message to its server part
      print ("Peer client sending the serialized message")
      start_time = time.time ()
      resp = stub.method (req)
      end_time = time.time ()
      print ("Got Response:\n", resp)
      print ("-----Iteration: {} contents of response message reply_request\n{} ----------".format (i, resp.reply_request))
      print ("sending/receiving took {} secs".format (end_time-start_time))
      resLST.append([counter, 'health serialization', end_time-start_time])

      counter+=1

      # ####################################################################
      # ############################### ORDER ##############################
      # ####################################################################

      # # print("########################### ORDER SECTION ###########################")

      # for every iteration, we will include the counter and a time stamp
      connect_order_string = args.addrOrder + ":" + str (args.portOrder)
      order_channel = grpc.insecure_channel (connect_order_string)
      order_stub = opb_grpc.OrderServiceStub (order_channel)
      order_req = opb.Order ()

      order_req.seq_no = i # this will be our sequence number
      order_req.ts = time.time ()  # current time
      order_req.veggies.carrots = random.randint(1,100)
      order_req.veggies.cucumber = random.randint(1,100)
      order_req.veggies.onions = random.randint(1,100)
      order_req.veggies.potatoes = random.randint(1,100)
      order_req.veggies.tomato = random.randint(1,100)
      order_req.veggies.broccoli = random.randint(1,100)

      for q in range(random.randint(1,5)):
        bread = opb.Bread()
        bread.type = random.randint(1,3)
        bread.quantity = random.randint(1,100)
        order_req.bread.append(bread)

      for q in range(random.randint(1,5)):
        milk = opb.Milk()
        milk.type = random.randint(1,7)
        milk.quantity = random.randint(1,100)
        order_req.milk.append(milk)

      for q in range(random.randint(1,5)):
        meat = opb.Meat()
        meat.type = random.randint(1,4)
        meat.quantity = random.randint(1,100)
        order_req.meat.append(meat)

      order_req.drinks.cans.coke = random.randint(1,100)
      order_req.drinks.cans.pepsi = random.randint(1,100)
      order_req.drinks.cans.beer = random.randint(1,100)

      order_req.drinks.bottles.gingerale = random.randint(1,100)
      order_req.drinks.bottles.wine = random.randint(1,100)
      order_req.drinks.bottles.sprite = random.randint(1,100)
      
      print ("-----Iteration: {} contents of message before sending\n{} ----------".format (i, order_req))

      # now let the client send the message to its server part
      print ("Peer client sending the serialized message")
      start_time = time.time ()
      order_resp = order_stub.method (order_req)
      end_time = time.time ()
      print ("-----Iteration: {} contents of response message reply_request\n{} ----------".format (i, order_resp.reply_request))
      print ("sending/receiving took {} secs".format (end_time-start_time))
      resLST.append([counter, 'order serialization', end_time-start_time])

      counter+=1

      # Save end-to-end latency data to txt file
      fname = args.fileName + ".txt"
      with open(fname, 'w') as x:
          for sub_list in resLST:
              #print(len(sub_list))
              count=0
              for item in sub_list:
                  #print(item)
                  if count < len(sub_list)-1:
                      x.write(str(item) + ',')
                      count+=1
                  else:
                      x.write(str(item) + '')
              x.write("\n")

  except Exception as e:
    print (e)
    return

  
##################################
# Command line parsing
##################################
def parseCmdLineArgs ():
    # parse the command line
    parser = argparse.ArgumentParser ()

    # add optional arguments
    parser.add_argument ("-ah", "--addrHealth", default="127.0.0.1", help="Health IP Address to connect to (default: localhost i.e., 127.0.0.1)")
    parser.add_argument ("-ao", "--addrOrder", default="127.0.0.1", help="Order IP Address to connect to (default: localhost i.e., 127.0.0.1)")
    parser.add_argument ("-i", "--iters", type=int, default=10, help="Number of iterations to run (default: 10)")
    parser.add_argument ("-pH", "--portHealth", type=int, default=5577, help="Port that health server is listening on (default: 5555)")
    parser.add_argument ("-pO", "--portOrder", type=int, default=5578, help="Port that order server is listening on (default: 5556)")
    parser.add_argument ("-fN", "--fileName", type=str, default='healthOrderTime', help="Text file name to save latency data (default: healthOrderTime)")
    
    # parse the args
    args = parser.parse_args ()

    return args
    
#------------------------------------------
# main function
def main ():
  """ Main program """

  print("Demo program for Protocol Buffers with gRPC serialization/deserialization")

  # first parse the command line args
  parsed_args = parseCmdLineArgs ()
    
  # start the driver code
  driver (parsed_args)

#----------------------------------------------
if __name__ == '__main__':
    main ()
