"""
Author                          : SABARI SARAVANAN M
Developed Tool and Version      : Python 3.9
Description                     : General functions for NI8452 (SPI/I2C/SPIO)
Module Name                     : NIUSB-8452 General Interface of SPI/I2C/SPIO
Module Version                  : 0.0.1
Created                         : February 2021
"""

import ctypes as c                                              # It provides C compatible data types, and allows calling functions in DLLs or shared libraries.

class General(object):

    """
     This class makes Python calls to the C DLL of NI USB 8452 (ni845x.dll).
     Use this following example line with I2c device.

        from NI8452 import I2C                                  # Importing I2c class from main NI8452 class

        NI8452 = I2C.I2C()                                      # Calls to the C DLL & & List out connected NI-8452 devices
        NI8452.ni845xOpen()                                     # Open a device
        NI8452.ni845xSetIoVoltageLevel(33)                      # Sets the voltage level
        NI8452.ni845xSetTimeout(1000)                           # The minimum amount of time an I2C, I2c, or DIO operation is allowed to complete

    """

    def __init__(self):
        """
        calls to the C DLL of NI USB 8452 (ni845x.dll) & List out connected instrument resources from pc
        """
        self.first_device = None
        self.find_device_handle = c.c_ulong()                               # unsigned __int32 type
        self.number_found = c.c_ulong()                                     # unsigned __int32 type
        self.device_handle = c.c_ulonglong()                                # unsigned __int64 type
        self.configuration_handle = c.c_ulonglong(18446744073709551615)     # unsigned __int64 type
        self.script_handle = c.c_ulonglong()                                # unsigned __int64 type
        self.script_read_index = c.c_uint32()                               # unsigned __int32 type
        try:
            self.ni8452 = c.cdll.LoadLibrary("C:\\Windows\\System32\\Ni845x.dll")
        except:
            self.import_error()

    ###########################################
    # Error Handler
    ###########################################

    def import_error(self):
        ''' Update import error reported by the system of loading dll driver error.
        '''
        print("dll file not loaded, 'NI USB-8452 driver was not present/installed'.")

    def check_error(self, error):
        ''' Update device error reported by the system.
        '''
        print("Command Error:", error)

    #############################################################
    # General Device
    #############################################################

    def ni845xFindDevice(self, device_size=256):
        """
        Calls NI USB-8452 C API function ni845xFindDevice whose prototype is:
        int32 ni845xFindDevice (char * pFirstDevice, NiHandle * pFindDeviceHandle, uInt32 * pNumberFound);
        :return: name of first device
        """
        self.first_device = c.create_string_buffer(device_size)
        #self.find_device_handle = (c.c_ulong * 5)()
        #c.cast(self.find_device_handle, c.POINTER(c.c_ulong))
        #self.number_found = (c.c_ulong * 5)()
        #c.cast(self.number_found, c.POINTER(c.c_ulong))

        returnvalue = self.ni8452.ni845xFindDevice(self.first_device, c.byref(self.find_device_handle), self.number_found)

        print("Find Devicename:", str(self.first_device.value))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)

    def ni845xFindDeviceNext(self, device_size=256):
        """
        Calls NI USB-8452 C API function ni845xFindDevice whose prototype is:
        int32 ni845xFindDeviceNext (NiHandle FindDeviceHandle, char * pNextDevice);
        :return: find the remaining devices in the system
        """
        self.next_device = c.create_string_buffer(device_size)

        returnvalue = self.ni8452.ni845xFindDeviceNext(self.find_device_handle, self.next_device)
        print("returnvalue ni845xFindDeviceNext", returnvalue)
        print("Next DeviceName:", str(self.next_device))
        if returnvalue != 0:
            ni845xStatusToString(returnvalue)

    def ni845xCloseFindDeviceHandle(self):
        """
        Calls NI USB-8452 C API function ni845xCloseFindDeviceHandle whose prototype is:
        int32 ni845xCloseFindDeviceHandle (NiHandle FindDeviceHandle);
        :return: None
        """
        returnvalue = self.ni8452.ni845xCloseFindDeviceHandle(self.find_device_handle)
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)

    def ni845xDeviceLock(self):
        """
        Calls NI USB-8452 C API function ni845xFindDevice whose prototype is:
        int32 ni845xDeviceLock (NiHandle DeviceHandle);
        :return: None
                    This function locks NI 845x devices and prevents multiple processes or threads from
                    accessing the device until the process or thread that owns the device lock calls an equal
                    number of ni845xDeviceUnlock calls. Any thread or process that attempts to call
                    ni845xDeviceLock when the device is already locked is forced to sleep by the
                    operating system. This is useful for when multiple Basic API device accesses must occur
                    uninterrupted by any other processes or threads. If a thread exits without fully unlocking
                    the device, the device is unlocked. If a thread is the current owner of the lock, and calls
                    ni845xDeviceLock again, the thread will not deadlock itself, but care must be taken to call
                    ni845xDeviceUnlock for every ni845xDeviceLock called. This function can possibly
                    lock a device indefinitely: If a thread never calls ni845xDeviceUnlock, or fails to call
                    ni845xDeviceUnlock for every ni845xDeviceLock call, and never exits, other processes
                    and threads are forced to wait. This is not recommended for users unfamiliar with threads or
                    processes. A simpler alternative is to use scripts. Scripts provide the same capability to ensure
                    transfers are uninterrupted, and with possible performance benefits.
        """
        returnvalue = self.ni8452.ni845xDeviceLock(self.find_device_handle)
        print("returnvalue ni845xDeviceLock", returnvalue)
        if returnvalue != 0:
            ni845xStatusToString(returnvalue)

    def ni845xDeviceUnlock(self):
        """
        Calls NI USB-8452 C API function ni845xFindDevice whose prototype is:
        int32 ni845xDeviceUnlock (NiHandle DeviceHandle);
        :return: None
                    Use ni845xDeviceUnlock to unlock access to an NI 845x device previously locked with
                    ni845xDeviceLock. Every call to ni845xDeviceLock must have a corresponding call to
                    ni845xDeviceUnlock. Refer to ni845xDeviceLock for more details regarding how to
                    use device locks.
        """
        returnvalue = self.ni8452.ni845xDeviceUnlock(self.find_device_handle)
        print("returnvalue ni845xDeviceUnlock", returnvalue)
        if returnvalue != 0:
            ni845xStatusToString(returnvalue)

    def ni845xStatusToString(self, status_code, max_size=1024):
        """
        Calls NI USB-8452 C API function ni845xStatusToString whose prototype is:
        void ni845xStatusToString (int32 StatusCode, uInt32 MaxSize, int8 * pStatusString);
        :return:None
        """
        try:
            status_string = c.create_string_buffer(max_size)
            returnvalue = self.ni8452.ni845xStatusToString(status_code, max_size, status_string)
            str(status_string)
            print("Error_code:", status_code,"\nError_code_to_string:", status_string.value)
        except Exception as error:
            self.check_error(error)

    def ni845xOpen(self):
        """
        Calls the NI USB-8452 C API function ni845xOpen whose prototype is:
        int32 ni845xOpen (char * pResourceName, NiHandle * pDeviceHandle);
        :param resource_name: name of the resource
        :return:device handle
        """
        try:
            self.ni845xFindDevice()                 # Finds an NI 8452 device
        except:
            self.ni845xFindDeviceNext()             # Finds next NI 8452 device, which is connected next to the first device
        returnvalue = self.ni8452.ni845xOpen(self.first_device, c.byref(self.device_handle))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)
        else:
            return (f"Device #: {str(self.first_device.value)} Port has been opened succesfully.")

    def ni845xClose(self):
        """
        Calls the NI USB-8452 C API function ni845xClose whose prototype is
        :return: None
        """
        returnvalue = self.ni8452.ni845xClose(self.device_handle)
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)
        else:
            return (f"Device #: {str(self.first_device.value)} Port has been closed succesfully.")

    def ni845xSetIoVoltageLevel(self, VoltageLevel=33):
        """
        Calls the NI USB-8452 C API function ni845xSetIoVoltageLevel whose prototype is
        int32 ni845xSetIoVoltageLevel (NiHandle DeviceHandle,uInt8 VoltageLevel);
        :param: NiHandle DeviceHandle: Device handle returned from ni845xOpen.
        uInt8 VoltageLevel: The desired voltage level. VoltageLevel uses the following values:
            • kNi845x33Volts (33): The output I/O high level is 3.3 V.
            • kNi845x25Volts (25): The output I/O high level is 2.5 V.
            • kNi845x18Volts (18): The output I/O high level is 1.8 V.
            • kNi845x15Volts (15): The output I/O high level is 1.5 V.
            • kNi845x12Volts (12): The output I/O high level is 1.2 V.
            The default value of this property is 3.3 V(33).
        :return: None
        """
        returnvalue = self.ni8452.ni845xSetIoVoltageLevel(self.device_handle, c.c_uint8(VoltageLevel))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)

    def ni845xSetTimeout(self, timeout=30000):
        """
        Calls the NI USB-8452 C API function ni845xSetTimeout whose prototype is
        int32 ni845xSetTimeout (NiHandle DeviceHandle, uInt32 Timeout);
        :param: NiHandle DeviceHandle: Device handle returned from ni845xOpen.
            uInt32 Timeout:
              The timeout value in milliseconds.
              The minimum timeout is 1000 ms (1 second). The default of this property is 30000 (30 seconds).
        :return: None
        """
        returnvalue = self.ni8452.ni845xSetTimeout(self.device_handle, c.c_uint32(timeout))
        if returnvalue != 0:
            self.ni845xStatusToString(returnvalue)
