"""
Author                          : SABARI SARAVANAN M
Developed Tool and Version      : Python 3.9
Description                     : General DIO functions for NI8452
Module Name                     : NIUSB-8452 DIO Interface
Module Version                  : 0.0.1
Created                         : February 2021

"""
import ctypes as c                                              # It provides C compatible data types, and allows calling functions in DLLs or shared libraries.
from NI8452.general import General                              # Importing main class

class DIO(General):
    """
     This class makes Python calls to the C DLL of NI USB 8452 (ni845x.dll).
     Use this following example line with DIO device.

        ni845xSetIoVoltageLevel(33)                             # Set the I/O Voltage Level
        ni845xDioSetDriverType(0,1)                             # Sets the DIO Driver Type
        ni845xDioSetPortLineDirectionMap(0,128)                 # Sets the Line Direction Map
        ni845xDioWriteLine(0,7,1)                               # Writes the Digital Line
        ni845xDioReadLine(0,7)                                  # Reads the Digital Line
    """

    def __init__(self):
        super(DIO, self).__init__()                             # Invoking the main(General) class

    #############################################################
    # Basic
    #############################################################

    def ni845xDioSetPortLineDirectionMap(self, dio_port=0, map=0):
        """
        Calls the NI USB-8452 C API function ni845xI2cConfigurationOpen whose prototype is
        int32 ni845xDioSetPortLineDirectionMap (NiHandle DeviceHandle, uInt8 DioPort, uInt8 Map);
        :param: NiHandle DeviceHandle, uInt8 DioPort, uInt8 Map
        :return: None
            uInt8 DioPort - The DIO port that contains the LineNumber.
            uInt8 Map     - If bit x = 1, line x is an output. If bit x = 0, line x is an input.
        """
        returnvalue = self.ni8452.ni845xDioSetPortLineDirectionMap(self.device_handle, c.c_uint8(dio_port), c.c_uint8(map))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)

    def ni845xDioSetDriverType(self, dioport=0, type=1):
        """
        Calls the NI USB-8452 C API function ni845xI2cConfigurationOpen whose prototype is
        int32 ni845xDioSetDriverType (NiHandle DeviceHandle, uInt8 DioPort, uInt8 Type);
        :param: NiHandle DeviceHandle, uInt8 DioPort, uInt8 Type
        :return: None
            uInt8 DioPort - The DIO port that contains the LineNumber.
            uInt8 Type    - The desired output driver type. Type uses the following values:
                                • kNi845xOpenDrain (0): The port is configured for open-drain.
                                • kNi845xPushPull (1): The port is configured for push-pull.
                            The default value of this property is Push-Pull.
        """
        returnvalue = self.ni8452.ni845xDioSetDriverType(self.device_handle, c.c_uint8(dioport), c.c_uint8(type))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)

    def ni845xDioWriteLine(self, portnumber=0, linenumber=0, writedata=0):
        """
        Calls the NI USB-8452 C API function ni845xI2cConfigurationOpen whose prototype is
        int32 ni845xDioWriteLine (NiHandle DeviceHandle, uInt8 PortNumber, uInt8 LineNumber, int32 WriteData);
        :param: NiHandle DeviceHandle, uInt8 PortNumber, uInt8 LineNumber, int32 WriteData
        :return: None
            uInt8 PortNumber - The DIO port that contains the LineNumber.
            uInt8 LineNumber - The DIO line to write.
            int32 WriteData  - The value to write to the line. WriteData uses the following values:
                                • kNi845xDioLogicLow (0): The line is set to the logic low state.
                                • kNi845xDioLogicHigh (1): The line is set to the logic high state.
        """
        returnvalue = self.ni8452.ni845xDioWriteLine(self.device_handle, c.c_uint8(portnumber), c.c_uint8(linenumber), c.c_int32(writedata))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)

    def ni845xDioWritePort(self, portnumber=0, writedata=0):
        """
        Calls the NI USB-8452 C API function ni845xI2cConfigurationOpen whose prototype is
        int32 ni845xDioWriteLine (NiHandle DeviceHandle, uInt8 PortNumber, uInt8 WriteData);
        :param: NiHandle DeviceHandle, uInt8 PortNumber, uInt8 WriteData
        :return: None
            uInt8 PortNumber - The DIO port that contains the LineNumber.
            uInt8 WriteData  - The value to write to the DIO port. Only lines configured for output are updated.
        """
        returnvalue = self.ni8452.ni845xDioWriteLine(self.device_handle, c.c_uint8(portnumber), c.c_uint8(writedata))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)

    def ni845xDioReadLine(self, portnumber=0, linenumber=0):
        """
        Calls the NI USB-8452 C API function ni845xI2cConfigurationOpen whose prototype is
        int32 ni845xDioReadLine (NiHandle DeviceHandle, uInt8 PortNumber, uInt8 LineNumber, int32 * pReadData);
        :param: NiHandle DeviceHandle, uInt8 PortNumber, uInt8 LineNumber, int32 * pReadData
        :return: None
            uInt8 PortNumber  - PortNumber specifies the DIO port that contains the LineNumber.
            uInt8 LineNumber  - LineNumber specifies the DIO line to read.
            int32 * pReadData - Contains the value read from the line. pReadData uses the following values:
                                    • kNi845xDioLogicLow (0): The line is set to the logic low state.
                                    • kNi845xDioLogicHigh (1): The line is set to the logic high state.
        """
        readline =  c.c_int32()
        returnvalue = self.ni8452.ni845xDioReadLine(self.device_handle, c.c_uint8(portnumber), c.c_uint8(linenumber), c.byref(readline))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)
        return (int("".join(filter(str.isdigit, str(readline)))))

    def ni845xDioReadPort(self, portnumber=0):
        """
        Calls the NI USB-8452 C API function ni845xI2cConfigurationOpen whose prototype is
        int32 ni845xDioReadLine (NiHandle DeviceHandle, uInt8 PortNumber, uInt8 * pReadData);
        :param: NiHandle DeviceHandle, uInt8 PortNumber, uInt8 * pReadData
        :return: None
            uInt8 PortNumber  - PortNumber specifies the DIO port that contains the LineNumber.
            uInt8 * pReadData - Contains the value read from the DIO port. If a DIO pin was previously configured for
                                input, the logic level being driven onto it by external circuitry is returned. If a DIO pin
                                was previously configured for output, the logic level driven onto the pin internally is
                                returned. pReadData bit n = DIO n.
        """
        readport = c.c_int32()
        returnvalue = self.ni8452.ni845xDioReadLine(self.device_handle, c.c_uint8(portnumber), c.byref(readport))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)
        return (int("".join(filter(str.isdigit, str(readport)))))
