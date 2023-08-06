import logging 
#Api regisers and defaults
from pymodbus.client import ModbusTcpClient
from pymodbus.client import ModbusSerialClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian

#import Defaults
from .Defaults import Defaults
from .SentioRegisterMap import *
from .SentioTypes import *

class ModbusWrapper:

    def __init__(self, _client, slaveId):
        self.client = _client
        self.slaveId = slaveId


    def writeRegister(self, registerMapObject, value, _subIndex = 0):
        returnValue = 0
        
        try:
            address = registerMapObject.address
            if(registerMapObject.objectType == RegisterObjectType.ROOM):
                logging.debug("Detected Room Object {0} - {1}".format(address, _subIndex))
                address = (_subIndex * 100) + address
            if(registerMapObject.regType == RegisterType.INPUT_REGISTER):
                logging.error("Not possible to write input reg")
            elif(registerMapObject.regType == RegisterType.DISCRETE_INPUT):
                logging.error("Not possible to write discrete input reg")
            elif(registerMapObject.regType == RegisterType.HOLDING_REGISTER):
                returnValue = self.client.write_register(address, value, slave=self.slaveId)
        except Exception as e:
            logging.exception("error occured ==>  {0}".format(e))
            returnValue = -1
        return returnValue


    def readRegister(self, registerMapObject, _subIndex = 0):
        returnValue = 0
        logging.debug("Reading {0}".format(registerMapObject))
        try:
            address = registerMapObject.address
            if(registerMapObject.objectType == RegisterObjectType.ROOM):
                logging.debug("Detected Room Object {0} - {1}".format(address, _subIndex))
                address = (_subIndex * 100) + address
            if(registerMapObject.objectType == RegisterObjectType.DEHUMIDIFIERS):
                logging.debug("Detected Dehumidifier Object {0} - {1}".format(address, _subIndex))
                address = (_subIndex * 100) + address
            if(registerMapObject.objectType == RegisterObjectType.ITC_CIRCUIT):
                logging.debug("Detected ITC Circuit {0} - {1}".format(address, _subIndex))
                address = (_subIndex * 100) + address


            if(registerMapObject.regType == RegisterType.INPUT_REGISTER):
                response = self.client.read_input_registers(address, registerMapObject.count, slave=self.slaveId)
                if not response.isError(): 
                    if(registerMapObject.dataType == RegisterDataType.NUMERIC):
                        if(registerMapObject.count == 1):
                            returnValue = response.registers[0]
                        else:
                            decoder = BinaryPayloadDecoder.fromRegisters(response.registers, wordorder=Endian.Big, byteorder=Endian.Big)
                            #if(registerMapObject.count == 2):
                            if(registerMapObject.count == 2):
                                returnValue = decoder.decode_32bit_uint()
                            elif(registerMapObject.count == 4):
                                returnValue = decoder.decode_64bit_uint()
                            else:
                                logging.error("Unsupported decoding format {0}".format(registerMapObject.count))
                    elif(registerMapObject.dataType == RegisterDataType.STRING):
                        decoder = BinaryPayloadDecoder.fromRegisters(response.registers, wordorder=Endian.Big, byteorder=Endian.Big)
                        returnValue = decoder.decode_string(registerMapObject.count)  
                        returnValue = returnValue.decode('utf-8').replace('\0', '')
                    elif(registerMapObject.dataType == RegisterDataType.VAL_D2FP100):
                        if(registerMapObject.count == 1):
                            
                            fp100value = response.registers[0]
                            if fp100value > 0xF000: #most likely negative
                                fp100value = 0xFFFF - fp100value
                                fp100value = fp100value * -1
                                logging.debug("Detected abnormal high value {0} {1} {2}".format(fp100value, 0xFFFF - fp100value, 0xF000))
        
                            returnValue = float(fp100value / 100)
                            logging.debug("Registers: {0} {1} {2}".format(response.registers[0], float(0x7FFF), 0x7FFF))
                            logging.debug("Found {0} -> /100 = {1}".format(fp100value, returnValue))
                        else:
                            logging.error("Unsupported count for Holding Registers {0} D2_FP100".format(registerMapObject.count))

                    else:
                        logging.error("No support yet for Input Register with {0} type".format(registerMapObject.regType))
                else:
                    logging.error("Error while reading")
                    returnValue = -1
                #logging.error("Read InputReg complete {0}".format(returnValue))
            elif(registerMapObject.regType == RegisterType.DISCRETE_INPUT):
                logging.error("Discrete Input type {0} - {1}".format(address, registerMapObject.count))
            
            elif(registerMapObject.regType == RegisterType.HOLDING_REGISTER):
                #logging.error("Holding Register type {0} - {1}".format(registerMapObject.address, registerMapObject.count))
                response = self.client.read_holding_registers(address, registerMapObject.count, slave=self.slaveId)
                if not response.isError(): 
                    if(registerMapObject.dataType == RegisterDataType.NUMERIC):
                        if(registerMapObject.count == 1):
                            returnValue = response.registers[0]
                        else:
                            logging.error("Unsupported count for Holding Registers {0} Numeric".format(registerMapObject.count))
                    elif(registerMapObject.dataType == RegisterDataType.STRING):
                        decoder = BinaryPayloadDecoder.fromRegisters(response.registers, wordorder=Endian.Big, byteorder=Endian.Big)
                        returnValue =  decoder.decode_string(registerMapObject.count)
                        returnValue = returnValue.decode('utf-8').replace('\0', '')
                    elif(registerMapObject.dataType == RegisterDataType.VAL_D2FP100):
                        if(registerMapObject.count == 1):
                            fp100value = response.registers[0]
                            returnValue = fp100value / 100
                            logging.info("Found {0} -> /100 = {1}".format(fp100value, returnValue))
                        else:
                            logging.error("Unsupported count for Holding Registers {0} D2_FP100".format(registerMapObject.count))
                else:
                    logging.debug("Error while reading")
                    returnValue = -1
        except Exception as e:
            logging.exception("error occured ==>  {0}".format(e))
            return -1
        return returnValue