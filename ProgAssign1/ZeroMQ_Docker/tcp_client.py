import os
import sys
import time
import csv

import argparse

import random

import zmq

import custom_health_msg
import custom_order_msg
import custom_rpy
import serialize as sz

##################################
#        Driver program
##################################

def driver (args):

    main_context = zmq.Context()

    #  Socket to talk to server
    print("Connecting to hello world health server...")
    health_socket = main_context.socket(zmq.REQ)
    connect_health_string = "tcp://" + args.addrHealth + ":" + str (args.portHealth)
    health_socket.connect(connect_health_string)

    #  Socket to talk to server
    print("Connecting to hello world order server...")
    order_socket = main_context.socket(zmq.REQ)
    connect_order_string = "tcp://" + args.addrOrder + ":" + str (args.portOrder)
    order_socket.connect(connect_order_string)

    def send_health_request (cm):
        print ("ZMQ sending custom HEALTH message via ZMQ's send_serialized method")
        health_socket.send_serialized (cm, sz.serialize_to_frames)

    def send_order_request (co):
        print ("ZMQ sending custom ORDER message via ZMQ's send_serialized method")
        order_socket.send_serialized (co, sz.serialize_order_to_frames)

    # Create the initial message
    cm = custom_health_msg.CustomHealthMessage ()
    cr = custom_rpy.CustomReply ()

    # Counter is used to keep track of each iteration message that is sent and or recieved.
    counter = 0

    # We are going to collect the latency data into a list which will be writen to a text file.
    resLST =  []

    # Add header to lists to that when the list are writen to the text file, the file
    #   can then be imported using pandas with the correct column labels
    resLST.append(['iterStep', 'process', 'time'])

    ###################################################################################
    ###################################################################################

    for k in range(args.iterLoop):
    #  Do 10 requests, waiting each time for a response

        print("########################### HEALTH SECTION ###########################")

        ####################################################################
        ############################### HEALTH #############################
        ####################################################################

        for request in range(args.iterHealth):

            # for every iteration, let us fill up our custom message with some info
            cm.seq_num = counter # this will be our sequence number
            cm.ts = time.time ()  # current time
            cm.name = "LG" # assigned name
            cm.dispenser = random.randint(0, 2) # sensor status
            cm.icemaker = random.randint(1,100) # efficiency
            cm.lightbulb = random.randint(0, 1) # sensor status
            cm.fridge_temp = random.randint(1, 100) # internal fridge temp deg C
            cm.freezer_temp = random.randint(-40, 40) # internal freezer temp deg C
            if ((cm.freezer_temp >=-10) or (cm.freezer_temp  <= 20)):
                cm.sensor_status = 1 # sensor status
            else:
                cm.sensor_status = 0 # sensor status
            print ("-----Iteration: {} contents of message before serializing ----------".format (counter))
            cm.dump ()


            print(f"Peer client sending the serialized message")
            start_time = time.time ()
            send_health_request (cm)
            end_time = time.time ()
            print ("Serialization took {} secs".format (end_time-start_time))

            resLST.append([counter, 'health serialization', end_time-start_time])

            counter+=1

            ####################################################################
            ########################### HEALTH REPLY ###########################
            ####################################################################

            print ("ZMQ receiving serialized custom reply message")
            #  Wait for next request from client
            start_time = time.time ()
            cr = health_socket.recv_serialized (sz.deserialize_reply_from_frames, copy=True)
            end_time = time.time ()
            print ("Deserialization took {} secs".format (end_time-start_time))
            print ("------ contents of message after deserializing ----------")
            cr.dump ()

            resLST.append([counter, 'health deserialization', end_time-start_time])

            #counter+=1

        ####################################################################
        ############################### ORDER ##############################
        ####################################################################

        print("########################### ORDER SECTION ###########################")

        # Create the initial message
        co = custom_order_msg.CustomOrderMessage ()

        # for every iteration, we will include the counter and a time stamp
        co.seq_num = counter # this will be our sequence number
        co.ts = time.time ()  # current time

        ####################################################################
        ####################################################################

        ######## START MILK ########

        for jmilk in range (0,random.randint (1.0, 5.0)):
            co.ml.append (custom_order_msg.Milk (mtype=random.choice ([custom_order_msg.MilkType.ONEPERCENT, 
                                                                        custom_order_msg.MilkType.TWOPERCENT,
                                                                        custom_order_msg.MilkType.FATFREE,
                                                                        custom_order_msg.MilkType.WHOLE,
                                                                        custom_order_msg.MilkType.ALMOND,
                                                                        custom_order_msg.MilkType.CASHEW,
                                                                        custom_order_msg.MilkType.OAT
                                                                        ]),
                                             quantity=random.randint (1.0, 5.0)))
        
        ######## END MILK ########

        ##########################################
        ##########################################

        ######## START VEG ########

        for jveg in range (0, random.randint (1.0, 5.0)):
            co.vl.append (custom_order_msg.Veg (vtype=random.choice ([custom_order_msg.VegType.TOMATO, 
                                                                        custom_order_msg.VegType.CUCUMBER,
                                                                        custom_order_msg.VegType.POTATO,
                                                                        custom_order_msg.VegType.CARROT,
                                                                        custom_order_msg.VegType.SPINACH,
                                                                        custom_order_msg.VegType.LETTUCE,
                                                                        custom_order_msg.VegType.BROCCOLI,
                                                                        custom_order_msg.VegType.CAULIFLOWER,
                                                                        custom_order_msg.VegType.BOK_CHOY,
                                                                        custom_order_msg.VegType.ONION,
                                                                        custom_order_msg.VegType.GARLIC,
                                                                        custom_order_msg.VegType.GREEN_BEANS,
                                                                        custom_order_msg.VegType.PEAS,
                                                                        ]),
                                             vquantity=random.randint (1.0, 5.0)))
        
        ######## END VEG ########

        ##########################################
        ##########################################

        ######## START CANDRINKS ########

        for jcan in range (0,random.randint (1.0, 5.0)):
            co.cl.append (custom_order_msg.CanDrink (ctype=random.choice ([custom_order_msg.CanType.COCA_COLA, 
                                                                        custom_order_msg.CanType.PEPSI,
                                                                        custom_order_msg.CanType.DIET_COKE,
                                                                        custom_order_msg.CanType.DR_PEPPER,
                                                                        custom_order_msg.CanType.MOUNTAIN_DEW,
                                                                        custom_order_msg.CanType.SPRITE,
                                                                        custom_order_msg.CanType.DEIT_PEPSI,
                                                                        custom_order_msg.CanType.COKE_ZERO,
                                                                        custom_order_msg.CanType.DIET_DR_PEPPER,
                                                                        custom_order_msg.CanType.FANTA,
                                                                        custom_order_msg.CanType.SIERRA_MIST,
                                                                        custom_order_msg.CanType.SUNKIST,
                                                                        custom_order_msg.CanType.TAB,
                                                                        ]),
                                             cquantity=random.randint (1.0, 5.0)))
        
        ######## END CANDRINKS ########

        ##########################################
        ##########################################

        ######## START BOTTLEDRINKS ########

        for jbottle in range (0,random.randint (1.0, 5.0)):
            co.bl.append (custom_order_msg.BottleDrink (btype=random.choice ([custom_order_msg.BottleType.COCA_COLA, 
                                                                        custom_order_msg.BottleType.PEPSI,
                                                                        custom_order_msg.BottleType.DIET_COKE,
                                                                        custom_order_msg.BottleType.DR_PEPPER,
                                                                        custom_order_msg.BottleType.MOUNTAIN_DEW,
                                                                        custom_order_msg.BottleType.SPRITE,
                                                                        custom_order_msg.BottleType.DEIT_PEPSI,
                                                                        custom_order_msg.BottleType.COKE_ZERO,
                                                                        custom_order_msg.BottleType.DIET_DR_PEPPER,
                                                                        ]),
                                             bquantity=random.randint (1.0, 5.0)))
        
        ######## END CANDRINKS ########

        ##########################################
        ##########################################

        ######## START BREAD ########

        for jbread in range (0,random.randint (1.0, 5.0)):
            co.yl.append (custom_order_msg.Bread (ytype=random.choice ([custom_order_msg.BreadType.AREPA,
                                                                        custom_order_msg.BreadType.BAGUETTE,
                                                                        custom_order_msg.BreadType.BAGEL,
                                                                        custom_order_msg.BreadType.BRIOCHE,
                                                                        custom_order_msg.BreadType.CIABATTA,
                                                                        custom_order_msg.BreadType.CHALLAH,
                                                                        custom_order_msg.BreadType.ENGLISH_MUFFIN,
                                                                        custom_order_msg.BreadType.FOCACCIA,
                                                                        custom_order_msg.BreadType.HOKKAIDO,
                                                                        custom_order_msg.BreadType.IRISH_SODA_BREAD,
                                                                        custom_order_msg.BreadType.MULTIGRAIN,
                                                                        custom_order_msg.BreadType.NAAN,
                                                                        custom_order_msg.BreadType.PARATHA,
                                                                        custom_order_msg.BreadType.PITA,
                                                                        custom_order_msg.BreadType.RYE_BREAD,
                                                                        custom_order_msg.BreadType.SOURDOUGH,
                                                                        custom_order_msg.BreadType.WHITE_BREAD,
                                                                        custom_order_msg.BreadType.WHOLE_WHEAT_BREAD,
                                                                        ]),
                                             yquantity=random.randint (1.0, 5.0)))
        
        ######## END BREAD ########

        ##########################################
        ##########################################

        ######## START MEAT ########

        for jmeat in range (0,random.randint (1.0, 5.0)):
            co.xl.append (custom_order_msg.Meat (xtype=random.choice ([custom_order_msg.MeatType.PORK,
                                                                        custom_order_msg.MeatType.CHICKEN,
                                                                        custom_order_msg.MeatType.BEEF,
                                                                        custom_order_msg.MeatType.LAMB,
                                                                        custom_order_msg.MeatType.GOAT,
                                                                        custom_order_msg.MeatType.TURKEY,
                                                                        custom_order_msg.MeatType.DUCK,
                                                                        custom_order_msg.MeatType.BUFFALO,
                                                                        custom_order_msg.MeatType.GOOSE,
                                                                        custom_order_msg.MeatType.RABBIT,
                                                                        ]),
                                             xquantity=random.randint (1.0, 5.0)))
        
        ######## END MEAT ########

        ####################################################################
        ####################################################################

        print ("-----Iteration: {} contents of order message before serializing ----------".format (counter))
        co.dump ()


        print(f"Peer client sending the order serialized message")
        start_time = time.time ()
        send_order_request (co)
        end_time = time.time ()
        print ("Order Serialization took {} secs".format (end_time-start_time))

        resLST.append([counter, 'order serialization', end_time-start_time])

        counter+=1

        ####################################################################
        ############################ ORDER REPLY ###########################
        ####################################################################

        print ("ZMQ receiving serialized custom ORDER reply message")
        #  Wait for next request from client
        start_time = time.time ()
        cr = order_socket.recv_serialized (sz.deserialize_reply_from_frames, copy=True)
        end_time = time.time ()
        print ("ORDER Deserialization took {} secs".format (end_time-start_time))
        print ("------ contents of ORDER message after deserializing ----------")
        cr.dump ()

        resLST.append([counter, 'ORDER deserialization', end_time-start_time])

        #counter+=1

        ####################################################################
        ####################################################################

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

    # cleanup the sockets
    health_socket.close ()
    order_socket.close ()

##################################
# Command line parsing
##################################
def parseCmdLineArgs ():
  # parse the command line
  parser = argparse.ArgumentParser ()

  # add optional arguments
  parser.add_argument ("-ah", "--addrHealth", default="127.0.0.1", help="Health IP Address to connect to (default: localhost i.e., 127.0.0.1)")
  parser.add_argument ("-ao", "--addrOrder", default="127.0.0.1", help="Order IP Address to connect to (default: localhost i.e., 127.0.0.1)")
  parser.add_argument ("-ih", "--iterHealth", type=int, default=2, help="Number of health iterations (default: 2")
  parser.add_argument ("-lp", "--iterLoop", type=int, default=2, help="Number of overall iterations (default: 2")
  parser.add_argument ("-pH", "--portHealth", type=int, default=5555, help="Port that health server is listening on (default: 5555)")
  parser.add_argument ("-pO", "--portOrder", type=int, default=5556, help="Port that order server is listening on (default: 5556)")
  parser.add_argument ("-fN", "--fileName", type=str, default='healthOrderTime', help="Text file name to save latency data (default: healthOrderTime)")
  args = parser.parse_args ()

  return args

#------------------------------------------
# main function
def main ():
  """ Main program """

  print("Demo program for Flatbuffer serialization/deserialization")

  # first parse the command line args
  parsed_args = parseCmdLineArgs ()
    
  # start the driver code
  driver (parsed_args)

#----------------------------------------------
if __name__ == '__main__':
    print("Current libzmq version is %s" % zmq.zmq_version())
    print("Current pyzmq version is %s" % zmq.pyzmq_version())
    main ()
