import os
import sys

import flatbuffers

##################################

from custom_health_msg import CustomHealthMessage
import CustomAppProto.HealthMessage
import CustomAppProto.Dispenser
import CustomAppProto.Lightbulb
import CustomAppProto.Sensor

##################################

import custom_order_msg
import CustomAppProto.OrderMessage

import CustomAppProto.Milk
import CustomAppProto.MilkType

import CustomAppProto.Veg
import CustomAppProto.VegType

import CustomAppProto.CanDrink
import CustomAppProto.CanType

import CustomAppProto.BottleDrink
import CustomAppProto.BottleType

import CustomAppProto.Bread
import CustomAppProto.BreadType

import CustomAppProto.Meat
import CustomAppProto.MeatType

##################################

from custom_rpy import CustomReply
import CustomAppProto.ReplyMessage
import CustomAppProto.ReplyRequest
import CustomAppProto.ReplyStatus

###################################################################################
###################################### HEALTH #####################################
###################################################################################

def serialize (cm):
    # first obtain the builder object that is used to create an in-memory representation
    # of the serialized object from the custom message
    builder = flatbuffers.Builder (0);

    # create the name string for the name field using
    # the parameter we passed
    name_field = builder.CreateString (cm.name)
    
    # let us create the serialized msg by adding contents to it.
    # Our custom msg consists of a seq num, timestamp, name, and an array of uint32s
    CustomAppProto.HealthMessage.Start (builder)  # serialization starts with the "Start" method
    CustomAppProto.HealthMessage.AddSeqNo (builder, cm.seq_num)
    CustomAppProto.HealthMessage.AddTs (builder, cm.ts)   # serialize current timestamp
    CustomAppProto.HealthMessage.AddName (builder, name_field)  # serialize the name
    CustomAppProto.HealthMessage.AddDispenser (builder, CustomAppProto.Dispenser.Dispenser().OPTIMAL)  # serialize the dummy data
    CustomAppProto.HealthMessage.AddIcemaker (builder, cm.icemaker)  # serialize the dummy data
    CustomAppProto.HealthMessage.AddLightbulb (builder, CustomAppProto.Lightbulb.Lightbulb().GOOD)  # serialize the dummy data
    CustomAppProto.HealthMessage.AddFridgeTemp (builder, cm.fridge_temp)  # serialize the dummy data
    CustomAppProto.HealthMessage.AddFreezerTemp (builder, cm.freezer_temp)  # serialize the dummy data
    CustomAppProto.HealthMessage.AddSensorStatus (builder, CustomAppProto.Sensor.Sensor().GOOD)  # serialize the dummy data
    serialized_msg = CustomAppProto.HealthMessage.End (builder)  # get the topic of all these fields

    # end the serialization process
    builder.Finish (serialized_msg)

    # get the serialized buffer
    buf = builder.Output ()

    # return this serialized buffer to the caller
    return buf

###################################################################################
###################################################################################

# serialize the custom message to iterable frame objects needed by zmq
def serialize_to_frames (cm):
  """ serialize into an interable format """
  print ("serialize custom message to iterable list")
  return [serialize (cm)]

###################################################################################
###################################################################################

# deserialize the incoming serialized structure into native data type
def deserialize (buf):
    cm = CustomHealthMessage ()
    
    packet = CustomAppProto.HealthMessage.HealthMessage.GetRootAs (buf, 0)

    # sequence number
    cm.seq_num = packet.SeqNo ()

    # timestamp received
    cm.ts = packet.Ts ()

    # name received
    cm.name = packet.Name ()

    # Dispenser received
    cm.dispenser = packet.Dispenser()

    # Icemaker efficiency received
    cm.icemaker = packet.Icemaker()

    # Lightbulb received
    cm.lightbulb = packet.Lightbulb()

    # Fridge temperature received
    cm.fridge_temp = packet.FridgeTemp()

    # Freezer temperature received
    cm.freezer_temp = packet.FreezerTemp()

    # Sensor Status received
    cm.sensor_status = packet.SensorStatus()

    return cm

# deserialize from frames
def deserialize_from_frames (recvd_seq):
  """ This is invoked on list of frames by zmq """
  assert (len (recvd_seq) == 1)
  #print ("type of each elem of received seq is {}".format (type (recvd_seq[i])))
  print ("received data over the wire = {}".format (recvd_seq[0]))
  cm = deserialize (recvd_seq[0])  # hand it to our deserialize method

  return cm


###################################################################################
###################################### REPLY ######################################
###################################################################################

def serialize_reply (cr):
    # first obtain the builder object that is used to create an in-memory representation
    # of the serialized object from the custom message
    builder = flatbuffers.Builder (0);
    
    # let us create the serialized msg by adding contents to it.
    # Our custom msg consists of a seq num, timestamp, name, and an array of uint32s
    CustomAppProto.ReplyMessage.Start (builder)  # serialization starts with the "Start" method
    CustomAppProto.ReplyMessage.AddSeqNo (builder, cr.seq_num)
    CustomAppProto.ReplyMessage.AddTs (builder, cr.ts)   # serialize current timestamp
    CustomAppProto.ReplyMessage.AddReplyRequest (builder, CustomAppProto.ReplyRequest.ReplyRequest().GOOD)  # serialize the dummy data
    CustomAppProto.ReplyMessage.AddReplyStatus (builder, CustomAppProto.ReplyStatus.ReplyStatus().GOOD)  # serialize the dummy data
    serialized_msg = CustomAppProto.ReplyMessage.End (builder)  # get the topic of all these fields

    # end the serialization process
    builder.Finish (serialized_msg)

    # get the serialized buffer
    buf = builder.Output ()

    # return this serialized buffer to the caller
    return buf

# serialize_reply the custom message to iterable frame objects needed by zmq
def serialize_reply_to_frames (cr):
  """ serialize_reply into an interable format """
  print ("serialize_reply custom message to iterable list")
  return [serialize_reply (cr)]

# deserialize the incoming serialized structure into native data type
def deserialize_reply (buf):
    cr = CustomReply ()
    
    packet = CustomAppProto.ReplyMessage.ReplyMessage.GetRootAs (buf, 0)

    # sequence number
    cr.seq_num = packet.SeqNo ()

    # timestamp received
    cr.ts = packet.Ts ()

    # reply_request received
    cr.reply_request = packet.ReplyRequest()

    # reply_status received
    cr.reply_status = packet.ReplyStatus()

    return cr

###################################################################################
###################################################################################

# deserialize_reply from frames
def deserialize_reply_from_frames (recvd_seq):
  """ This is invoked on list of frames by zmq """
  assert (len (recvd_seq) == 1)
  #print ("type of each elem of received seq is {}".format (type (recvd_seq[i])))
  print ("received data over the wire = {}".format (recvd_seq[0]))
  cr = deserialize_reply (recvd_seq[0])  # hand it to our deserialize_reply method

  return cr

###################################################################################
###################################### ORDER ######################################
###################################################################################

def serialize_order (co):  #msg refers to the complex struct in native format
  
    builder = flatbuffers.Builder (0);

    ##########################################
    ##########################################

    ######## START VEG ########

    # let us first get the list of milks done before we get the final root type done
    ser_veg = []   # list of serialized individual milks
    for i in range (len (co.vl)):   # for that many items in the veg list
        CustomAppProto.Veg.Start (builder)
        CustomAppProto.Veg.AddVtype (builder, co.vl[i].vtype)
        CustomAppProto.Veg.AddVquantity (builder, co.vl[i].vquantity)
        ser_veg.append (CustomAppProto.Veg.End (builder))

    # Now serialize the vector field inside veg order
    CustomAppProto.OrderMessage.StartVlVector (builder, len (co.vl))  # as many elements as in our native veg order
    for i in reversed (range (len (co.vl))):   # for that many items in the veg list
        builder.PrependUOffsetTRelative (ser_veg[i])
    ser_veg_vec = builder.EndVector ()  # get the serialized vector of veg

    ######## END VEG ########

    ##########################################
    ##########################################

    ######## START CANDRINKS ########

    # let us first get the list of candrinks done before we get the final root type done
    ser_can_drinks = []   # list of serialized individual candrinks
    for i in range (len (co.cl)):   # for that many items in the candrinks list
        CustomAppProto.CanDrink.Start (builder)
        CustomAppProto.CanDrink.AddCtype (builder, co.cl[i].ctype)
        CustomAppProto.CanDrink.AddCquantity (builder, co.cl[i].cquantity)
        ser_can_drinks.append (CustomAppProto.CanDrink.End (builder))

    # Now serialize the vector field inside candrinks order
    CustomAppProto.OrderMessage.StartClVector (builder, len (co.cl))  # as many elements as in our native candrinks order
    for i in reversed (range (len (co.cl))):   # for that many items in the candrinks list
        builder.PrependUOffsetTRelative (ser_can_drinks[i])
    ser_can_drinks_vec = builder.EndVector ()  # get the serialized vector of candrinks

    ######## END CANDRINKS ########

    ##########################################
    ##########################################

    ######## START BOTTLEDRINKS ########

    # let us first get the list of candrinks done before we get the final root type done
    ser_bottle_drinks = []   # list of serialized individual candrinks
    for i in range (len (co.bl)):   # for that many items in the candrinks list
        CustomAppProto.BottleDrink.Start (builder)
        CustomAppProto.BottleDrink.AddBtype (builder, co.bl[i].btype)
        CustomAppProto.BottleDrink.AddBquantity (builder, co.bl[i].bquantity)
        ser_bottle_drinks.append (CustomAppProto.BottleDrink.End (builder))

    # Now serialize the vector field inside candrinks order
    CustomAppProto.OrderMessage.StartBlVector (builder, len (co.bl))  # as many elements as in our native candrinks order
    for i in reversed (range (len (co.bl))):   # for that many items in the candrinks list
        builder.PrependUOffsetTRelative (ser_bottle_drinks[i])
    ser_bottle_drinks_vec = builder.EndVector ()  # get the serialized vector of candrinks

    ######## END BOTTLEDRINKS ########

    ##########################################
    ##########################################

    ######## START MILK ########

    # let us first get the list of milks done before we get the final root type done
    ser_milk = []   # list of serialized individual milks
    for i in range (len (co.ml)):   # for that many items in the milk list
        CustomAppProto.Milk.Start (builder)
        CustomAppProto.Milk.AddMtype (builder, co.ml[i].mtype)
        CustomAppProto.Milk.AddQuantity (builder, co.ml[i].quantity)
        ser_milk.append (CustomAppProto.Milk.End (builder))

    # Now serialize the vector field inside milk order
    CustomAppProto.OrderMessage.StartMlVector (builder, len (co.ml))  # as many elements as in our native milk order
    for i in reversed (range (len (co.ml))):   # for that many items in the milk list
        builder.PrependUOffsetTRelative (ser_milk[i])
    ser_milk_vec = builder.EndVector ()  # get the serialized vector of milks

    ######## END MILK ########

    ##########################################
    ##########################################

    ######## START BREAD ########

    # let us first get the list of bread done before we get the final root type done
    ser_bread = []   # list of serialized individual bread
    for i in range (len (co.yl)):   # for that many items in the bread list
        CustomAppProto.Bread.Start (builder)
        CustomAppProto.Bread.AddYtype (builder, co.yl[i].ytype)
        CustomAppProto.Bread.AddYquantity (builder, co.yl[i].yquantity)
        ser_bread.append (CustomAppProto.Bread.End (builder))

    # Now serialize the vector field inside bread order
    CustomAppProto.OrderMessage.StartYlVector (builder, len (co.yl))  # as many elements as in our native bread order
    for i in reversed (range (len (co.yl))):   # for that many items in the bread list
        builder.PrependUOffsetTRelative (ser_bread[i])
    ser_bread_vec = builder.EndVector ()  # get the serialized vector of bread

    ######## END BREAD ########

    ##########################################
    ##########################################

    ######## START MEAT ########

    # let us first get the list of meat done before we get the final root type done
    ser_meat = []   # list of serialized individual meat
    for i in range (len (co.xl)):   # for that many items in the meat list
        CustomAppProto.Meat.Start (builder)
        CustomAppProto.Meat.AddXtype (builder, co.xl[i].xtype)
        CustomAppProto.Meat.AddXquantity (builder, co.xl[i].xquantity)
        ser_meat.append (CustomAppProto.Meat.End (builder))

    # Now serialize the vector field inside meat order
    CustomAppProto.OrderMessage.StartXlVector (builder, len (co.xl))  # as many elements as in our native bread order
    for i in reversed (range (len (co.xl))):   # for that many items in the meat list
        builder.PrependUOffsetTRelative (ser_meat[i])
    ser_meat_vec = builder.EndVector ()  # get the serialized vector of meat

    ######## END MEAT ########

    ####################################################################
    ####################################################################

    # Now serialize the top level milk order
    CustomAppProto.OrderMessage.Start (builder)
    CustomAppProto.OrderMessage.AddSeqNo (builder, co.seq_num)
    CustomAppProto.OrderMessage.AddTs (builder, co.ts)

    ######## START VEG ########
    CustomAppProto.OrderMessage.AddVl (builder, ser_veg_vec)
    ######## END VEG ########

    ######## START CANDRINKS ########
    CustomAppProto.OrderMessage.AddCl (builder, ser_can_drinks_vec)
    ######## END CANDRINKS ########

    ######## START BOTTLEDRINKS ########
    CustomAppProto.OrderMessage.AddBl (builder, ser_bottle_drinks_vec)
    ######## END BOTTLEDRINKS ########

    ######## START MILK ########
    CustomAppProto.OrderMessage.AddMl (builder, ser_milk_vec)
    ######## END MILK ########

    ######## START BREAD ########
    CustomAppProto.OrderMessage.AddYl (builder, ser_bread_vec)
    ######## END BREAD ########

    ######## START MEAT ########
    CustomAppProto.OrderMessage.AddXl (builder, ser_meat_vec)
    ######## END MEAT ########

    ser_mo = CustomAppProto.OrderMessage.End (builder)
    
    # end the serialization process
    builder.Finish (ser_mo)

    # get the serialized buffer
    buf = builder.Output ()

    # return this serialized buffer to the caller
    return buf

###################################################################################
###################################################################################

# serialize the custom message to iterable frame objects needed by zmq
def serialize_order_to_frames (co):
    """ serialize into an interable format """
    print ("serialize custom message to iterable list")
    return [serialize_order (co)]


###################################################################################
###################################################################################

# deserialize the incoming serialized structure into native data type
def deserialize_order (buf):

    # First retrieve the flatbuf formatted milk order from the serialized buffer
    deser_mo = CustomAppProto.OrderMessage.OrderMessage.GetRootAs (buf, 0)

    # allocate some space for the deserialized milk order in our native format
    native_mo = custom_order_msg.CustomOrderMessage ()

    ##########################################
    ##########################################

    ######## START VEG ########

    for i in range (deser_mo.VlLength ()):   # this is the generated method on the class
        # instantiate a Veg object in native format and initialize its fields
        native_veg = custom_order_msg.Veg (custom_order_msg.VegType (deser_mo.Vl (i).Vtype ()),
                               # also use the generated method that gives the underlying Veg obj
                                              deser_mo.Vl (i).Vquantity ()) 
        # append this to the milk list
        native_mo.vl.append (native_veg)

    ######## END VEG ########

    ##########################################
    ##########################################

    ######## START CANDRINKS ########

    for i in range (deser_mo.ClLength ()):   # this is the generated method on the class
        # instantiate a CanDrink object in native format and initialize its fields
        native_candrink = custom_order_msg.CanDrink (custom_order_msg.CanType (deser_mo.Cl (i).Ctype ()),
                               # also use the generated method that gives the underlying CanDrink obj
                                              deser_mo.Cl (i).Cquantity ()) 
        # append this to the milk list
        native_mo.cl.append (native_candrink)

    ######## END CANDRINKS ########

    ##########################################
    ##########################################

    ######## START BOTTLEDRINKS ########

    for i in range (deser_mo.BlLength ()):   # this is the generated method on the class
        # instantiate a CanDrink object in native format and initialize its fields
        native_bottledrink = custom_order_msg.BottleDrink (custom_order_msg.BottleType (deser_mo.Bl (i).Btype ()),
                               # also use the generated method that gives the underlying BottleDrink obj
                                              deser_mo.Bl (i).Bquantity ()) 
        # append this to the milk list
        native_mo.bl.append (native_bottledrink)

    ######## END BOTTLEDRINKS ########

    ##########################################
    ##########################################

    ######## START MILK ########

    for i in range (deser_mo.MlLength ()):   # this is the generated method on the class
        # instantiate a Milk object in native format and initialize its fields
        native_milk = custom_order_msg.Milk (custom_order_msg.MilkType (deser_mo.Ml (i).Mtype ()),
                               # also use the generated method that gives the underlying Milk obj
                                              deser_mo.Ml (i).Quantity ()) 
        # append this to the milk list
        native_mo.ml.append (native_milk)

    ######## END MILK ########

    ##########################################
    ##########################################

    ######## START BREAD ########

    for i in range (deser_mo.YlLength ()):   # this is the generated method on the class
        # instantiate a Bread object in native format and initialize its fields
        native_bread = custom_order_msg.Bread (custom_order_msg.BreadType (deser_mo.Yl (i).Ytype ()),
                               # also use the generated method that gives the underlying Bread obj
                                              deser_mo.Yl (i).Yquantity ()) 
        # append this to the milk list
        native_mo.yl.append (native_bread)

    ######## END BREAD ########

    ##########################################
    ##########################################

    ######## START MEAT ########

    for i in range (deser_mo.XlLength ()):   # this is the generated method on the class
        # instantiate a Meat object in native format and initialize its fields
        native_meat = custom_order_msg.Meat (custom_order_msg.MeatType (deser_mo.Xl (i).Xtype ()),
                               # also use the generated method that gives the underlying Meat obj
                                              deser_mo.Xl (i).Xquantity ()) 
        # append this to the milk list
        native_mo.xl.append (native_meat)

    ######## END MEAT ########

    ##########################################
    ##########################################

    # sequence number
    native_mo.seq_num = deser_mo.SeqNo ()

    # timestamp received
    native_mo.ts = deser_mo.Ts ()

    # return the native formatted retrieved object
    return native_mo

###################################################################################
###################################################################################

# deserialize from frames
def deserialize_order_from_frames (recvd_seq):
    """ This is invoked on list of frames by zmq """
    print("len of recvd_seq = {}".format(len(recvd_seq)))
    assert (len (recvd_seq) == 1)
    #print ("type of each elem of received seq is {}".format (type (recvd_seq[i])))
    print ("received data over the wire = {}".format (recvd_seq[0]))
    co = deserialize_order (recvd_seq[0])  # hand it to our deserialize method

    return co