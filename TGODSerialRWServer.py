'''
This is the Read/Write Serial Server code for use in the Cornell Spooky
By Tristan Kuzma
TO RUN: 
sudo python3 /home/cornelltgod/Documents/CornellSpooky/pymodbus-dev/TGODSerialRWServer.py
'''
# ----------------------------------------------------- # 
# IMPORTS # 

#Import the neccisary Libraries
import threading
from threading import Thread
import asyncio
import logging
import os
import sys
import time
import setproctitle         #pip install setproctitle

#Import from PyModbus
from examples import helper 
from pymodbus import __version__ as pymodbus_version
from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusServerContext,
    ModbusSlaveContext,
    ModbusSparseDataBlock,
)
from pymodbus import register_read_message 
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.transaction import ModbusRtuFramer 

#Import Server Implementations 
from pymodbus.server import (
	StartAsyncSerialServer,
    StartAsyncTcpServer,
    StartAsyncTlsServer,
    StartAsyncUdpServer,
    ModbusSerialServer
)

#from pymodbus.server import StopServer

print('Imports Pass')

debugLog = '/home/cornelltgod/Documents/CornellSpooky/SpookyDebug'

#Initialzie Logger
logging.basicConfig(filename=debugLog, filemode ='w', level=logging.DEBUG)


# ----------------------------------------------------- # 
# SETUP SERVER #

title = "TGODServer"

def setup_server(description=None, context=None, cmdline=None):
    localPID = os.getpid()
    setproctitle.setproctitle(title)
    process_name = setproctitle.getthreadtitle()
    
    
    logging.info(str(localPID) + "- Local PID")
    logging.info(str(process_name) + "- Process Name")
    """Run server setup."""
    args = helper.get_commandline(server=True, description=description, cmdline=cmdline)
    if context:
        args.context = context
    if not args.context:
        logging.info("### Create datastore bruh")
        
        args.store = "sequential" 
        datablock = ModbusSequentialDataBlock(0x00, [123] * 0xFFFF)  #This works every time. 
            
    
        context = ModbusSlaveContext(
        di=datablock, co=datablock, hr=datablock, ir=datablock
        )
        single = True

        # Build data storage
        args.context = ModbusServerContext(slaves=context, single=single)

    args.identity = ModbusDeviceIdentification(
        info_name={
            "VendorName": "Pymodbus",
            "ProductCode": "PM",
            "VendorUrl": "https://github.com/pymodbus-dev/pymodbus/examples",
            "ProductName": "Pymodbus Server",
            "ModelName": "Pymodbus Server",
            "MajorMinorRevision": pymodbus_version,
        }
    )

    return args

# ----------------------------------------------------- # 
# RUN THE SERVER #

async def run_async_server(args):
    """Run server."""
    args.comm = "serial"
    args.port = '/dev/ttyACM0'
    args.baudrate = 9600
    args.store = "sequential"   
    args.framer = ModbusRtuFramer
    
    txt = f"### start ASYNC server, listening on {args.port} - {args.comm}"
    logging.info(txt)
    
    #!! {INPUT} THIS IS WHERE I SET COMMS VARIABLES !!  
    
    
    if args.comm == "serial":
        server = await StartAsyncSerialServer(
            context=args.context,  # Data storage
            identity=args.identity,  # server identify
            #timeout=0.000000000001,  # waiting time for request to complete
            port=args.port,  # serial port
            # custom_functions=[],  # allow custom handling
            framer=args.framer,  # The framer strategy to use
            # handler=None,  # handler for each session
            stopbits=1,  # The number of stop bits to use
            bytesize=8,  # The bytesize of the serial messages
            parity="N",  # Which kind of parity to use
            baudrate=args.baudrate,  # The baud rate to use for the serial device
            handle_local_echo=True,  # Handle local echo of the USB-to-RS485 adaptor
            # ignore_missing_slaves=True,  # ignore request to a missing slave
            # broadcast_enable=False,  # treat slave_id 0 as broadcast address,
            # strict=True,  # use strict timing, t1.5 for Modbus RTU
            # defer_start=False,  # Only define server do not activate
            # python3 /home/cornellpi1/pymodbus-3.2.2/examples/server_asyncV2.py
	    )  
        
    return server

'''   
def stop():
	StopServer()
	logging.debug("Connection Terminated Sucsessfully")
'''

def updateServer():
    '''
    
    [WE MAY BE DELETING THIS FUNCTION IF WE'RE PASSING DIRECTLY FROM ASYNC.IO -> JSON]
    
    
    datablock = ModbusSequentialDataBlock(0x00, [123] * 0xEA60)  #This works every time. 
    context = ModbusSlaveContext(
    di=datablock, co=datablock, hr=datablock, ir=datablock
    )
    single = True
    '''
    #time.sleep(10)
    #logging.info("!!!! \n  ###Running Server Update###  \n !!!!") 
    #readValue = context.getValues(0x4, 4001, count =1)	#This does not update when the server is written to via the AMI portal. 
    #readValue = context.getValues(0x4, 1, count =1)
    #self = self.creation()
    #readValue = ModbusSlaveContext.getValues(ModbusDataBlock(), 0x4, 1, count = 1)	
    #logging.info("This is my update : " + str(readValue)) 
    #time.sleep(10)
    #threading.Timer(10, updateServer).start()	#This works, that's pretty gangster. 
	
# ----------------------------------------------------- # 
# MAIN LOOP #

if __name__ == "__main__":
    run_args = setup_server(description="Run asynchronous server.")
    #threading.Timer(10, updateServer).start()
    asyncio.run(run_async_server(run_args), debug=True)
    
    
   
