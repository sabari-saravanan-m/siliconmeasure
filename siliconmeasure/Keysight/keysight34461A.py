"""
Author                          : SABARI SARAVANAN M
Developed Tool and Version      : Python 3.9
Description                     : General functions for Keysight34461A/Keysight34465A
Module Name                     : Keysight General Interface of E3631A & 34465A AC/DC DMM
Module Version                  : 0.0.1
Created                         : March 2021
"""

import pyvisa as visa                                       # Provides a programming interface to control Ethernet/LXI, GPIB, serial, USB, PXI, and VXI instruments

class Keysight34461A(object):

    """ This Keysight - 34461A library file provides you with the information required to use functions for remotely controlling your instrument.

        import keysight34461A as Keysight                                           # Importing chroma6314A file

        KEYSIGHT = Keysight.Keysight34461A()                                        # Initialize & open an instrument reference
        KEYSIGHT.open("TCPIP0::A-34461A::5025::SOCKET")

        KEYSIGHT.configure_I(1, 0, 1, 3)                                            # Configures parameters based on selection type for AC/DC current
        KEYSIGHT.configure_V(1, 1, 0, 3)                                            # Configures parameters based on selection type for AC/DC voltage
        KEYSIGHT.Read(1, 0)                                                         # Returns set of triggered values

        KEYSIGHT.close()                                                            # Close an instrument reference
    """

    def __init__(self):
        """ Initialize visa resources & get list out all connected instruemnts resources with the system """
        try:
            self.rm                 = visa.ResourceManager()                            # Provides access to all resources registered with it
            self.D                  = list(self.rm.list_resources())                    # Lists the available resources

        except Exception as ex:
            self.import_error(ex)

        """ Create variable instances for function commands """

        self.setting_Q          = ["*CAL?, *ESR?", "*STB?", "*TST?"]                    # Sets comman query setting
        self.bandwidth          = [3, 20, 200]                                          # Enables you either to optimize low frequency(HZ) accuracy or
                                                                                        # to achieve faster AC settling times following a change in
                                                                                        # input signal amplitude.
        self.type               = ["AC", "DC"]                                          # Sets measurement type
        self.auto_impedance     = ["OFF", "ON"]                                         # Disables or enables automatic input impedance mode for DC voltage
        self.trigger_source     = ["IMMediate", "EXTernal", "BUS", "INTernal"]          # Selects the trigger source for measurements
        self.voltage_range      = [0.001, 1, 10, 100, 1000]                             # Configure voltage measurements(V)
        self.current_range      = [0.000001, 0.001, 0.010, 0.100, 1, 3]                 # Configure current measurements(A)
        self.current_terminal   = [3, 10]                                               # Configures the AC or DC current measurement to measure the source
                                                                                        # on the 3A or 10A terminals.

    def resource_list(self):
        """ List out connected instruments from list_resources """
        return self.D

    def open(self, inst_resource: str="", reset=True, idn=True):
        """ Establishes communication with the instrument and
            optionally performs an instrument identification query and/or an instrument reset.
        """
        try:
            self.inst = self.rm.open_resource(f"{inst_resource}")                       # Opens the resource of an instrument

            if (self.inst.resource_name.startswith("ASRL") or
                self.inst.resource_name.startswith("TCPIP") or
                self.inst.resource_name.startswith("TCPIP0") or
                self.inst.resource_name.endswith("SOCKET")
                ):
                self.inst.read_termination = "\n"                                       # Add read_termination = "\n" if communication type is TCP/IP

            if (len(self.D)) == 0:
                print("No devices connected.")
            else:
                if reset:
                    self.reset()
                if idn:
                    print(f"{self.inst_Q()} resource has been connected")
        except Exception as ex:
            self.exceptionhandler(ex)

    def close(self):
        """ Closes connections to the instrument """
        try:
            close = self.inst_Q()
            self.inst.close()
            self.rm.close()
            print(f"{close} resource has been disconnected")
        except Exception as ex:
            self.exceptionhandler(ex)

    #############################################################
    # Error Handler
    #############################################################

    def import_error(self):
        """ Update import error reported by the system
        """
        print("Invalid Adapter provided for Instrument since, 'Chroma6314A - Load Python file is not present/installed'.")

    def exceptionhandler(self, exception):
        """ Update device error reported by the system
        """
        print("Command Error:", exception)

    ###########################################
    # Utility
    ###########################################

    def reset(self):
        """ Resets the instrument and then sends a set of default setup commands to the instrument """
        try:
            self.write("*RST")                                                          # Calling "write" instance to write SCPI commands
            self.default_setup()                                                        # Calling "default setup" instance
        except Exception as ex:
            self.exceptionhandler(ex)

    def default_setup(self):
        """ Sends a default command string to the instrument whenever a new VISA session is opened, or the instrument is reset.
            Use this function as a subfunction for the Initialize and Reset.
        """
        try:
            self.write("*ESE 60;*SRE 48;*CLS")                                          # Calling "write" instance to write SCPI commands
        except Exception as ex:
            self.exceptionhandler(ex)

    ###########################################
    # Query
    ###########################################

    def inst_Q(self):
        """ Query an instrument identification """
        try:
            inst_Q = self.query("*IDN?")                                                # Calling "query" instance to write SCPI commands
            return inst_Q
        except Exception as ex:
            self.exceptionhandler(ex)

    def common_Q(self, setting_q=0):
        """
        *CAL? - Query an instruemnt calibration status.
                Note: The self-calibration can take several minutes to respond.
                      No other commands will be executed until calibration is complete.
        *ESR? - Returns the contents of the event status register in decimal form
                and subsequently sets the register to zero.
        *STB? - Reads the contents of the status byte in decimal form.
        *TST? - Initiates self-tests of the instrument and returns an error code

        Passing an argument for setting_q variable from above listed commands;

        Example: common_Q = (0)
        """
        try:
            common_Q = self.query(self.setting_Q[int(setting_q)])
            return common_Q

        except Exception as ex:
            self.exceptionhandler(ex)

    #############################################################
    # Common
    #############################################################

    def write(self, cmd: str=""):
        """ Writes function commands into an instrument """
        try:
            self.inst.write(cmd)
        except Exception as ex:
            self.exceptionhandler(ex)

    def query(self, cmd: str=""):
        """ Queries function commands from an instrument """
        try:
            query = self.inst.query(cmd)
            return query
        except Exception as ex:
            self.exceptionhandler(ex)

    def read(self, cmd: str=""):
        """ Reads function commands from an instrument """
        try:
            read = self.inst.read(cmd)
            return read
        except Exception as ex:
            self.exceptionhandler(ex)

    #############################################################
    # Configuration
    #############################################################

    def configure_V(self, type=1, bandwidth=1, auto_impedance=0, voltage_range=3):
        """ Configures parameters based on selection type AC/DC """
        """
            type           -> Sets measurement type for AC/DC.
            bandwidth      -> The instrument selects the slow (3 Hz), medium (20 Hz) or fast (200 Hz) filter based
                              on the cutoff frequency specified by this command.(only for AC).

            auto_impedance -> Disables or enables automatic input impedance mode for DC voltage and ratio measurements.
                              OFF - The input impedance for DC voltage measurements is fixed at 10 MΩ for all ranges to minimize
                                     noise pickup.
                              ON  - The input impedance for DC voltage measurements varies by range. It is set to "HI-Z" (>10 GΩ) for
                                    the 100 mV, 1 V, and 10 V ranges to reduce the effects of measurement loading errors on these lower
                                    ranges. The 100 V and 1000 V ranges remain at a 10 MΩ input impedance.
            voltage_range  -> Selects a fixed measurement range for AC and DC voltage measurements.
                              If the input signal is greater than can be measured on the specified manual range, the instrument displays
                              the word Overload on front panel and returns "9.9E37" from the remote interface.
        """
        if type == 0:                                                                   # Chooses AC type configuration
            self.write(":CONF:VOLTage:{};:VOLTage:{}:BANDwidth {};:VOLTage:{}:RANGe {};"
                        .format(self.type[int(type)], self.type[int(type)],
                                self.bandwidth[int(bandwidth)],
                                self.type[int(type)],
                                self.voltage_range[int(voltage_range)]
                                 )
                        )

        else:                                                                           # Chooses DC type configuration
            self.write(":CONF:VOLTage:{};:VOLTage:IMPedance:AUTO {};:VOLTage:{}:RANGe {};"
                        .format(self.type[int(type)],
                                self.auto_impedance[int(auto_impedance)],
                                self.type[int(type)],
                                self.voltage_range[int(voltage_range)]
                                 )
                        )

    def configure_I(self, type=1, current_terminal=0, bandwidth=1, current_range=3):
        """ Configures parameters based on selection type for AC/DC """
        """
            type                -> Sets measurement type for AC/DC.
            current_terminal    -> Configures the AC or DC current measurement to measure the source on the 3 A or 10 A terminals
            bandwidth           -> The instrument selects the slow (3 Hz), medium (20 Hz) or fast (200 Hz) filter based
                                   on the cutoff frequency specified by this command.(only for AC).

            current_range       -> Selects a fixed measurement range for AC or DC current measurements on the 3 A terminals.
                                   If the input signal is greater than can be measured on the specified manual range, the instrument displays
                                   the word Overload on front panel and returns "9.9E37" from the remote interface.
        """
        if type == 0:                                                                   # Chooses AC type configuration
            self.write(":CONF:CURRent:{};:CURRent:{}:TERMinals {};:CURRent:{}:BANDwidth {};:CURRent:{}:RANGe {};"
                        .format(self.type[int(type)], self.type[int(type)],
                                self.current_terminal[int(current_terminal)],
                                self.type[int(type)], self.bandwidth[int(bandwidth)],
                                self.type[int(type)],
                                self.current_range[int(current_range)]
                                 )
                        )

        else:                                                                           # Chooses DC type configuration
            self.write(":CONF:CURRent:{};:CURRent:{}:TERMinals {};:CURRent:{}:RANGe {};"
                        .format(self.type[int(type)], self.type[int(type)],
                                self.current_terminal[int(current_terminal)],
                                self.type[int(type)],
                                self.current_range[int(current_range)]
                                 )
                        )

    #############################################################
    # Read
    #############################################################

    def read_DMM(self, sample_count=1, trigger_source=0):
        """ Returns set of triggered values """
        """ trigger_source   -> Selects the trigger source for measurements.
                IMMediate - The trigger signal is always present. When you place the instrument in the "wait-for-trigger"
                            state, the trigger is issued immediately. BUS The instrument is triggered by *TRG over the remote
                            interface once the DMM is in the "wait-fortrigger" state.
                EXTernal -  The instrument accepts hardware triggers applied to the rear-panel Ext Trig input and takes the
                            specified number of measurements (SAMPle:COUNt), each time a TTL pulse specified by
                            OUTPut:TRIGger:SLOPe is received. If the instrument receives an external trigger before it is
                            ready, it buffers one trigger.
                INTernal -  The INTernal source is available for the 34465A and 34470A with the DIG option only, and
                            provides level triggering capability. To trigger on a level on the input signal, select INTernal for the
                            source, and set the level and slope with the TRIGger:LEVel and TRIGger:SLOPe commands.
            sample_count ->  Specifies the number of measurements (samples) the instrument takes per trigger.
        """
        read = self.query(":SAMPle:COUNt {};:TRIGger:SOURce {};:READ?"
                    .format(sample_count, self.trigger_source[int(trigger_source)]
                            )
                    )
        return float(read)
