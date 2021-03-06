import sys
import time

import serial
import serial.tools.list_ports


import sim



def check_available_ports():
    '''
    return a list of [port, desc, hwid]
    '''
    ports = serial.tools.list_ports.comports()
    result = []
    for port, desc, hwid in sorted(ports):
        result.append([port, desc, hwid])
    return result



class ComSerial(serial.Serial):
    """docstring for ComPort
    port_info can be port name ig:'COM01' or hwid eg: '0483:5740'
    port_info_type = 'port' or 'hwid'
    """
    def __init__(self, port_info, port_info_type='port'):
        super().__init__()
        #self = serial.Serial()
        #ser.port = "/dev/ttyUSB0"
        self.port_info = port_info
        self.port_info_type = port_info_type
        #ser.port = "/dev/ttyS2"
        self.baudrate = 9600
        self.bytesize = serial.EIGHTBITS #number of bits per bytes
        self.parity = serial.PARITY_NONE #set parity check: no parity
        self.stopbits = serial.STOPBITS_ONE #number of stop bits
        #ser.timeout = None          #block read
        self.timeout = 1            #non-block read
        #ser.timeout = 2              #timeout block read
        self.xonxoff = False     #disable software flow control
        self.rtscts = False     #disable hardware (RTS/CTS) flow control
        self.dsrdtr = False       #disable hardware (DSR/DTR) flow control
        self.writeTimeout = 2     #timeout for write
        # buffer for readline method
        self.buf = bytearray()


    def connect(self):
        ports_info = check_available_ports()
        if self.port_info_type=='port':
            self.open_port(self.port_info)
            return True
        else:
            for port, desc, hwid_info in ports_info:
                if self.port_info in hwid_info:
                    self.open_port(port)
                    return True
        time.sleep(2)
        return False

    def disconnect(self):
        self.close()
        time.sleep(1)

    def open_port(self, port_num):
        self.port = port_num
        try: 
            self.open()
            time.sleep(2)
        except Exception as e:
            print ("error open serial port: " + str(e))
            raise e

    def write_data(self, data):
        try:
            if self.isOpen():
                self.flushInput() #flush input buffer, discarding all its contents
                self.flushOutput()#flush output buffer, aborting current output 
                                 #and discard all that is in buffer
                data_encoded = str.encode(data)
                self.write(data_encoded)
                #time.sleep(0.03)
                return True
        except Exception as e:
            print ("error communicating...: " + str(e))
            return False
        return False

    def readline(self, timeout=0):
        start_time = time.time()
        i = self.buf.find(b"\n")
        if i >= 0:
            r = self.buf[:i+1]
            self.buf = self.buf[i+1:]
            return r.decode("utf-8", errors="ignore").replace('\r\n','')
        while True:
            i = max(1, min(2048, self.in_waiting))
            data = self.read(i)
            i = data.find(b"\n")
            if i >= 0:
                r = self.buf + data[:i+1]
                self.buf[0:] = data[i+1:]
                return r.decode("utf-8", errors="ignore").replace('\r\n','')
            else:
                self.buf.extend(data)
                if time.time()-start_time>=timeout:
                    return 'TIMEOUT'



class DriverSerial(ComSerial):
    """docstring for DriverSerial
    port_info can be port name ig:'COM01' or hwid eg: '0483:5740'
    port_info_type = 'port' or 'hwid'
    """
    def __init__(self, port_info, port_info_type='port'):
        super().__init__(port_info, port_info_type)


class BoschSerial(ComSerial):
    """docstring for BoschSerial
    port_info can be port name ig:'COM01' or hwid eg: '0483:5740'
    port_info_type = 'port' or 'hwid'
    """
    def __init__(self, port_info, port_info_type='port'):
        super().__init__(port_info, port_info_type)
        


class Bosch():
    """docstring for Bosch
    port_info can be port name ig:'COM01' or hwid eg: '0483:5740'
    port_info_type = 'port' or 'hwid'
    """
    def __init__(self, driver_ser, bosch_ser):
        self.driver_ser = driver_ser
        self.driver_ser.connect()

        self.bosch_ser = bosch_ser

    def power_on(self):
        BOSCH_ON = '<RL1_1>'
        self.driver_ser.write_data(BOSCH_ON)

    def power_off(self):
        BOSCH_OFF = '<RL1_0>'
        self.driver_ser.write_data(BOSCH_OFF)

    def press_button(self, button_name):
        '''
        button_name can be: INFO, LEFT, RIGHT, BACK, UP, DOWN, CODE, ENTER
        '''
        cmds={}
        cmds['INFO_ON'] = '<BT1_1>'
        cmds['INFO_OFF'] = '<BT1_0>'
        cmds['LEFT_ON'] = '<BT2_1>'
        cmds['LEFT_OFF'] = '<BT2_0>'
        cmds['BACK_ON'] = '<BT3_1>'
        cmds['BACK_OFF'] = '<BT3_0>'
        cmds['UP_ON'] = '<BT4_1>'
        cmds['UP_OFF'] = '<BT4_0>'
        cmds['DOWN_ON'] = '<BT5_1>'
        cmds['DOWN_OFF'] = '<BT5_0>'
        cmds['CODE_ON'] = '<BT6_1>'
        cmds['CODE_OFF'] = '<BT6_0>'
        cmds['RIGHT_ON'] = '<BT7_1>'
        cmds['RIGHT_OFF'] = '<BT7_0>'
        cmds['ENTER_ON'] = '<BT8_1>'
        cmds['ENTER_OFF'] = '<BT8_0>'

        self.driver_ser.write_data(cmds[button_name + '_ON'])
        time.sleep(0.2)
        self.driver_ser.write_data(cmds[button_name + '_OFF'])
        time.sleep(0.2)
        print('pressed: ', button_name)

    def control_by_sequence(self, cmd_sequence):
        # select vehicle by sequence
        for cmd in cmd_sequence:
            cmd_type = cmd[0]
            parameter = cmd[1]
            if cmd_type=='WAIT':
                parameter = float(parameter)
                time.sleep(parameter)
            else:
                parameter = int(parameter)
                for press_count in range(0, parameter): 
                    self.press_button(cmd_type)

    def select_vehicle(self, select_vehicle_sequence):
        # back to main menu sequence
        main_menu_sequence = [
              ['BACK', 10],
              ['LEFT', 1],
              ['ENTER',1],
              ['BACK',1]]
        self.control_by_sequence(main_menu_sequence)

        # select vehicle from main menu
        self.control_by_sequence(select_vehicle_sequence)



    def obd2_link(self, cap):
        ''' link to obd2 first time after selecting vehicle '''

        cap.clear_data()
        for press_count in range(0, 2):
            self.press_button('ENTER')


        # wait for bosch to start reading monitor icons
        while cap.is_data_existing()==False: time.sleep(1)

        # check if the transmission is done 
        previous_data = cap.get_data() 
        while True:
            ''' for every 1s if the data gotten from sim software has no change
            then we assume there is no more data will be sent in this stage
            '''
            time.sleep(1) # check every 1s
            current_data = cap.get_data()
            if current_data==previous_data:
                break
            else:
                previous_data = current_data

        # clear data to check next transmission (DTCs)
        cap.clear_data()

        # enter to continue
        self.press_button('ENTER')

        # there are 2 cases after bosch finishes reading monitor icons
        # Case 1: bosch will read DTCs after pressing Enter
        # Case 2: bosch will go to Diagnostic Menu after pressing Enter
        # => we will wait for maximun 3 seconds to check if bosch would read DTCs then process for each case

        time_count = 0 # count time from this step
        # wait for bosch to start reading DTCs
        while cap.is_data_existing()==False: 
            time.sleep(0.5)
            time_count += 0.5
            if time_count>=3: # wait maximun 3 second
                break

        if time_count<3:
            pass # do nothing because DTCs has been linked automatically
        else:   
            # read DTCs if bosch does not automatically read DTCs
            self.press_button('DOWN')
            self.press_button('ENTER')
            self.press_button('ENTER')
            time.sleep(0.5)


        # check if the transmission is done 
        previous_data = cap.get_data() 
        while True:
            ''' for every 1s if the data gotten from sim software has no change
            then we assume there is no more data will be sent in this stage
            '''
            time.sleep(1) # check every 1s
            current_data = cap.get_data()
            if current_data==previous_data:
                break
            else:
                previous_data = current_data


    def obd2_relink(self, cap):
        ''' relink obd2 from the DTC screen'''
        relink_sequence = [
              ['BACK', 3],
              ['ENTER', 1],
              ['DOWN',1],
              ['ENTER',3]]

        cap.clear_data()
        self.control_by_sequence(relink_sequence)

        # wait for reading DTCs
        while cap.is_data_existing()==False: time.sleep(1)
        # wait for linking dtcs done
        time.sleep(5)

    def get_report_after_link(self):
        print_sequence = [
              ['BACK', 2],
              ['LEFT', 1],
              ['DOWN', 5],
              ['ENTER',1]]
        self.control_by_sequence(print_sequence)
        time.sleep(2) # wait the computer recognize com port
        print('sequence to print')
        self.bosch_ser.connect()
        print('bosch connected')
        self.press_button('ENTER')
        self.press_button('ENTER')
        report = ''
        while True:
            line = self.bosch_ser.readline(timeout=2)
            if not line=='TIMEOUT':
                report += line + '\n'
            else:
                self.bosch_ser.disconnect()
                print('finished get report')
                return report




class ReverseSystem():
    """docstring for ReverseSystem"""
    def __init__(self, cap_path, cap_hwid, driver_hwid, bosch_hwid):
        self.driver_ser = DriverSerial(driver_hwid, port_info_type='hwid')
        self.bosch_ser = BoschSerial(bosch_hwid, port_info_type='hwid')
        self.cap = sim.CaptureTool(cap_path, cap_hwid)
        self.bosch = None

    def init(self):
        self.cap.run()
        self.bosch = Bosch(self.driver_ser, self.bosch_ser)
        self.bosch.power_on()




import vehicles
print('================= load list of vehicle sequences')
vehicle_selections = vehicles.get_sequences()


print('================= assign HWID and simulation exe path')
cap_path = 'CaptureTool 3.0.42\\CaptureTool.exe'
cap_hwid = '0483:5740'
driver_hwid = '1A86:7523'
bosch_hwid = '125E:2806'


print('================= create reverse system and init')
reverse_system_01 = ReverseSystem(cap_path, cap_hwid, driver_hwid, bosch_hwid)
reverse_system_01.init()



for veh, sequence in vehicle_selections.items():
    print('================= load vehicle:', veh)
    reverse_system_01.bosch.select_vehicle(sequence)

    # all the dtc that we want to reverse
    dtcs_storage =['P0002','P0003','P0004', 'P1005']
    # number of dtcs that we want to create simulation file a time
    number_of_dtcs = 3
    # this pointer is used for selecting the next set of dtcs
    pointer = 0

    while True:
        dtcs = dtcs_storage[pointer: pointer + number_of_dtcs]
        print('================= current set of dtcs:', dtcs)




        print('================= create sim file for the current set of dtcs')
        sim_path = 'sim\\bosch_sim.sim'
        sim.create_sim(sim_path, dtcs)


        print('================= load sim file')
        reverse_system_01.cap.load(sim_path)
        print('================= clear sim info data')
        reverse_system_01.cap.clear_data()



        # check if the this is the first time of obd2 linking
        print('================= link obd2')
        if 'first_flag' not in locals():
            reverse_system_01.bosch.obd2_link(reverse_system_01.cap)
            first_flag=True
            print('linked obd2 frist time')
        else:
            reverse_system_01.bosch.obd2_relink(reverse_system_01.cap)
            print('relinked obd2')

        # get report 
        print('================= print report')
        report = reverse_system_01.bosch.get_report_after_link()
        print(report, '\n\n\n\n\n\n')
        
        # set new pointer for the list of dtcs
        print('================= set new pointer')
        if pointer > len(dtcs_storage) - number_of_dtcs:
            break
        else:
            pointer += number_of_dtcs







