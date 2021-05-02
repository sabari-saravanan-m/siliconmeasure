"""
Author                          : SABARI SARAVANAN M
Developed Tool and Version      : Python 3.9
Description                     : General I2c-API functions for NI8452
Module Name                     : NIUSB-8452 I2C Interface
Module Version                  : 0.0.1
Created                         : February 2021

"""
import ctypes as c                                          # It provides C compatible data types, and allows calling functions in DLLs or shared libraries.
from NI8452.general import General                          # Importing main class

class I2C(General):
    """
     This class makes Python calls to the C DLL of NI USB 8452 (ni845x.dll).
     Use this following example line with I2C device.

        ni845xI2cConfigurationOpen()                        # Create a new configuration reference to use with the NI-8452 I2c Basic API

        ni845xI2cConfigurationSetAddress(0)                 # Sets the configuration address
        ni845xI2cConfigurationSetAddressSize(0)             # Sets the configuration address size
        ni845xI2cConfigurationSetClockRate(100)             # Sets the configuration clock rate in kilohertz
        ni845xI2cWrite(2, [0xaa,0xaa])                      # Writes an array of data to an I2C slave device
        ni845xI2cRead(128, 2)                               # Reads an array of data from an I2C slave device
        ni845xI2cWriteRead(1, [0x9A], 3)                    # Writes and reads an array of data to/from an I2C slave device

        ni845xI2cConfigurationClose()                       # Close configuration reference with the NI-8452 SPI Basic API

    """

    def __init__(self):
        """ Invoking the main(General) class
        """
        super(I2C, self).__init__()                         # Invoking the main(General) class
        self.status = 0

    #############################################################
    # General Device
    #############################################################

    def ni845xI2cSetPullupEnable(self, pullup_enable=0):
        """
        Calls the NI USB-8452 C API function ni845xClose whose prototype is
        int32 ni845xI2cSetPullupEnable (NiHandle DeviceHandle, uInt8 Enable);
        :param:     NiHandle DeviceHandle Device handle returned from ni845xOpen.
        uInt8 Enable:   The setting for the pullup resistors. Enable uses the following values:
                        • kNi845xPullupDisable (0): Pullups are disabled.
                        • kNi845xPullupEnable (1): Pullups are enabled.
        :return: None
        """
        returnvalue = self.ni8452.ni845xI2cSetPullupEnable(self.device_handle, c.c_uint8(pullup_enable))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)

    #############################################################
    # Configuration
    #############################################################

    def ni845xI2cConfigurationOpen(self):
        """
        Calls the NI USB-8452 C API function ni845xI2cConfigurationOpen whose prototype is
        int32 ni845xI2cConfigurationOpen (NiHandle * pConfigurationHandle);
        :param: None
        :return: configuration handle
        """
        returnvalue = self.ni8452.ni845xI2cConfigurationOpen(c.byref(self.configuration_handle))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)

    def ni845xI2cConfigurationClose(self):
        """
        Calls the NI USB-8452 C API function ni845xI2cConfigurationClose whose prototype is
        int32 ni845xI2cConfigurationClose (NiHandle ConfigurationHandle);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xI2cConfigurationOpen.
        :return: None
        """
        returnvalue = self.ni8452.ni845xI2cConfigurationOpen(self.configuration_handle)
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)

    def ni845xI2cConfigurationSetAckPollTimeout(self, timeout=0):
        """
        Calls the NI USB-8452 C API function  whose prototype is
        int32 ni845xI2cConfigurationSetAckPollTimeout (NiHandle ConfigurationHandle, uInt16 * Timeout);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xI2cConfigurationOpen.
        :return: None
                Specifies the I2C ACK poll timeout in milliseconds. When this value is zero, ACK
                polling is disabled. Otherwise, the ni845xI2cRead, ni845xI2cWrite, and
                ni845xI2cWriteRead API calls ACK poll until an acknowledge (ACK) is detected or the timeout is reached.
                ACK polling is not supported with 10-bit addressing. If the configuration's address size
                is set to 10 bits and Timeout is nonzero, an error is generated when attempting an I/O API call.
                The default value is 0 ms (disabled).
        """
        returnvalue = self.ni8452.ni845xI2cConfigurationSetAckPollTimeout(self.configuration_handle, c.c_uint16(timeout))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)

    def ni845xI2cConfigurationGetAckPollTimeout(self):
        """
        Calls the NI USB-8452 C API function  whose prototype is
        int32 ni845xI2cConfigurationGetAckPollTimeout (NiHandle ConfigurationHandle, uInt16 * pTimeout);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xI2cConfigurationOpen.
        :return: None
            retrieve the I2C ACK poll timeout in milliseconds.
        """
        timeout = c.c_uint16()
        returnvalue = self.ni8452.ni845xI2cConfigurationGetAckPollTimeout(self.configuration_handle, c.byref(timeout))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)
        return timeout

    def ni845xI2cConfigurationSetAddress(self, address=0x00):
        """
        Calls the NI USB-8452 C API function  whose prototype is
        int32 ni845xI2cConfigurationSetAddress (NiHandle ConfigurationHandle, uInt16 * Address);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xI2cConfigurationOpen.
        :return: None
                The slave address. For 7-bit device addressing, the NXP I2C specification defines a 7-bit
                slave address and a direction bit. During the address phase of an I2C transaction, these
                values are sent across the bus as one byte (slave address in bits 7–1, direction in bit 0).
                The NI-845x software follows the convention used in the NXP I2C specification and
                defines an address for a 7-bit device as a 7-bit value. The NI-845x software internally sets
                the direction bit to the correct value, depending on the function (write or read). Some
                manufacturers specify the address for their 7-bit device as a byte. In such cases, bits 7–1
                contain the slave address, and bit 0 contains the direction. When using the NI-845x
                software, discard the direction bit and right-shift the byte value by one to create the 7-bit
                address.
                The address default value is 0.
        """
        returnvalue = self.ni8452.ni845xI2cConfigurationSetAddress(self.configuration_handle, c.c_uint16(address))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)

    def ni845xI2cConfigurationGetAddress(self):
        """
        Calls the NI USB-8452 C API function  whose prototype is
        int32 ni845xI2cConfigurationGetAddress (NiHandle ConfigurationHandle, uInt16 * pAddress);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xI2cConfigurationOpen.
        :return: None
            retrieve the I2C configuration slave address without the direction bit.
        """
        address = c.c_uint16()
        returnvalue = self.ni8452.ni845xI2cConfigurationGetAddress(self.configuration_handle, c.byref(address))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)
        return address

    def ni845xI2cConfigurationSetAddressSize(self, address_size=0):
        """
        Calls the NI USB-8452 C API function  whose prototype is
        int32 ni845xI2cConfigurationSetAddressSize (NiHandle ConfigurationHandle, int32 * Size);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xI2cConfigurationOpen.
        :return: None
        Size uses the following values;
            • kNi845xI2cAddress7Bit (0): The NI 845x hardware uses the standard 7-bit
              addressing when communicating with the I2C slave device.
            • kNi845xI2cAddress10Bit (1): The NI 845x hardware uses the extended 10-bit
              addressing when communicating with the I2C slave device.
        the configuration address size as either 7 bits or 10 bits(default is 7 bits).
        """
        returnvalue = self.ni8452.ni845xI2cConfigurationSetAddressSize(self.configuration_handle, c.c_int32(address_size))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)

    def ni845xI2cConfigurationGetAddressSize(self):
        """
        Calls the NI USB-8452 C API function  whose prototype is
        int32 ni845xI2cConfigurationGetAddressSize (NiHandle ConfigurationHandle, int32 * pSize);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xI2cConfigurationOpen.
        :return: None
            retrieve the addressing scheme to use when addressing the I2C slave device this configuration describes.
        """
        address_size = c.c_int32()
        returnvalue = self.ni8452.ni845xI2cConfigurationGetAddressSize(self.configuration_handle, c.byref(address_size))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)
        return address_size

    def ni845xI2cConfigurationSetClockRate(self, clockrate=100):
        """
        Calls the NI USB-8452 C API function ni845xI2cConfigurationSetClockRate whose prototype is
        int32 ni845xI2cConfigurationSetClockRate (NiHandle ConfigurationHandle,uInt16 ClockRate);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xI2cConfigurationOpen.
            uInt16 ClockRate: Specifies the I2C clock rate in kilohertz. RRefer to Chapter 3, NI USB-845x Hardware
                              Overview, to determine which clock rates your NI 845x device supports.
                              If your hardware does not support the supplied clock rate, a warning is generated, and the next smallest
                              supported clock rate is used. If the supplied clock rate is smaller than the smallest
                              supported clock rate, an error is generated.
            The default value for the clock rate is 100 kHz.
        :return: None
        """
        returnvalue = self.ni8452.ni845xI2cConfigurationSetClockRate(self.configuration_handle, c.c_uint16(clockrate))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)

    def ni845xI2cConfigurationGetClockRate(self):
        """
        Calls the NI USB-8452 C API function ni845xI2cConfigurationGetClockRate whose prototype is
        int32 ni845xI2cConfigurationGetClockRate (NiHandle ConfigurationHandle,uInt16 * pClockRate);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xI2cConfigurationOpen.
        :return: uInt16 * pClockRate:
            A pointer to an unsigned 16-bit integer to store the clock rate in.
            retrieve the I2C clock rate in kilohertz.
        """
        clockrate = c.c_uint16()
        returnvalue = self.ni8452.ni845xI2cConfigurationGetClockRate(self.configuration_handle, c.byref(clockrate))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)
        return clockrate

    def ni845xI2cConfigurationSetHSClockRate(self, hsc_clockrate=1666):
        """
        Calls the NI USB-8452 C API function ni845xI2cConfigurationGetClockRate whose prototype is
        int32 ni845xI2cConfigurationSetHSClockRate (NiHandle ConfigurationHandle, uInt16 * HSClockRate);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xI2cConfigurationOpen.
        :return: uInt16 * HSClockRate: Specifies the I2C clock rate in kilohertz. Refer to Appendix A, NI USB-845x Hardware
                                       Specifications, to determine which High Speed clock rates your NI 845x device supports.
                                       If your hardware does not support the supplied clock rate, a warning is generated, and the
                                       next smallest supported clock rate is used.
                                       If the supplied clock rate is smaller than the smallest supported clock rate, an error is generated.
        The clock rate default value is 1666 Hz.
        """
        returnvalue = self.ni8452.ni845xI2cConfigurationSetHSClockRate(self.configuration_handle, c.c_uint16(hsc_clockrate))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)

    def ni845xI2cConfigurationGetHSClockRate(self):
        """
        Calls the NI USB-8452 C API function ni845xI2cConfigurationGetClockRate whose prototype is
        int32 ni845xI2cConfigurationGetHSClockRate (NiHandle ConfigurationHandle, uInt16 * pHSClockRate);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xI2cConfigurationOpen.
        :return: uInt16 * pHSClockRate:
            A pointer to an unsigned 16-bit integer to store the clock rate in.
            retrieve the I2C High Speed clock rate in kilohertz.
        """
        hsc_clockrate = c.c_uint16()
        returnvalue = self.ni8452.ni845xI2cConfigurationGetHSClockRate(self.configuration_handle, c.byref(hsc_clockrate))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)
        return hsc_clockrate

    def ni845xI2cConfigurationSetHSEnable(self, hs_enable=0):
        """
        Calls the NI USB-8452 C API function ni845xI2cConfigurationGetClockRate whose prototype is
        int32 ni845xI2cConfigurationSetHSEnable (NiHandle ConfigurationHandle, uInt16 * HSEnable);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xI2cConfigurationOpen.
        :return: uInt8 * HSEnable:  Specifies the I2C High Speed enabled status. Refer to Appendix A, NI USB-845x
                                    Hardware Specifications, to determine if your NI 845x device supports I2C High Speed mode.
                                    If your hardware does not support I2C High Speed Mode, an error is generated.
        HSEnable uses the following values:
            • kNi845xHSDisable (0): Disable High Speed mode.
            • kNi845xHSEnable (1): Enable High Speed mode.
            The default value is kNi845xHSDisable.
        """
        returnvalue = self.ni8452.ni845xI2cConfigurationSetHSEnable(self.configuration_handle, c.c_uint8(hs_enable))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)

    def ni845xI2cConfigurationGetHSEnable(self):
        """
        Calls the NI USB-8452 C API function ni845xI2cConfigurationGetClockRate whose prototype is
        int32 ni845xI2cConfigurationGetHSEnable (NiHandle ConfigurationHandle, uInt8 * pHSEnable);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xI2cConfigurationOpen.
        :return: uInt8 * pHSEnable:
            A pointer to an unsigned 8-bit integer to store the enabled status in.
            retrieve the configuration High Speed enable status.
        """
        hs_enable = c.c_uint8()
        returnvalue = self.ni8452.ni845xI2cConfigurationGetHSEnable(self.configuration_handle, c.byref(hs_enable))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)
        return hs_enable

    def ni845xI2cConfigurationSetHSMasterCode(self, hs_mastercode=1):
        """
        Calls the NI USB-8452 C API function ni845xI2cConfigurationGetClockRate whose prototype is
        int32 ni845xI2cConfigurationSetHSMasterCode (NiHandle ConfigurationHandle, uInt8 * HSMasterCode);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xI2cConfigurationOpen.
        :uInt16 * pHSMasterCode
            Specifies the I2C High Speed master code.
            The default value is 1.
        """
        returnvalue = self.ni8452.ni845xI2cConfigurationSetHSMasterCode(self.configuration_handle, c.c_uint8(hs_mastercode))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)

    def ni845xI2cConfigurationGetHSMasterCode(self):
        """
        Calls the NI USB-8452 C API function ni845xI2cConfigurationGetClockRate whose prototype is
        int32 ni845xI2cConfigurationGetHSMasterCode (NiHandle ConfigurationHandle, uInt8 * pHSMasterCode);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xI2cConfigurationOpen.
        :uInt16 * pHSMasterCode
            A pointer to an unsigned 8-bit integer to store the master code in.
            retrieve the I2C High Speed master code.
        """
        hs_mastercode = c.c_uint8()
        returnvalue = self.ni8452.ni845xI2cConfigurationGetHSMasterCode(self.configuration_handle, c.byref(hs_mastercode))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)
        return hs_mastercode

    def ni845xI2cConfigurationSetPort(self, port=0):
        """
        Calls the NI USB-8452 C API function ni845xI2cConfigurationSetPort whose prototype is
        int32 ni845xI2cConfigurationSetPort (NiHandle ConfigurationHandle,uInt8 Port);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xI2cConfigurationOpen.
            uInt8 Port: Specifies the I2c port that this configuration communicates across.
                Refer to Chapter 3, NI USB-845x Hardware Overview, to determine the number of I2c
                ports your NI 845x device supports.
                The default value for the port number is 0.
        :return: None
        """
        returnvalue = self.ni8452.ni845xI2cConfigurationSetPort(self.configuration_handle, c.c_uint8(port))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)

    def ni845xI2cConfigurationGetPort(self):
        """
        Calls the NI USB-8452 C API function ni845xI2cConfigurationGetPort whose prototype is
        int32 ni845xI2cConfigurationGetPort (NiHandle ConfigurationHandle,uInt8 * pPort);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xI2cConfigurationOpen.
        :return: uInt8 * pPort:
            A pointer to an unsigned byte to store the port value in.
        """
        getport = c.c_uint8()
        returnvalue = self.ni8452.ni845xI2cConfigurationGetPort(self.configuration_handle, c.byref(getport))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)
        return getport

    #############################################################
    # Basic
    #############################################################

    def ni845xI2cWrite(self, writesize=0, writedata=0):
        """
        Calls the NI USB-8452 C API function ni845xI2cConfigurationSetPort whose prototype is
        int32 ni845xI2cWrite (NiHandle DeviceHandle,
                              NiHandle ConfigurationHandle,
                              uInt32 WriteSize,
                              uInt8 * pWriteData);
        :param: NiHandle DeviceHandle: Device handle returned from ni845xOpen.
                NiHandle ConfigurationHandle: The configuration handle returned from ni845xI2cConfigurationOpen.
                uInt32 WriteSize: The number of bytes to write. This must be nonzero.
                uInt8 * pWriteData: The data bytes to be written.

        :return: None   Use ni845xI2cWrite to write an array of data to an I2C slave device. This function first
                        waits for the I2C bus to be free. If the I2C bus is not free within the one second timeout of
                        your NI 845x device, an error is returned. If the bus is free before the timeout, the NI 845x
                        device executes a 7-bit or 10-bit I2C write transaction, per the NXP I2C specification.
                        The address type (7-bit or 10-bit) and other configuration parameters are specified by ConfigurationHandle.
                        If the NI 845x device tries to access the bus at the same time as
                        another I2C master device and loses arbitration, the write transaction is terminated and an
                        error is returned. If the slave device does not acknowledge the address, the NI 845x device
                        ACK polls as specified by ConfigurationHandle. (Refer to the I2C ACK Polling section
                        in Chapter 1, Introduction, for more information about ACK polling.)
                        If the slave device does not acknowledge any transaction byte, an error is returned. Otherwise, the transaction is
                        completed, and a stop condition is generated per the NXP I2C specification.

        """
        Writedata = (c.c_uint8 * writesize)(*writedata)
        returnvalue = self.ni8452.ni845xI2cWrite(self.device_handle, self.configuration_handle,
                                                 c.c_uint32(writesize),
                                                 c.byref(Writedata)
                                                 )
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)
            self.status = returnvalue
        Writedata = [i for i in Writedata]
        return Writedata

    def ni845xI2cRead(self, noofbytestoread=0):
        """
        Calls the NI USB-8452 C API function ni845xI2cConfigurationSetPort whose prototype is
        int32 ni845xI2cRead (NiHandle DeviceHandle,
                             NiHandle ConfigurationHandle,
                             uInt32 NumBytesToRead,
                             uInt32 * pReadSize,
                             uInt8 * pReadData
                             );
        :param: NiHandle DeviceHandle: Device handle returned from ni845xOpen.
                NiHandle ConfigurationHandle: The configuration handle returned from ni845xI2cConfigurationOpen.
                uInt32 NumBytesToRead: The number of bytes to read. This must be nonzero.
                uInt32 * pReadSize: A pointer to the amount of bytes read.
                uInt8 * pReadData: A pointer to an array of bytes where the bytes that have been read are stored.

        :return: None   Use ni845xI2cRead to read an array of data from an I2C slave device. Per the NXP I2C
                        specification, each byte read up to the last byte is acknowledged. The last byte is not
                        acknowledged. This function first waits for the I2C bus to be free. If the I2C bus is not free
                        within the one second timeout of your NI 845x device, an error is returned. If the bus is free
                        before the timeout, the NI 845x device executes a 7-bit or 10-bit I2C read transaction, per the NXP I2C specification.
                        The address type (7-bit or 10-bit) and other configuration parameters
                        are specified by ConfigurationHandle. If the NI 845x device tries to access the bus at the
                        same time as another I2C master device and loses arbitration, the read transaction is terminated and an error is returned.
                        If the slave device does not acknowledge the transaction address, the NI 845x device ACK polls as specified by ConfigurationHandle.
                        (Refer to the I2C ACK Polling section in Chapter 1, Introduction, for more information about ACK polling.)
                        Otherwise, the transaction is completed, and a stop condition is generated per the NXP I2C specification.

        """
        readsize = c.c_uint32()
        readdata = list()
        Readdata = (c.c_uint8 * noofbytestoread)(*readdata)
        returnvalue = self.ni8452.ni845xI2cRead(self.device_handle, self.configuration_handle,
                                                c.c_uint32(noofbytestoread),
                                                c.byref(readsize),
                                                c.byref(Readdata)
                                                )
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)
            self.status = returnvalue
        Readdata = [i for i in Readdata]
        return Readdata

    def ni845xI2cWriteRead(self, writesize=0, writedata=0, noofbytestoread=0):
        """
        Calls the NI USB-8452 C API function ni845xI2cConfigurationSetPort whose prototype is
        int32 ni845xI2cWriteRead (NiHandle DeviceHandle,
                                  NiHandle ConfigurationHandle,
                                  uInt32 WriteSize,
                                  uInt8 * pWriteData,
                                  uInt32 NumBytesToRead,
                                  uInt32 * pReadSize,
                                  uInt8 * pReadData
                                  );
        :param: NiHandle DeviceHandle: Device handle returned from ni845xOpen.
                NiHandle ConfigurationHandle: The configuration handle returned from ni845xI2cConfigurationOpen.
                uInt32 WriteSize: The number of bytes to write. This must be nonzero.
                uInt8 * pWriteData: The data bytes to be written.
                uInt32 NumBytesToRead: An unsigned 32-bit integer corresponding to the number of bytes to read. This must be nonzero.
                uInt32 * pReadSize: A pointer to the amount of bytes read.
                uInt8 * pReadData: A pointer to an array of bytes where the bytes that have been read are stored.
        :return: None   Use ni845xI2cWriteRead to perform a write followed by read (combined format) on an
                        I2C slave device. During the transaction read portion, per the NXP I2C specification, each byte
                        read up to the last byte is acknowledged. The last byte is not acknowledged. This function
                        first waits for the I2C bus to be free. If the I2C bus is not free within the one second timeout
                        of your NI 845x device, an error is returned. If the bus is free before the timeout, the
                        NI 845x device executes a 7-bit or 10-bit I2C write/read transaction. Per the NXP I2C
                        specification, the write/read transaction consists of a start-write-restart-read-stop sequence.
                        The address type (7-bit or 10-bit) and other configuration parameters are specified by
                        ConfigurationHandle. If the NI 845x device tries to access the bus at the same time as
                        another I2C master device and loses arbitration, the read transaction is terminated and an error is returned.
                        If the slave device does not acknowledge the write address, the NI 845x device
                        ACK polls as specified by ConfigurationHandle. (Refer to the I2C ACK Polling section
                        in Chapter 1, Introduction, for more information about ACK polling.) If the slave device does
                        not acknowledge the read address or byte write within the transaction, an error is returned.
                        Otherwise, the transaction is completed and a stop condition is generated per the NXP I2C
                        specification. Note that this type of combined transaction is provided because it is commonly used (for example, with EEPROMs).
                        The NXP I2C specification provides flexibility in the construction of I2C transactions.
                        The NI-845x I2C scripting functions allow creating and customizing complex I2C transactions as needed.
        """
        readsize = c.c_uint32()
        readdata = list()
        Writedata = (c.c_uint8 * writesize)(*writedata)
        Readdata = (c.c_uint8 * noofbytestoread)(*readdata)
        returnvalue = self.ni8452.ni845xI2cWriteRead(self.device_handle, self.configuration_handle,
                                                    c.c_uint32(writesize),
                                                    c.byref(Writedata),
                                                    c.c_uint32(noofbytestoread),
                                                    c.byref(readsize),
                                                    c.byref(Readdata)
                                                    )
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)
            self.status = returnvalue
        Writedata, Readdata = [i for i in Writedata], [j for j in Readdata]
        return Readdata
