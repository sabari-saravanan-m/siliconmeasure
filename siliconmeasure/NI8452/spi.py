"""
Author                          : SABARI SARAVANAN M
Developed Tool and Version      : Python 3.9
Description                     : General SPI-API functions for NI8452
Module Name                     : NIUSB-8452 SPI Interface
Module Version                  : 0.0.1
Created                         : January 2021

"""
import ctypes as c                                              # It provides C compatible data types, and allows calling functions in DLLs or shared libraries.
from NI8452.general import General                              # Importing main class

class SPI(General):
    """
     This class makes Python calls to the C DLL of NI USB 8452 (ni845x.dll).
     Use this following example line with SPI device.

        ni845xSpiConfigurationOpen()                            # Create a new configuration reference to use with the NI-8452 SPI Basic API

        ni845xSpiConfigurationSetChipSelect(0)                  # Select the chip select where the SPI slave device resides
        ni845xSpiConfigurationSetClockPhase(0)                  # Sets the value of the clock phase that ConfigurationHandle uses
        ni845xSpiConfigurationSetClockPolarity(0)               # Sets the clock polarity to use when communicating with the SPI slave device
        ni845xSpiConfigurationSetClockRate(25000)               # Sets the SPI configuration clock rate in kilohertz
        ni845xSpiConfigurationSetNumBitsPerSample(16)           # Sets the number of bits per sample for an SPI transmission
        ni845xSpiWriteRead(2, [0xaa,0xaa], 2)                   # Exchanges an array of data with an SPI slave device

        ni845xSpiConfigurationClose()                           # Close configuration reference with the NI-8452 SPI Basic API

    """

    def __init__(self):
        super(SPI, self).__init__()                             # Invoking the main(General) class
        self.status = 0

    #############################################################
    # Configuration
    #############################################################

    def ni845xSpiConfigurationOpen(self):
        """
        Calls the NI USB-8452 C API function ni845xSpiConfigurationOpen whose prototype is
        int32 ni845xSpiConfigurationOpen (NiHandle * pConfigurationHandle);
        :param: None
        :return: configuration handle
        """

        returnvalue = self.ni8452.ni845xSpiConfigurationOpen(c.byref(self.configuration_handle))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)

    def ni845xSpiConfigurationClose(self):
        """
        Calls the NI USB-8452 C API function ni845xSpiConfigurationClose whose prototype is
        int32 ni845xSpiConfigurationClose (NiHandle ConfigurationHandle);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xSpiConfigurationOpen.
        :return: None
        """
        returnvalue = self.ni8452.ni845xSpiConfigurationClose(self.configuration_handle)
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)
        return (f"Device #: {str(self.first_device.value)} configuration has been closed succesfully.")

    def ni845xSpiConfigurationSetChipSelect(self, chipselect=0):
        """
        Calls the NI USB-8452 C API function ni845xSpiConfigurationSetChipSelect whose prototype is
        int32 ni845xSpiConfigurationSetChipSelect (NiHandle ConfigurationHandle,uInt32 ChipSelect);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xSpiConfigurationOpen.
                uInt32 ChipSelect: Selects the chip select line for this configuration.
                The default value for the chip select is 0.
        :return: None
        """
        returnvalue = self.ni8452.ni845xSpiConfigurationSetChipSelect(self.configuration_handle, c.c_uint32(chipselect))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)

    def ni845xSpiConfigurationGetChipSelect(self):
        """
        Calls the NI USB-8452 C API function  whose prototype is
        int32 ni845xSpiConfigurationGetChipSelect (NiHandle ConfigurationHandle,uInt32 * pChipSelect);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xSpiConfigurationOpen.
        :return: None
        """
        chipselect = c.c_uint32()
        returnvalue = self.ni8452.ni845xSpiConfigurationGetChipSelect(self.configuration_handle, c.byref(chipselect))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)
        return chipselect

    def ni845xSpiConfigurationSetClockPhase(self, clockphase=0):
        """
        Calls the NI USB-8452 C API function ni845xSpiConfigurationSetClockPhase whose prototype is
        int32 ni845xSpiConfigurationSetClockPhase (NiHandle ConfigurationHandle,int32 ClockPhase);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xSpiConfigurationOpen.
        int32 ClockPhase:Sets the positioning of the data bits relative to the clock edges for the SPI Port.
            ClockPhase uses the following values:
                • kNi845xSpiClockPhaseFirstEdge (0): Data is centered on the first edge of the clock period.
                • kNi845xSpiClockPhaseSecondEdge (1): Data is centered on the second edge of the clock period.
        The default value for this property is kNi845xSpiClockPhaseFirstEdge.
        :return: None
        """
        returnvalue = self.ni8452.ni845xSpiConfigurationSetClockPhase(self.configuration_handle, c.c_uint32(clockphase))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)

    def ni845xSpiConfigurationGetClockPhase(self):
        """
        Calls the NI USB-8452 C API function ni845xSpiConfigurationGetClockPhase whose prototype is
        int32 ni845xSpiConfigurationGetClockPhase (NiHandle ConfigurationHandle,int32 * pClockPhase);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xSpiConfigurationOpen.
        :return: int32 * pClockPhase:
            A pointer to an integer to store the clock phase in. pClockPhase uses the followingvalues:
                • kNi845xSpiClockPhaseFirstEdge (0): Data is centered on the first edge of theclock period.
                • kNi845xSpiClockPhaseSecondEdge (1): Data is centered on the second edge ofthe clock period.
        """
        clockphase = c.c_uint32()
        returnvalue = self.ni8452.ni845xSpiConfigurationGetClockPhase(self.configuration_handle, c.byref(clockphase))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)
        return clockphase

    def ni845xSpiConfigurationSetClockPolarity(self, clockpolarity=0):
        """
        Calls the NI USB-8452 C API function ni845xSpiConfigurationSetClockPolarity whose prototype is
        int32 ni845xSpiConfigurationSetClockPolarity (NiHandle ConfigurationHandle,int32 ClockPolarity);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xSpiConfigurationOpen.
         int32 ClockPolarity: Sets the clock line idle state for the SPI Port.
            ClockPolarity uses the following values:
                    • kNi845xSpiClockPolarityIdleLow (0): Clock is low in the idle state.
                    • kNi845xSpiClockPolarityIdleHigh (1): Clock is high in the idle state.
        The default value for this property is kNi845xSpiClockPolarityIdleLow.
        :return: None
        """
        returnvalue = self.ni8452.ni845xSpiConfigurationSetClockPolarity(self.configuration_handle, c.c_uint32(clockpolarity))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)

    def ni845xSpiConfigurationGetClockPolarity(self):
        """
        Calls the NI USB-8452 C API function ni845xSpiConfigurationGetClockPolarity whose prototype is
        int32 ni845xSpiConfigurationGetClockPolarity (NiHandle ConfigurationHandle,int32 * pClockPolarity);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xSpiConfigurationOpen.
        :return: int32 * pClockPolarity:
            A pointer to an integer to store the clock polarity in. pClockPolarity uses thefollowing values:
                • kNi845xSpiClockPolarityIdleLow (0): Clock is low in the idle state.
                • kNi845xSpiClockPolarityIdleHigh (1): Clock is high in the idle state.
        """
        clockpolarity = c.c_uint32()
        returnvalue = self.ni8452.ni845xSpiConfigurationGetClockPolarity(self.configuration_handle, c.byref(clockpolarity))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)
        return clockpolarity

    def ni845xSpiConfigurationSetClockRate(self, clockrate=1000):
        """
        Calls the NI USB-8452 C API function ni845xSpiConfigurationSetClockRate whose prototype is
        int32 ni845xSpiConfigurationSetClockRate (NiHandle ConfigurationHandle,uInt16 ClockRate);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xSpiConfigurationOpen.
            uInt16 ClockRate: Specifies the SPI clock rate. Refer to Chapter 3, NI USB-845x Hardware Overview, to
                    determine which clock rates your NI 845x device supports. If your hardware does not
                    support the supplied clock rate, a warning is generated, and the next smallest supported
                    clock rate is used.
                    If the supplied clock rate is smaller than the smallest supported clock rate, an error is
                    generated. The configuration does not validate the clock rate until it is committed to hardware.
            The default value for the clock rate is 1000 kHz (1 MHz).
        :return: None
        """
        returnvalue = self.ni8452.ni845xSpiConfigurationSetClockRate(self.configuration_handle, c.c_uint16(clockrate))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)

    def ni845xSpiConfigurationGetClockRate(self):
        """
        Calls the NI USB-8452 C API function ni845xSpiConfigurationGetClockRate whose prototype is
        int32 ni845xSpiConfigurationGetClockRate (NiHandle ConfigurationHandle,uInt16 * pClockRate);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xSpiConfigurationOpen.
        :return: uInt16 * pClockRate:
            A pointer to an unsigned 16-bit integer to store the clock rate in.
        """
        clockrate = c.c_uint16()
        returnvalue = self.ni8452.ni845xSpiConfigurationGetClockRate(self.configuration_handle, c.byref(clockrate))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)
        return clockrate

    def ni845xSpiConfigurationSetNumBitsPerSample(self, numbitspersample=8):
        """
        Calls the NI USB-8452 C API function ni845xSpiConfigurationSetNumBitsPerSample whose prototype is
        int32 ni845xSpiConfigurationSetNumBitsPerSample (NiHandle ConfigurationHandle,uInt16 NumBitsPerSample);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xSpiConfigurationOpen.
            uInt16 NumBitsPerSample: Specifies the number of bits per sample to be used for SPI transmissions.
                    The default value for the number of bits per sample is 8.
                    Refer to Appendix A, NI USB-845x Hardware Specifications, for valid settings for this property.
        :return: None
        """
        returnvalue = self.ni8452.ni845xSpiConfigurationSetNumBitsPerSample(self.configuration_handle, c.c_uint16(numbitspersample))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)

    def ni845xSpiConfigurationGetNumBitsPerSample(self):
        """
        Calls the NI USB-8452 C API function ni845xSpiConfigurationGetNumBitsPerSample whose prototype is
        int32 ni845xSpiConfigurationGetNumBitsPerSample (NiHandle ConfigurationHandle,uInt16 * pNumBitsPerSample);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xSpiConfigurationOpen.
        :return: uInt16 * pNumBitsPerSample:
            A pointer to an unsigned 16-bit integer to store the number of bits per sample in.
        """
        numbitspersample = c.c_uint16()
        returnvalue = self.ni8452.ni845xSpiConfigurationGetNumBitsPerSample(self.configuration_handle, c.byref(numbitspersample))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)
        return numbitspersample

    def ni845xSpiConfigurationSetPort(self, port=0):
        """
        Calls the NI USB-8452 C API function ni845xSpiConfigurationSetPort whose prototype is
        int32 ni845xSpiConfigurationSetPort (NiHandle ConfigurationHandle,uInt8 Port);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xSpiConfigurationOpen.
            uInt8 Port: Specifies the SPI port that this configuration communicates across.
                Refer to Chapter 3, NI USB-845x Hardware Overview, to determine the number of SPI
                ports your NI 845x device supports.
                The default value for the port number is 0.
        :return: None
        """
        returnvalue = self.ni8452.ni845xSpiConfigurationSetPort(self.configuration_handle, c.c_uint8(port))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)

    def ni845xSpiConfigurationGetPort(self):
        """
        Calls the NI USB-8452 C API function ni845xSpiConfigurationGetPort whose prototype is
        int32 ni845xSpiConfigurationGetPort (NiHandle ConfigurationHandle,uInt8 * pPort);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xSpiConfigurationOpen.
        :return: uInt8 * pPort:
            A pointer to an unsigned byte to store the port value in.
        """
        getport = c.c_uint8()
        returnvalue = self.ni8452.ni845xSpiConfigurationGetPort(self.configuration_handle, c.byref(getport))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)
        return getport

    #############################################################
    # Basic
    #############################################################

    def ni845xSpiWriteRead(self, writesize=0, writedata=0, readsize = 0):
        """
        Calls the NI USB-8452 C API function ni845xSpiConfigurationSetPort whose prototype is
        int32 ni845xSpiWriteRead (NiHandle DeviceHandle,
                                  NiHandle ConfigurationHandle,
                                  uInt32 WriteSize,
                                  uInt8 * pWriteData,
                                  uInt32 * pReadSize,
                                  uInt8 * pReadData);
        :param: NiHandle DeviceHandle: Device handle returned from ni845xOpen.
                NiHandle ConfigurationHandle: The configuration handle returned from ni845xSpiConfigurationOpen.
                uInt32 WriteSize: The number of bytes to write. This must be nonzero.
                uInt8 * pWriteData: The data bytes to be written.
        :return: None
        """
        readdata = list()
        Writedata = (c.c_uint8 * writesize)(*writedata)
        Readdata = (c.c_uint8 * readsize)(*readdata)
        returnvalue = self.ni8452.ni845xSpiWriteRead(self.device_handle, self.configuration_handle,
                                                    c.c_uint32(writesize),
                                                    c.byref(Writedata),
                                                    c.byref(c.c_uint32(readsize)),
                                                    c.byref(Readdata)
                                                    )
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)
            self.status = returnvalue
        Writedata, readdataandSize = [i for i in Writedata], [[j for j in Readdata], len(Readdata)]
        return readdataandSize
