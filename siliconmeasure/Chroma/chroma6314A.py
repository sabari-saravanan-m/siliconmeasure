"""
Author                          : SABARI SARAVANAN M
Developed Tool and Version      : Python 3.9
Description                     : General ChromaLoad-API functions for 6314A
Module Name                     : Chroma Load 6314A - API Interface
Module Version                  : 0.0.1
Created                         : March 2021

"""

import time
import numpy
import pyvisa as visa

class Chroma6314A(object):
    """
        This Chroma - 6314A library file provides you with the information required to use functions for remotely controlling your instrument.

        import chroma6314A as chroma                                                # Importing chroma6314A file

        CHROMA = chroma.Chroma6314A()                                               # Initialize & open an instrument reference
        CHROMA.open("GPIB0::1::INSTR")

        CHROMA.channel_subsystem(0, 1, 0)                                           # Configures channel
        CHROMA.mode_subsystem(0)                                                    # Configures CC/CV mode
        CHROMA.current_subsystem(1, 0.5, 0.2, 0.200, 0.200, 0.020, 0.010)           # Configures current subsystem parameters
        CHROMA.load_subsystem(1)                                                    # Enables load to sink the current
        CHROMA.measure_I()                                                          # Returns current value

        CHROMA.close()                                                              # Close an instrument reference

    """
    def __init__(self):
        """ Initialize visa resources & get list out all connected instruemnts resources with the system """
        try:
            self.rm              = visa.ResourceManager()                               # Provides access to all resources registered with it
            self.D               = list(self.rm.list_resources())                       # Lists the available resources

        except Exception as ex:
            self.import_error(ex)

        """ Create variable instances for function commands """

        self.channel            = [1,2,3,4,5,6,7,8]                                     #
        self.mode               = ['CCL', 'CCH', 'CCDL', 'CCDH', 'CRL', 'CRH', 'CV']    # Sets operational modes of the electronic load
        self.default_low_l1     = 12                                                    # 12A for all low mode level1 voltage
        self.default_low_l2     = 6                                                     # 6A for all low mode level1 voltage
        self.default_high_l1    = 120                                                   # 120A for all low mode level1 voltage
        self.default_high_l2    = 60                                                    # 60A for all low mode level1 voltage
        self.default_rise_fall  = 4                                                     # 4mA/Us
        self.default_T1_T2      = '0.5mS'                                               # 0.5mS
        self.input_port         = ['UUT','LOAD']
        self.curr_range         = 120
        self.curr_subsystem     = ["STATic", "DYNamic"]
        self.state              = ["OFF", "ON"]
        self.volt_mode          = ["FAST", "SLOW"]
        self.volt_slowtype      = ["MOST", "MORE"]
        self.auto_mode          = ["LOAD", "PROGRAM"]

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
        except:
            self.import_error()

    def resource_list(self):
        """ List out connected instruments from list_resources """
        return self.D

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

    def common_Q(self, setting_q: str=""):
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
            common_Q = self.query(setting_q)
            return common_Q

        except Exception as ex:
            self.exceptionhandler(ex)

    #############################################################
    # Common
    #############################################################

    def write(self, cmd: str=""):
        """
            SCPI command directly can be sent using this function
            cmd : type string / parameter - SCIPI command with proper format e.g. 'MEAS:CURR?'
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

    #############################################################
    # Configuration
    #############################################################

    def measure_subsystem(self, input_port=0, scan=0):
        """
        Select the input port of electronic load to measure the voltage parameter: UUT / LOAD.
        Sets the scanning mode of frame to load module ON or OFF
        """
        self.write(":MEASure:INPut {};:MEASure:SCAN {};"
                        .format(self.input_port[int(input_port)],
                                self.state[int(scan)]
                                )
                        )

    def channel_subsystem(self, channel=0, active=0, synchronized=0):
        """
            channel         - Select a specific channel by which the coming channel-specific
                              command will be received and executed.
            active          - Enables or disables the load module.
            synchronized    - Sets the load module to receive synchronized command action of RUN ABORT or not.
        """

        self.write(":CHANnel {};:CHANnel:ACTive {};:CHANnel:SYNCon {};"
                        .format(self.channel[int(channel)],
                                self.state[int(active)],
                                self.state[int(synchronized)]
                                )
                        )

    def mode_subsystem(self, mode=0):
        """
            This command sets operational modes of the electronic load.
            Parameters : CCL, CCH, CCDL, CCDH, CRL, CRH, CV
            CCL     -   Set CC mode of low range.
            CCH     -   Set CC mode of high range.
            CCDL    -   Set CC dynamic mode of low range.
            CCDH    -   Set CC dynamic mode of high range.
            CRL     -   Set CR mode of low range.
            CRH     -   Set CR mode of high range.
            CV      -   Set CV mode.
        """
        self.write(':MODE {};'
                        .format(self.mode[int(mode)]
                                )
                        )

    def current_subsystem(self, curr_subsystem=0, max_iload1=1, min_iload2=0, rise_slewrate=2.5,
                          fall_slewrate=1, dynamic_duration1=0.020, dynamic_duration2=0.010):
        """
            Sets dynamic and static load configuration mode,max_load1,max_load2,rise_slewrate, fall_slewrate,
            dynamic_duration1, dynamic_duration2 in this function. Need to provide all input

            curr_subsystem                          : type - string / parameter - STATic , DYNamic
            max_iload1, max_iload2                  : type - int or float / parameter - 20A, 10A
            rise_slewrate, fall_slewrate            : type - int or float / parameter - 2.5 ,1 (format - 2.5A/uS)
            dynamic_duration1, dynamic_duration2    : type - str / parameter - 10mS ,1S
        """

        self.write(":CURRent:{}:L1 {};:CURRent:{}:L2 {};:CURRent:{}:RISE {};:CURRent:{}:FALL {};"
                    .format(self.curr_subsystem[int(curr_subsystem)], max_iload1,
                            self.curr_subsystem[int(curr_subsystem)], min_iload2,
                            self.curr_subsystem[int(curr_subsystem)], rise_slewrate,
                            self.curr_subsystem[int(curr_subsystem)], fall_slewrate
                            )
                   )

        if curr_subsystem == 1:                                                             # Sets the Dynamic Load Current during constant current mode
            self.write(":CURRent:{}:T1 {};:CURRent:{}:T2 {};"                          # Sets the duration parameter T1 or T2 of dynamic load
                            .format(self.curr_subsystem[int(curr_subsystem)], dynamic_duration1,
                                    self.curr_subsystem[int(curr_subsystem)], dynamic_duration2
                                    )
                            )

    def voltage_subsystem(self, max_vload1=5, min_vload2=0, max_currentlimit=0.5,
                          min_currentlimit=0, volt_mode=0, volt_slowtype=0):
        """
            Sets the voltage of static load during constant voltage mode.

            max_vload1, max_vload2                  : sets the voltage of static load during constant voltage mode. (24V, 8V)
            max_currentlimit, min_currentlimit      : It sets the current limit of constant voltage mode. (3A, 0A)
            volt_mode                               : It sets the response speed of CV mode. ["FAST", "SLOW"]
            volt_slowtype                           : It sets the response speed of slow type. ["MOST", "MORE"]
        """

        self.write(":VOLTage:L1 {};:VOLTage:L2 {};:VOLTage:CURRent {};:VOLTage:CURRent {};:VOLTage:MODE {};:VOLTage:SLOWTYPE {};"
                   .format(max_vload1, min_vload2,
                           max_currentlimit, min_currentlimit,
                           self.volt_mode[int(volt_mode)],
                           self.volt_slowtype[int(volt_slowtype)]
                           )
                   )

    def resistance_subsystem(self, max_resistance_load=5, min_resistance_load=0,
                             rise_slewrate=0.5, fall_slewrate=0):
        """
            It sets the static resistance level of constant resistance mode.

            max_resistance_load, max_resistance_load    : It sets the constant resistance = 20 ohm for Load L1, 10 ohm for Load L2
            rise_slewrate, fall_slewrate                : It sets the CR rise slew rate to 2.5A/μS, fall slew rate to 1A/μS.
        """

        self.write(":RESistance:L1 {};:RESistance:L2 {};:RESistance:RISE {};:RESistance:FALL {};"
                   .format(max_resistance_load, min_resistance_load,
                           rise_slewrate, fall_slewrate
                           )
                   )

    def load_subsystem(self, active=1):
        """ The LOAD command makes the electronic load active/on or inactive/off """
        self.write(":LOAD {};"
                    .format(self.state[int(active)]
                            )
                    )

    def configure_subsystem(self, key=1, remote_sound=1):
        """
            KEY         -> Sets if change the MEAS key on the Module to Static/Dynamic.
            SOUND       -> Sets the buffer sound of load module to ON or OFF.
        """
        self.write(":CONFigure:KEY {};:CONFigure:SOUND {};"
                    .format(self.state[int(key)],
                            self.state[int(remote_sound)]
                            )
                    )

    # def sweep(self,start,stop,step):
    #
    #     ''' sweep DC load from given start current value to given stop current value with given step current value
    #     type int'''
    #     print('Please check sense line connection ,VOUT Voltage level and current rating of the load cable ')
    #
    #     time.sleep(3)
    #     self.inst.write('CURR:STAT:L1 0')
    #     self.inst.write('CURR:STAT:L2 0')
    #     self.inst.write('LOAD ON')
    #     stop=stop+step
    #     try:
    #         for i in numpy.arange(start, stop, step):
    #             self.inst.write('CURR:STAT:L1 '+str(i))
    #             self.inst.write('CURR:STAT:L2 '+str(i))
    #             time.sleep(1)
    #         self.inst.close()
    #         return True
    #     except: raise('Error happened while sweeping DC load current')

    #############################################################
    # Measure
    #############################################################

    def measure_V(self):
        """ Return the voltage measured at the input of electronic load """
        measure_V = self.write("MEASure:VOLTage?")
        return measure_V

    def measure_I(self):
        """ Return the current measured at the input of electronic load """
        measure_I = self.write("MEASure:CURRent?")
        return measure_I

    def measure_all_V(self):
        """ Return the voltage measured at the input of all module """
        self.write("MEASure:ALLVoltage?")

    def measure_all_I(self):
        """ Return the current measured at the input of all module """
        self.write("MEASure:ALLCurrent?")

    def get_load_status(self):
        """ Return the current measured at the input of all module """
        self.write("LOAD?")

    def fetch_status(self):
        """ Return the real time status of the load module """
        self.write("FETCh:STATus?")

    def select_ch_query(self):
        """ Return selected channel """
        self.write(":CHANnel?")

    def query_mode(self):
        """ return selected mode """
        self.write(":MODE?")

    def query_meas_input(self):
        """ Return Selected the input port of electronic load to measure the voltage """
        self.write("MEASure:INP?")

    def query_meas_scan(self):
        """ Return Selected scanning mode of frame to load module """
        self.write("MEASure:SCAN?")


"""
c = Chroma6314A()
c.open(inst_resource="GPIB0::1::INSTR", reset=True, idn=True)
for i in range(1, 8, 2):
    i += 1
    try:
        c.channel_subsystem(channel=i, active=0, synchronized=0)
    except IndexError:
        break
c.channel_subsystem(channel=0, active=1, synchronized=0)
c.mode_subsystem(mode=2)
c.current_subsystem(curr_subsystem=1, max_iload1=0.5, min_iload2=0.2, rise_slewrate=0.200, fall_slewrate=0.020,
                    dynamic_duration1=0.020, dynamic_duration2=0.010)
# c.configure_subsystem(key=0, remote_sound=1)
c.load_subsystem(1)
print(c.measure_V())
print(c.measure_I())
# c.configure_subsystem(auto_load=0, auto_mode=0, remote_sound=1)
c.close()
"""
