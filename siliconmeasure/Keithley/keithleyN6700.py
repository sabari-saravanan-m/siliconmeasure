"""
Author                          : SABARI SARAVANAN M
Developed Tool and Version      : Python 3.9
Description                     : General functions for keithleyN6700
Module Name                     : Keithley general Interface of N6700 source meter
Module Version                  : 0.0.1
Created                         : March 2021
"""

import pyvisa as visa                                       # Provides a programming interface to control Ethernet/LXI, GPIB, serial, USB, PXI, and VXI instruments

class KeithleyN6700(object):

    """ This Keithley - N6700 library file provides you with the information required to use functions for remotely controlling your instrument.

        import keithleyN6700 as Keithley                                                 # Importing chroma6314A file

        KEITHLEY = Keithley.KeithleyN6700()                                              # Initialize & open an instrument reference
        KEITHLEY.open("GPIB0::6::INSTR")

        KEITHLEY.configure(1, 2.5, 0.5, 1)                                               # Configures parameters based on output selection(1/2/3/4)
        KEITHLEY.output(1)                                                               # Enables the output
        KEITHLEY.read_outputvoltage()                                                    # Returns set of triggered values

        KEITHLEY.close()                                                                 # Close an instrument reference
    """

    def __init__(self):
        """ Initialize visa resources & get list out all connected instruemnts resources with the system """
        try:
            self.rm              = visa.ResourceManager()                               # Provides access to all resources registered with it
            self.D               = list(self.rm.list_resources())                       # Lists the available resources

        except Exception as ex:
            self.import_error(ex)

        """ Create variable instances for function commands """

        self.channel            = [1, 2, 3, 4]                                          # Sets supply voltage of selected channel
        self.output_enable      = ["OFF", "ON"]                                         # Enables/disables output state

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
                    print(f"{self.inst_Q().strip()} resource has been connected")
        except Exception as ex:
            self.exceptionhandler(ex)

    def close(self):
        """ Closes connections to the instrument """
        try:
            close = self.inst_Q().strip()
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

    #############################################################
    # Utility
    #############################################################

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

    #############################################################
    # Query
    #############################################################

    def inst_Q(self):
        """ Query an instrument identification """
        try:
            inst_Q = self.write("*IDN?")                                                # Calling "query" instance to write SCPI commands
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
            common_Q = self.write(self.setting_Q[int(setting_q)])
            return common_Q

        except Exception as ex:
            self.exceptionhandler(ex)

    #############################################################
    # Common
    #############################################################

    def write(self, cmd: str=""):
        ''' SCIPI command directly can be sent using this function
            cmd : type string / parameter - SCIPI command with proper format e.g. 'MEAS:CURR?'
        '''
        if isinstance(cmd, str):
            if cmd.endswith('?'):
                try:
                    query = self.inst.query(cmd)
                    return query
                except Exception as ex:
                    self.exceptionhandler(ex)
            else:
                try:
                    self.inst.write(cmd)
                except Exception as ex:
                    self.exceptionhandler(ex)
        else:
            print("Invalid SCPI command: Please provid valid SCPI command input")

    #############################################################
    # Configuration
    #############################################################

    def configure(self, channel=0, output_voltage=0, output_current=0, display=1):
        """ Configures parameters of output voltage/current """
        """
            channel             ->  Sets the channel number
            output_voltage      ->  Sets an output voltage limit
            output_current      ->  Sets an output current limit
            display             ->  sets the front panel to display channel 4
        """
        self.write(":VOLTage {}, (@{});:CURRent {}, (@{});:DISPlay:CHANNel {}"
                    .format(output_voltage, self.channel[int(channel)],
                            output_current, self.channel[int(channel)],
                            self.channel[int(channel)]
                            )
                    )

    def output(self, output=1):
        """ Configures output state """
        """ output ->  Enables/disables output state """

        self.write(":OUTPut {};"
                    .format(self.output_enable[int(output)]
                            )
                    )

    #############################################################
    # Read
    #############################################################

    def read_outputvoltage(self):
        """ Returns the voltage measured at the output terminals of the source meter """

        read_voltage = self.write(":MEASure:VOLTage?")
        return float(read_voltage)

    def read_outputcurrent(self):
        """ Returns the current measured at the output terminals of the source meter """

        read_current = self.write(":MEASure:CURRent?")
        return float(read_current)

    def read_outputpower(self):
        """ Returns the power measured at the output terminals of the source meter """

        read_current = self.write(":MEASure:CURRent?")
        return float(read_current)

    def read_output(self):
        """ Returns the output state of the power supply """

        read_output = self.write(":OUTPut?")
        return read_output
