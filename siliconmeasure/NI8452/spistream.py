"""
Author                          : SABARI SARAVANAN M
Developed Tool and Version      : Python 3.9
Description                     : General SPI Scripting -API functions for NI8452
Module Name                     : NIUSB-8452 SPI Scripting Interface
Module Version                  : 0.0.1
Created                         : March 2021

"""
import ctypes as c                                              # It provides C compatible data types, and allows calling functions in DLLs or shared libraries.
from NI8452.general import General                              # Importing main class

class SPIStream(General):
    """
     This class makes Python calls to the C DLL of NI USB 8452 (ni845x.dll).
     Use this following example line with SPI device.

        ni845xSpiScriptOpen()                                   # Create a new configuration reference to use with the NI-8452 SPI Basic API

        ni845xSpiConfigurationSetChipSelect(0)                  # Select the chip select where the SPI slave device resides
        ni845xSpiConfigurationSetClockPhase(0)                  # Sets the value of the clock phase that ConfigurationHandle uses
        ni845xSpiConfigurationSetClockPolarity(0)               # Sets the clock polarity to use when communicating with the SPI slave device
        ni845xSpiConfigurationSetClockRate(25000)               # Sets the SPI configuration clock rate in kilohertz
        ni845xSpiConfigurationSetNumBitsPerSample(16)           # Sets the number of bits per sample for an SPI transmission
        ni845xSpiWriteRead(2, [0xaa,0xaa], 2)                   # Exchanges an array of data with an SPI slave device

        ni845xSpiConfigurationClose()                           # Close configuration reference with the NI-8452 SPI Basic API

    """

    def __init__(self):
        super(SPIStream, self).__init__()                       # Invoking the main(General) class
        self.status = 0

    #############################################################
    # Configuration
    #############################################################

    def ni845xSpiStreamConfigurationOpen(self):
        """
        Calls the NI USB-8452 C API function ni845xSpiStreamConfigurationOpen whose prototype is
        int32 ni845xSpiStreamConfigurationOpen (NiHandle * pConfigurationHandle);
        :param: None
        :return: configuration handle
        """

        returnvalue = self.ni8452.ni845xSpiStreamConfigurationOpen(c.byref(self.configuration_handle))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)
        else:
            return (f"Device #: {str(self.first_device.value)} configuration has been closed succesfully.")

    def ni845xSpiStreamConfigurationClose(self):
        """
        Calls the NI USB-8452 C API function ni845xSpiStreamConfigurationClose whose prototype is
        int32 ni845xSpiStreamConfigurationClose (NiHandle ConfigurationHandle);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xSpiStreamConfigurationOpen.
        :return: None
        """
        returnvalue = self.ni8452.ni845xSpiStreamConfigurationClose(self.configuration_handle)
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)
        else:
            return (f"Device #: {str(self.first_device.value)} configuration has been closed succesfully.")

    def ni845xSpiStreamConfigurationSetNumBits(self, numbits=0):
        """
        Calls the NI USB-8452 C API function ni845xSpiStreamConfigurationSetNumBits whose prototype is
        int32 ni845xSpiStreamConfigurationSetNumBits (NiHandle ConfigurationHandle,uInt8 NumBits);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xSpiStreamConfigurationOpen.
                uInt8 NumBits: An unsigned 8-bit integer that contains the number of bits per sample.
        :return: None
        """

        returnvalue = self.ni8452.ni845xSpiStreamConfigurationSetNumBits(self.configuration_handle, c.c_uint8(numbits))
        if returnvalue != 0: self.ni845xStatusToString(returnvalue)

    def ni845xSpiStreamConfigurationSetNumSamples(self, numsamples=0):
        """
        Calls the NI USB-8452 C API function ni845xSpiStreamConfigurationSetNumSamples whose prototype is
        int32 ni845xSpiStreamConfigurationSetNumSamples (NiHandle ConfigurationHandle,uInt32 NumSamples);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xSpiStreamConfigurationOpen.
                uInt32 NumSamples: An unsigned 32-bit integer to set the number of samples to stream.
        :return: None
        """

        returnvalue = self.ni8452.ni845xSpiStreamConfigurationSetNumSamples(self.configuration_handle, c.c_uint32(numsamples))
        if returnvalue != 0: self.ni845xStatusToString(returnvalue)

    def ni845xSpiStreamConfigurationSetNumSamples(self, numsamples=0):
        """
        Calls the NI USB-8452 C API function ni845xSpiStreamConfigurationSetNumSamples whose prototype is
        int32 ni845xSpiStreamConfigurationSetNumSamples (NiHandle ConfigurationHandle,uInt32 NumSamples);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xSpiStreamConfigurationOpen.
                uInt32 NumSamples: An unsigned 32-bit integer to set the number of samples to stream.
        :return: None
        """

        returnvalue = self.ni8452.ni845xSpiStreamConfigurationSetNumSamples(self.configuration_handle, c.c_uint32(numsamples))
        if returnvalue != 0: self.ni845xStatusToString(returnvalue)

    def ni845xSpiStreamConfigurationSetClockPhase(self, clockphase=0):
        """
        Calls the NI USB-8452 C API function ni845xSpiStreamConfigurationSetClockPhase whose prototype is
        int32 ni845xSpiStreamConfigurationSetClockPhase (NiHandle ConfigurationHandle,uInt8 ClockPhase);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xSpiStreamConfigurationOpen.
        int32 ClockPhase:Sets the positioning of the data bits relative to the clock edges for the SPI Port.
            ClockPhase uses the following values:
                • kNi845xSpiStreamClockPhaseFirstEdge (0): Data is updated on the first edge of the clock period.
                • kNi845xSpiStreamClockPhaseSecondEdge (1): Data is updated on the second edge of the clock period.
        The default value for this property is kNi845xSpiClockPhaseFirstEdge.
        :return: None
        """
        returnvalue = self.ni8452.ni845xSpiStreamConfigurationSetClockPhase(self.configuration_handle, c.c_uint8(clockphase))
        if returnvalue != 0: self.ni845xStatusToString(returnvalue)

    def ni845xSpiStreamConfigurationSetClockPolarity(self, clockpolarity=0):
        """
        Calls the NI USB-8452 C API function ni845xSpiStreamConfigurationSetClockPolarity whose prototype is
        int32 ni845xSpiStreamConfigurationSetClockPolarity (NiHandle ConfigurationHandle,uInt8 ClockPolarity);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xSpiStreamConfigurationOpen.
         int32 ClockPolarity: Sets the clock line idle state for the SPI Port.
            ClockPolarity uses the following values:
                    • kNi845xSpiStreamClockPolarityIdleLow (0): Clock is low in the idle state.
                    • kNi845xSpiStreamClockPolarityIdleHigh (1): Clock is high in the idle state.
        The default value for this property is kNi845xSpiClockPolarityIdleLow.
        :return: None
        """
        returnvalue = self.ni8452.ni845xSpiStreamConfigurationSetClockPolarity(self.configuration_handle, c.c_uint8(clockpolarity))
        if returnvalue != 0: self.ni845xStatusToString(returnvalue)

    def ni845xSpiStreamConfigurationWave1SetTimingParam(self, timingparameter=0, ParameterValue =0):
        """
        Calls the NI USB-8452 C API function ni845xSpiStreamConfigurationWave1SetTimingParam whose prototype is
        int32 ni845xSpiStreamConfigurationWave1SetTimingParam (NiHandle ConfigurationHandle,uInt8 TimingParameter,uInt32 ParameterValue);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xSpiStreamConfigurationOpen.
                uInt8 TimingParameter: An unsigned 8-bit integer to determine the timing parameter uses the following values:
                    • kNi845xSpiStreamWave1SclkL (0): SCLK low period for Waveform 1.
                    • kNi845xSpiStreamWave1SclkH (1): SCLK high period for Waveform 1.
                    • kNi845xSpiStreamWave1T1 (2): Timing Parameter T1—CONV assert to CONV deassert for Waveform 1.
                    • kNi845xSpiStreamWave1T2 (3): Timing Parameter T2—CONV deassert to Chip Select assert for Waveform 1.
                    • kNi845xSpiStreamWave1T3 (4): Timing Parameter T3—CONV deassert to SCLK assert (first bit) for Waveform 1.
                    • kNi845xSpiStreamWave1T4 (5): Timing Parameter T4—DRDY assert to Chip Select assert for Waveform 1.
                    • kNi845xSpiStreamWave1T5 (6): Timing Parameter T5—DRDY assert to SCLK assert (first bit) for Waveform 1.
                    • kNi845xSpiStreamWave1T6 (7): Timing Parameter T6—DRDY deassert to CONV assert for Waveform 1.
                    • kNi845xSpiStreamWave1T7 (8): Timing Parameter T7—Chip Select assert to SCLK assert (first bit) for Waveform 1.
                    • kNi845xSpiStreamWave1T8 (9): Timing Parameter T8—Chip Select deassert to CONV assert for Waveform 1.
                    • kNi845xSpiStreamWave1T9 (10): Timing Parameter T9—Chip Select deassert to Chip Select assert.
                    • kNi845xSpiStreamWave1T10 (11): Timing Parameter T10—SCLK deassert (last bit) to CONV assert for Waveform 1.
                    • kNi845xSpiStreamWave1T11 (12): Timing Parameter T11—SCLK deassert (last bit) to Chip Select deassert for Waveform 1.
                    • kNi845xSpiStreamWave1T12 (13): Timing Parameter T12—SCLK deassert (last bit) to SCLK assert (first bit) for Waveform 1.
                uInt32 ParameterValue: A 32-bit unsigned integer to set the timing parameter in system clocks.
        :return: None
        """
        returnvalue = self.ni8452.ni845xSpiStreamConfigurationWave1SetTimingParam(self.configuration_handle,
                                                                                  c.c_uint8(timingparameter),
                                                                                  c.c_uint32(ParameterValue))
        if returnvalue != 0: self.ni845xStatusToString(returnvalue)

    def ni845xSpiStreamConfigurationWave1SetMosiData(self, dataarray=[], arraysize=0):
        """
        Calls the NI USB-8452 C API function ni845xSpiStreamConfigurationWave1SetMosiData whose prototype is
        int32 ni845xSpiStreamConfigurationWave1SetMosiData (NiHandle ConfigurationHandle,uInt8 * DataArray,uInt32 ArraySize);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xSpiStreamConfigurationOpen.
                uInt8* DataArray: An array of unsigned 8-bit integers used to specify the data transferred on MOSI.
                                  The data must be organized in big endian format.
        :return: None
        """
        returnvalue = self.ni8452.ni845xSpiStreamConfigurationWave1SetMosiData(self.configuration_handle,
                                                                               ((c.c_uint8 * arraysize)(*dataarray)),
                                                                               c.c_uint32(arraysize))
        if returnvalue != 0: self.ni845xStatusToString(returnvalue)

    def ni845xSpiStreamConfigurationWave1SetPinConfig(self, pinnumber=0, mode=0):
        """
        Calls the NI USB-8452 C API function ni845xSpiStreamConfigurationWave1SetPinConfig whose prototype is
        int32 ni845xSpiStreamConfigurationWave1SetPinConfig (NiHandle ConfigurationHandle,uInt8 PinNumber,uInt8 Mode);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xSpiStreamConfigurationOpen.
                uInt8 PinNumber: An unsigned 8-bit integer to determine the pin uses the following values:
                    • kNi845xSpiStreamWave1ConvPin (0): CONV output for Waveform 1.
                    • kNi845xSpiStreamWave1DrdyPin (1): DRDY input for Waveform 1.
                    • kNi845xSpiStreamWave1CsPin (2): Chip Select output for Waveform 1.
                uInt8 Mode: An 8-bit unsigned integer to set the pin mode that uses the following values:
                    • kNi845xSpiStreamDisabled (0): Pin is disabled.
                    • kNi845xSpiStreamActiveHigh (1): Pin is set to active high.
                    • kNi845xSpiStreamActiveLow (2): Pin is set to active low.
                    • kNi845xSpiStreamDriveHigh (3): Pin driven high.
                    • kNi845xSpiStreamDriveLow (4): Pin driven low.
        :return: None
        """
        returnvalue = self.ni8452.ni845xSpiStreamConfigurationWave1SetPinConfig(self.configuration_handle,
                                                                                c.c_uint8(pinnumber), c.c_uint8(mode))
        if returnvalue != 0: self.ni845xStatusToString(returnvalue)

    def ni845xSpiStreamConfigurationSetPacketSize(self, packetsize=0):
        """
        Calls the NI USB-8452 C API function ni845xSpiStreamConfigurationSetPacketSize whose prototype is
        int32 ni845xSpiStreamConfigurationSetPacketSize (NiHandle ConfigurationHandle,uInt32 PacketSize);
        :param: NiHandle ConfigurationHandle: The configuration handle returned from ni845xSpiStreamConfigurationOpen.
                uInt32 PacketSize: An unsigned 32-bit integer to set the packet size.

                This parameter should be set to a multiple of 512 bytes for optimal performance.
                This setting can affect the performance of data streaming to the host from your NI 845x device.
        :return: None
        """
        returnvalue = self.ni8452.ni845xSpiStreamConfigurationSetPacketSize(self.configuration_handle, c.c_uint32(packetsize))
        if returnvalue != 0: self.ni845xStatusToString(returnvalue)

    #############################################################
    # Streaming
    #############################################################

    def ni845xSpiStreamRead(self, numbytestoread=0):
        """
        Calls the NI USB-8452 C API function ni845xSpiStreamRead whose prototype is
        int32 ni845xSpiStreamRead (NiHandle DeviceHandle,
                                   NiHandle ConfigurationHandle,
                                   uint32 NumBytesToRead,
                                   uInt8 * ReadData,
                                   uInt32 * ReadSize
                                   );
        :param: NiHandle DeviceHandle: Device handle returned from ni845xOpen.
                NiHandle ConfigurationHandle: The configuration handle returned from ni845xSpiStreamConfigurationOpen.
                uInt32 NumBytesToRead: The number of bytes to read. This number must be nonzero.
                                       ReadData must be large enough to read the requested number of bytes.
        :return: uInt8 * ReadData: A pointer to an array of bytes where the bytes that have been read are stored.
                 uInt32 * ReadSize: A pointer to the amount of bytes actually read.
        """
        readdata = list()
        readdata = (c.c_uint8 * numbytestoread)(*readdata)
        readsize = c.c_uint32()
        returnvalue = self.ni8452.ni845xSpiStreamRead(self.device_handle, self.configuration_handle,
                                                      c.c_uint32(numbytestoread), c.byref(readdata),
                                                      c.byref(readsize))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)
        else:
            readdata = [i for i in readdata]
            return readdata

    def ni845xSpiStreamStart(self, numbytestoread=0):
        """
        Calls the NI USB-8452 C API function ni845xSpiStreamStart whose prototype is
        int32 ni845xSpiStreamStart (NiHandle DeviceHandle,NiHandle ConfigurationHandle);
        :param: NiHandle DeviceHandle: Device handle returned from ni845xOpen.
                NiHandle ConfigurationHandle: The configuration handle returned from ni845xSpiStreamConfigurationOpen.

        :return: None
        """
        returnvalue = self.ni8452.ni845xSpiStreamStart(self.device_handle, self.configuration_handle)
        if returnvalue != 0: self.ni845xStatusToString(returnvalue)

    def ni845xSpiStreamStop(self, numbytestoread=0):
        """
        Calls the NI USB-8452 C API function ni845xSpiStreamStop whose prototype is
        int32 ni845xSpiStreamStop (NiHandle DeviceHandle,NiHandle ConfigurationHandle);
        :param: NiHandle DeviceHandle: Device handle returned from ni845xOpen.
                NiHandle ConfigurationHandle: The configuration handle returned from ni845xSpiStreamConfigurationOpen.

        :return: None
        """
        returnvalue = self.ni8452.ni845xSpiStreamStop(self.device_handle, self.configuration_handle)
        if returnvalue != 0: self.ni845xStatusToString(returnvalue)
