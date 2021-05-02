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

class SPIScript(General):
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
        super(SPIScript, self).__init__()                       # Invoking the main(General) class
        self.status = 0

    #############################################################
    # Scripting
    #############################################################

    def ni845xSpiScriptOpen(self):
        """
        Calls the NI USB-8452 C API function ni845xSpiScriptOpen whose prototype is
        int32 ni845xSpiScriptOpen (NiHandle ScriptHandle);
        :param: None
        :return: Script handle
        """

        returnvalue = self.ni8452.ni845xSpiScriptOpen(c.byref(self.script_handle))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)
        else:
            return (f"Device #: {str(self.first_device.value)} SPI script opened succesfully.")

    def ni845xSpiScriptClose(self):
        """
        Calls the NI USB-8452 C API function ni845xSpiScriptClose whose prototype is
        int32 ni845xSpiScriptClose (NiHandle ScriptHandle);
        :param: NiHandle ScriptHandle: The script handle returned from ni845xSpiScriptOpen.
        :return: None
        """
        returnvalue = self.ni8452.ni845xSpiScriptClose(self.script_handle)
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)
        else:
            return (f"Device #: {str(self.first_device.value)} SPI script closed succesfully.")

    def ni845xSpiScriptClockPolarityPhase(self, clockpolarity=0, clockphase=0):
        """
        Calls the NI USB-8452 C API function ni845xSpiScriptClockPolarityPhase whose prototype is
        int32 ni845xSpiScriptClockPolarityPhase (NiHandle ScriptHandle,int32 Polarity,int32 Phase);
        :param: NiHandle ScriptHandle: The script handle returned from ni845xSpiScriptOpen.
                int32 Polarity: The clock line idle state for the SPI Port.
                    Polarity uses the following values:
                        • kNi845xSpiClockPolarityIdleLow (0): Clock is low in the idle state.
                        • kNi845xSpiClockPolarityIdleHigh (1): Clock is high in the idle state.
                int32 Phase: The positioning of the data bits relative to the clock edges for the SPI Port.
                    Phase uses the following values:
                        • kNi845xSpiClockPhaseFirstEdge (0): Data is centered on the first edge of the clock period.
                        • kNi845xSpiClockPhaseSecondEdge (1): Data is centered on the second edge of the clock period.
        The default value for this property is kNi845xSpiClockPolarityIdleLow & kNi845xSpiClockPhaseFirstEdge.
        :return: None
        """
        returnvalue = self.ni8452.ni845xSpiScriptClockPolarityPhase(self.script_handle, c.c_uint32(clockpolarity), c.c_uint32(clockphase))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)

    def ni845xSpiScriptClockRate(self, clockrate=1000):
        """
        Calls the NI USB-8452 C API function ni845xSpiConfigurationSetClockRate whose prototype is
        int32 ni845xSpiScriptClockRate (NiHandle ScriptHandle,uInt16 ClockRate);
        :param: NiHandle ScriptHandle: The script handle returned from ni845xSpiScriptOpen.
                uInt16 ClockRate: Specifies the SPI clock rate. Refer to Chapter 3, NI USB-845x Hardware Overview, to
                    determine which clock rates your NI 845x device supports. If your hardware does not
                    support the supplied clock rate, a warning is generated, and the next smallest supported
                    clock rate is used.
                    If the supplied clock rate is smaller than the smallest supported clock rate, an error is
                    generated. The configuration does not validate the clock rate until it is committed to hardware.
        :return: None
        """
        returnvalue = self.ni8452.ni845xSpiScriptClockRate(self.script_handle, c.c_uint16(clockrate))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)

    def ni845xSpiScriptCSHigh(self, chipselect=0):
        """
        Calls the NI USB-8452 C API function ni845xSpiScriptCSHigh whose prototype is
        int32 ni845xSpiScriptCSHigh (NiHandle ScriptHandle,uInt32 ChipSelectNum);
        :param: NiHandle ScriptHandle: The script handle returned from ni845xSpiScriptOpen.
                uInt32 ChipSelect: The chip select to set high.
        :return: None
        """
        returnvalue = self.ni8452.ni845xSpiScriptCSHigh(self.script_handle, c.c_uint32(chipselect))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)

    def ni845xSpiScriptCSLow(self, chipselect=0):
        """
        Calls the NI USB-8452 C API function ni845xSpiScriptCSLow whose prototype is
        int32 ni845xSpiScriptCSLow (NiHandle ScriptHandle,uInt32 ChipSelectNum);
        :param: NiHandle ScriptHandle: The script handle returned from ni845xSpiScriptOpen.
                uInt32 ChipSelect: The chip select to set low.
        :return: None
        """
        returnvalue = self.ni8452.ni845xSpiScriptCSLow(self.script_handle, c.c_uint32(chipselect))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)

    def ni845xSpiScriptNumBitsPerSample(self, numbitspersample=0):
        """
        Calls the NI USB-8452 C API function ni845xSpiScriptNumBitsPerSample whose prototype is
        int32 ni845xSpiScriptNumBitsPerSample (NiHandle pScriptHandle,uInt16 NumBitsPerSample);
        :param: NiHandle ScriptHandle: The script handle returned from ni845xSpiScriptOpen.
                uInt16 * pNumBitsPerSample:
                    ASets the number of bits per sample to be clocked each SPI transmission. Refer to
                    Appendix A, NI USB-845x Hardware Specifications. for valid settings for this property.
        """
        returnvalue = self.ni8452.ni845xSpiScriptNumBitsPerSample(self.script_handle, c.c_uint16(numbitspersample))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)

    def ni845xSpiScriptUsDelay(self, delay=0):
        """
        Calls the NI USB-8452 C API function ni845xSpiScriptUsDelay whose prototype is
        int32 ni845xSpiScriptUsDelay (NiHandle ScriptHandle,uInt16 Delay);
        :param: NiHandle ScriptHandle: The script handle returned from ni845xSpiScriptOpen.
                uInt16 Delay: The desired delay in microseconds.
        :return: None
        This command adds a microsecond delay after the previousSPI script command.
        """
        returnvalue = self.ni8452.ni845xSpiScriptUsDelay(self.script_handle, c.c_uint16(delay))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)

    def ni845xSpiScriptEnableSPI(self):
        """
        Calls the NI USB-8452 C API function ni845xSpiScriptEnableSPI whose prototype is
        int32 ni845xSpiScriptEnableSPI (NiHandle pScriptHandle);
        :param: NiHandle ScriptHandle: The script handle returned from ni845xSpiScriptOpen.
        :return: None

        This command switches the pins on the SPI port you
        specify when you use ni845xSpiScriptRun, from tristate to master mode function.
        """
        returnvalue = self.ni8452.ni845xSpiScriptEnableSPI(self.script_handle)
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)

    def ni845xSpiScriptDisableSPI(self):
        """
        Calls the NI USB-8452 C API function ni845xSpiScriptDisableSPI whose prototype is
        int32 ni845xSpiScriptDisableSPI (NiHandle pScriptHandle);
        :param: NiHandle ScriptHandle: The script handle returned from ni845xSpiScriptOpen.
        :return: None
        This command tristates the pins on the SPI port you
        specify when you use ni845xSpiScriptRun. All chip select pins are also tristated.
        """
        returnvalue = self.ni8452.ni845xSpiScriptDisableSPI(self.script_handle)
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)

    def ni845xSpiScriptWriteRead(self, writesize=0, writedata=0, scriptreadindex=0):
        """
        Calls the NI USB-8452 C API function ni845xSpiScriptWriteRead whose prototype is
        int32 ni845xSpiScriptWriteRead (NiHandle ScriptHandle,
                                        uInt32 WriteSize,
                                        uInt8 * pWriteData,
                                        uInt32 * pScriptReadIndex);
        :param: NiHandle ScriptHandle: The script handle returned from ni845xSpiScriptOpen.
                uInt32 WriteSize: The number of bytes to write. This must be nonzero.
                uInt8 * pWriteData: The bytes to be write.
        :return: uInt32 * pScriptReadIndex:
                    A pointer to the write/read command index within the script. It is used as an input into
                    "ni845xSpiScriptExtractReadData".
        """
        Writedata = (c.c_uint8 * writesize)(*writedata)
        returnvalue = self.ni8452.ni845xSpiScriptWriteRead(self.script_handle,
                                                           c.c_uint32(writesize),
                                                           c.byref(Writedata),
                                                           c.byref(self.script_read_index)
                                                           )
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)
            self.status = returnvalue

    def ni845xSpiScriptExtractReadData(self, scriptreadindex=0):
        """
        Calls the NI USB-8452 C API function ni845xSpiScriptExtractReadData whose prototype is
        int32 ni845xSpiScriptExtractReadData (NiHandle ScriptHandle,
                                              uInt32 ScriptReadIndex,
                                              uInt8 * pReadData
                                              );
        :param: NiHandle ScriptHandle: The script handle returned from ni845xSpiScriptOpen.
                uInt32 * pScriptReadIndex: Identifies the read in the script whose data should be extracted.
        :return: uInt8 * pReadData:
                    Identifies the read in the script whose data should be extracted.
        """
        readdata = list()
        Readdata = (c.c_uint8 * scriptreadindex)(*readdata)
        returnvalue = self.ni8452.ni845xSpiScriptExtractReadData(self.script_handle,
                                                                 self.script_read_index,
                                                                 c.byref(Readdata)
                                                                 )
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)
            self.status = returnvalue

        readdata = [i for i in Readdata]
        return readdata

    def ni845xSpiScriptRun(self, portnumber=0):
        """
        Calls the NI USB-8452 C API function ni845xSpiScriptRun whose prototype is
        int32 ni845xSpiScriptRun (NiHandle ScriptHandle,NiHandle DeviceHandle,uInt8 PortNumber);
        :param: NiHandle ScriptHandle: The script handle returned from ni845xSpiScriptOpen.
                NiHandle DeviceHandle: Device handle returned from ni845xOpen.
                uInt8 PortNumber: The SPI port this script runs on.
        :return: None
        """
        returnvalue = self.ni8452.ni845xSpiScriptRun(self.script_handle,
                                                     self.device_handle,
                                                     c.c_uint8(portnumber)
                                                     )
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)
