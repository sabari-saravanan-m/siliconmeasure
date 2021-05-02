"""
Author                          : SABARI SARAVANAN M
Developed Tool and Version      : Python 3.9
Description                     : General functions for tektronixMSO4000B, MDO4000B, MDO4000, MSO4000B, DPO4000B and MDO3000
Module Name                     : Tektronix general Interface of MDO4000B, MDO4000, MSO4000B, DPO4000B and MDO3000 Series Oscilloscopes
Module Version                  : 0.0.1
Created                         : March 2021
"""

import pyvisa as visa                                       # Provides a programming interface to control Ethernet/LXI, GPIB, serial, USB, PXI, and VXI instruments
from datetime import datetime

class TektronixMSO4000B(object):

    """ This TEKTRONIX - MSO4000B, MDO4000B, MDO4000, MSO4000B, DPO4000B and MDO3000 library file provides you with the
        information required to use functions for remotely controlling your instrument.

        import tektronixMSO4000B as Tektronix                                           # Importing chroma6314A file

        TEKTRONIX = Tektronix.TektronixMSO4000B()                                       # Initialize & open an instrument reference
        TEKTRONIX.open("TCPIP0::192.168.199.149::4000::SOCKET")

        TEKTRONIX.time_measurement(1, 0, 0, 1, 0, 1)                                    # Configures time_measurement parameters based on the channel selection
        TEKTRONIX.read_measurement(0, 0)                                                # Reads the measurement value

        TEKTRONIX.close()                                                               # Close an instrument reference
    """

    def __init__(self):
        """ Initialize visa resources & get list out all connected instruemnts resources with the system """
        try:
            self.rm              = visa.ResourceManager()                               # Provides access to all resources registered with it
            self.D               = list(self.rm.list_resources())                       # Lists the available resources

        except Exception as ex:
            self.import_error(ex)

        """ Create variable instances for function commands """

        self.channel            = ["CH1", "CH2", "CH3", "CH4",
                                   "CH5", "CH6", "CH7", "CH8"]                          # Select the channel
        self.time_measure_type  = ["FREQuency", "PERIod", "PWIdth", "NWIdth",           # Select the immediate measurement type
                                   "FALL", "RISe", "DELay", "PDUty", "NDUty"]
        self.measure_visible    = ["OFF", "MEAS"]                                       # specify the state of visible measurement indicator
        self.measure_active     = [1, 2, 3, 4, 5, 6, 7, 8]                              # visible measurement indicators for measurement <x>, can be 1 through 8.
        self.acquisition        = ["OFF", "ON", "RUN", "STOP"]                          # Acquisition mode
        self.display            = ["OFF", "ON"]

    def resource_list(self):
        """ List out connected instruments from list_resources """
        return self.D

    def open(self, inst_resource: str="", reset=False, idn=True):
        """ Establishes communication with the instrument and
            optionally performs an instrument identification query and/or an instrument reset.
        """
        try:
            self.inst = self.rm.open_resource(f"{inst_resource}")                       # Opens the resource of an instrument
            self.inst.timeout = 10000

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
                    print(f"{self.inst} resource has been connected")
        except Exception as ex:
            self.exceptionhandler(ex)

    def close(self):
        """ Closes connections to the instrument """
        try:
            #close = self.inst_Q()
            self.inst.close()
            self.rm.close()
            print(f"{self.inst} resource has been disconnected")
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

        self.write("*RST")                                                          # Calling "write" instance to write SCPI commands
        self.default_setup()                                                        # Calling "default setup" instance

    def default_setup(self):
        """ Sends a default command string to the instrument whenever a new VISA session is opened, or the instrument is reset.
            Use this function as a subfunction for the Initialize and Reset.
        """

        self.write("*ESE 60;*SRE 48;*CLS")                                          # Calling "write" instance to write SCPI commands


    #############################################################
    # Query
    #############################################################

    def inst_Q(self):
        """ Query an instrument identification """

        inst_Q = self.write("*IDN?")                                                # Calling "query" instance to write SCPI commands
        return inst_Q

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
        common_Q = self.write(self.setting_Q[int(setting_q)])
        return common_Q

    #############################################################
    # Common
    #############################################################

    def write(self, cmd: str=""):
        """ SCPI command directly can be sent using this function
            cmd : type string / parameter - SCPI command with proper format e.g. 'MEAS:CURR?'
        """

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

    ###########################################
    # Settings                                #
    ###########################################

    def save_setup(self, location="1"):
        """
            Saves the current front-panel setup into the specified memory location or file.
            "location" - Argument should be following format;
                         file_path - "C:\Windows"
                         or
                         Value ranges from 1 to 10.
        """
        self.write(f"SAVe:SETUp {location}")
        print("Front-panel setup has been saved successfully.")


    def recall_setup(self, recall="FACtory"):
        """
            Restores a stored or factory frontpanel setup of the instrument from a copy of the settings stored in memory.
            "recall" - Argument should be following format;
                       By default restores the factory setup - FACtory
                       or
                       file_path - "C:\Windows"
                       or
                       Value - 1 to 10.
        """
        self.write(f"RECAll:SETUp {recall}")
        print("Front-panel setup has been recalled successfully.")

    def delete_setup(self, delete="ALL"):
        """
            Changes the setup to reference the factory setup instead of the specific user setup slot.
            "recall" - Argument should be following format;
                       By default it deletes all the stored setups - ALL
                       or
                       Value - 1 to 10.
            Note: The setup information cannot be recovered once it has been deleted.
        """
        self.write(f"DELEte:SETUp {delete}")
        print("Front-panel setup has been deleted successfully.")

    #############################################################
    # Configure
    #############################################################

    def time_measurement(self, acquisition=1, channel=0, time_measure_type=0, measure_visible=1, measure_active=0, display=1):
        """ Configures parameters to read the time measurement of the channel """
        """
            acquisition         ->  Starts or stops acquisitions. When state is set to ON or RUN, a new acquisition will be started.
                OFF, STOP       -   stops acquisitions.
                ON, RUN         -   starts acquisitions.
            channel             ->  specifies the source for all single channel(CH1) measurements.
            time_measure_type   ->  specifies the immediate measurement type as ("PERIod", "FREQuency",...)
                FREQuency       -   Measures the first cycle in the waveform or gated region. Frequency
                                    is the reciprocal of the period and is measured in hertz (Hz), where 1 Hz = 1
                                    cycle per second.
                PERIod          -   The time required to complete the first cycle in a waveform or gated region.
                                    Period is the reciprocal of frequency and is measured in seconds.
                PWIdth          -   The distance (time) between the middle reference (default = 50%) amplitude points of a positive pulse.
                                    The measurement is made on the first pulse in the waveform or gated region.
                NWIdth          -   The distance (time) between the middle reference (default = 50%) amplitude points of a negative pulse.
                                    The measurement is made on the first pulse in the waveform or gated region.
                FALL            -   Measures the time taken for the falling edge of the first pulse in the
                                    waveform or gated region to fall from a high reference value (default is 90%) to
                                    a low reference value (default is 10%). This measurement is applicable only
                                    to the analog channels.
                RISe            -   The time it takes for the leading edge of the first pulse encountered to rise from a
                                    low reference value (default is 10%) to a high reference value (default is 90%).
                                    This measurement is applicable only to the analog channels.
                DELay           -   Measures the time between the middle reference (default = 50%) amplitude
                                    point of the source waveform and the destination waveform.
                PDUty           -   The ratio of the positive pulse width to the signal period, expressed as a percentage.
                                    It is measured on the first cycle in the waveform or gated region.
                                    Positive Duty Cycle = ((Positive Width) / Period) × 100%
                NDUty           -   The ratio of the negative pulse width to the signal period, expressed as a percentage.
                                    The duty cycle is measured on the first cycle in the waveform or gated region.
                                    Negative Duty Cycle = ((Negative Width) / Period) × 100%
            measure_visible     ->  Specifies the state of visible measurement indicators.
                OFF             -   Turns the visible measurement indicators off.
                MEAS<x>         -   Displays the visible measurement indicators for measurement <x>,
                                    where <x> can be 1 through 8.
            measure_active      ->  Returns the units associated with the specified measurement. The measurement
                                    slots are specified by <x>, which ranges from 1 through 8.
            display             ->  This command specifies the state of visible measurement indicators.
                OFF             -   Turns the visible measurement indicators off.
                ON              -   Turns the visible measurement indicators on.

        """
        self.write(":ACQuire:STATE {};:MEASUrement:MEAS{}:TYPe {};:MEASUREMENT:INDICATORS:STATE {}{};:MEASUrement:MEAS{}:STATE {};:MEASUrement:MEAS{}:SOUrce1 {};"
                    .format(self.acquisition[int(acquisition)],
                            self.measure_active[int(measure_active)],
                            self.time_measure_type[int(time_measure_type)],
                            self.measure_visible[int(measure_visible)],
                            self.measure_active[int(measure_active)],
                            self.measure_active[int(measure_active)],
                            self.display[int(display)],
                            self.measure_active[int(measure_active)],
                            self.channel[int(channel)]
                            )
                    )
    #############################################################
    # Read
    #############################################################

    def read_measurement(self, channel=0, time_measure_type=0):
        """ Read configred measurement value from the channel
        """
        read_measurement = self.write(":MEASUrement:IMMed:SOUrce1 {};:MEASUrement:IMMed:TYPe {};:MEASUrement:IMMed:VALue?"
                                      .format(self.channel[int(channel)],
                                              self.time_measure_type[int(time_measure_type)]
                                              )
                                      )
        return read_measurement

    def save_hardcopy(self, path:str="D:\\", filename:str="MSO4000B"):
        try:
            self.write("SAVe:IMAGe 'C:/Temp.png'")                                          # Save image to instrument's local disk
            self.write("*OPC?")                                                             # Wait for instrument to finish writing image to disk
            self.write("FILESystem:READFile 'C:/Temp.png'")                                 # Read image file from instrument
            read_data = self.inst.read_raw(1024*1024)

            file = open(f"{path}{filename}.png", 'wb')                                      # Open the file
            file.write(read_data); file.close()                                             # Image data has been transferred to PC and saved

            self.write("FILESyetem:DELEte 'C:/Temp.png'")                                   # Delete image file from instrument's hard disk
            print("Hardcopy has saved!!!")
        except:
            pass
