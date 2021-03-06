import sys
import re
import os
import time
from os import path

import serial
import serial.tools.list_ports

from pywinauto.application import Application
from pywinauto.keyboard import send_keys
from pywinauto.timings import TimeoutError

from dtc_converter import dtc2hex




def check_available_ports():
    '''
    return a list of [port, desc, hwid]
    '''
    ports = serial.tools.list_ports.comports()
    result = []
    for port, desc, hwid in sorted(ports):
        result.append([port, desc, hwid])
    return result



def ser_hwid_to_port(hwid):
    ports_info = check_available_ports()
    for port, desc, hwid_info in ports_info:
        if hwid in hwid_info:
            return port

def create_sim(fpath, dtcs):
    # standardize a dtcs list wiht at least 65 elements
    dtcs.extend(['P0000']*(65-len(dtcs)))
    dtcs = dtcs[0:65]
    byte_list = []
    for dtc in dtcs:
        byte_list.extend(dtc2hex(dtc).split(' '))

    global sim_template
    sim_data = sim_template.format(*byte_list)
    
    with open(fpath, 'w') as file_object:
        file_object.write(sim_data)




class CaptureTool():
    '''
    create a object of capture tool software
        path: path to cature tool exe
        hwid: hardware id of capture tool COM port
    '''
    def __init__(self, path, hwid):
        self.path = path
        self.port = ser_hwid_to_port(hwid)
        self.app = None
        self.main_win = None

    def run(self):
        '''
        run capture tool software, select COM port and press connect
        NOTE:
            + pressing connect cannot make sure the capture tool would connect to the Comport
            + need to check if the capture tool is connect by the method is_connected() 
        '''
        # run app
        self.app = Application().start(self.path)
        self.main_win = self.app.window(title_re='OBD Capture Tool .+')
        self.connect()


    def connect(self):
        ''' connect to comport '''
        # select COM
        combo_port = self.main_win.child_window(best_match='Edit1')
        combo_port.set_text(self.port)
        # click button connect
        button_connect = self.main_win.child_window(best_match='Connect')
        button_connect.click()


    def is_connected(self):
        # check if connected, if after 1 second the button still keeps 'Connect' value => failed
        button_connect = self.main_win.child_window(best_match='Connect')
        time.sleep(1)
        if button_connect.window_text()=='Connect':
            return False
        return True


    def load(self, sim_path):
        # get the absolute path of sim file
        sim_path = os.path.abspath(sim_path)

        # split file name and dir path out of the file path
        file_name = re.sub(r'^.+\\','',sim_path)
        dir_path = sim_path.replace('\\' + file_name,'')

        # click button
        self.main_win.set_focus()
        button_load = self.main_win.child_window(best_match='LoadDB')
        button_load.click()

        # get save dialog
        save_dlg = self.app.window(title_re='Save Simulation DataBase')
        save_dlg.wait('enabled')
        time.sleep(1)

        # get toolbar => click to toolbar => fill out address
        toolbar = save_dlg.child_window(control_id=1001, class_name='ToolbarWindow32')
        cur_dir_path = toolbar.texts()[0].replace('Address: ', '')

        # if the current dir path is same as the input dir path => skip filling new path
        if dir_path!=cur_dir_path:
            toolbar.click()
            save_dlg.type_keys(dir_path.replace(' ','{SPACE}'))
            time.sleep(1)
            save_dlg.type_keys('{ENTER}')
            time.sleep(1)

        # file name
        save_dlg.child_window(best_match='Edit1').set_text(file_name)
        save_dlg.child_window(best_match='Button1').click()

        # check file name error
        try:
            save_dlg.wait_not('visible', timeout=1)
        except Exception as e:
            return 'sim path not exists'

        # check load completes
        button_start_stop = self.main_win.child_window(best_match='Button5')
        while True:
            text = button_start_stop.window_text()
            if text=='start [ESC]':
                time.sleep(1)
            else: #stop
                break
        return True


    def is_data_existing(self):
        tooldata = self.main_win.child_window(best_match='Edit4')
        if tooldata.window_text():
            return True
        else:
            return False

    def get_data(self):
        tooldata = self.main_win.child_window(best_match='Edit4')
        return tooldata.window_text()

    def clear_data(self):
        self.main_win.child_window(best_match='Clear').click()
        time.sleep(0.5) #wait for the data is totally clear

    def close(self):
        self.app.kill()





sim_template = '''
###########################################
#         Auto Generated                  #
###########################################
<config sw> Protocol = 29
<config sw> PIN_KRX_CANH = 6
<config sw> TYPE_KRX_CANH = 0
<config sw> VOLT_KRX_CANH = 3
<config sw> PIN_KTX_CANH = 14
<config sw> TYPE_KTX_CANH = 0
<config sw> VOLT_KTX_CANH = 3
<config sw> PIN_LRX_CANH =  6
<config sw> TYPE_LTX_CANH = 0
<config sw> VOLT_LTX_CANH = 3
<config sw> VREF = 0
<config sw> BAUDRATE = 500000
<config sw> DATABIT = 0
<config sw> PARITY = 0
<config sw> TBYTE = 5
<config sw> TFRAME = 4
<config sw> F CAN NUMBER FRAME = 1
<config sw> RANGE =   0,0;
###########################################
#         End of config                   #
###########################################


 
INFO_DATABASE = Req>1\t\t\t000007DF 08 02 01 00 xx xx xx xx xx \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 06 41 00 BF BE B9 93 37 \tNONE\t0\t0

INFO_DATABASE = Req>1\t\t\t000007DF 08 02 01 01 xx xx xx xx xx \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 06 41 01 00 07 65 65 00 \tNONE\t0\t0

INFO_DATABASE = Req>1\t\t\t000007DF 08 02 01 13 xx xx xx xx xx \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 03 41 13 03 00 00 00 00 \tNONE\t0\t0

INFO_DATABASE = Req>1\t\t\t000007DF 08 02 01 20 xx xx xx xx xx \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 06 41 20 A0 05 B0 11 00 \tNONE\t0\t0

INFO_DATABASE = Req>1\t\t\t000007DF 08 02 01 40 xx xx xx xx xx \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 06 41 40 FE D0 04 00 00 \tNONE\t0\t0

INFO_DATABASE = Req>1\t\t\t000007DF 08 02 09 00 xx xx xx xx xx \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 06 49 00 55 00 00 00 00 \tNONE\t0\t0

INFO_DATABASE = Req>1\t\t\t000007DF 08 02 09 02 xx xx xx xx xx \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 10 14 49 02 01 57 41 31 \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 21 43 47 41 46 45 30 42 \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 22 44 30 30 31 35 37 35 \tNONE\t0\t0


INFO_DATABASE = Req>1\t\t\t000007DF 08 01 07 xx xx xx xx xx xx \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 10 84 47 40 {} {} {} {} \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 21 {} {} {} {} {} {} {} \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 22 {} {} {} {} {} {} {} \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 23 {} {} {} {} {} {} {} \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 24 {} {} {} {} {} {} {} \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 25 {} {} {} {} {} {} {} \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 26 {} {} {} {} {} {} {} \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 27 {} {} {} {} {} {} {} \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 28 {} {} {} {} {} {} {} \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 29 {} {} {} {} {} {} {} \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 2A {} {} {} {} {} {} {} \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 2B {} {} {} {} {} {} {} \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 2C {} {} {} {} {} {} {} \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 2D {} {} {} {} {} {} {} \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 2E {} {} {} {} {} {} {} \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 2F {} {} {} {} {} {} {} \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 20 {} {} {} {} {} {} {} \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 21 {} {} {} {} {} {} {} \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 22 {} {} {} {} {} {} {} \tNONE\t0\t0


INFO_DATABASE = Req>1\t\t\t000007DF 08 03 02 xx xx xx xx xx xx \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 07 42 00 00 7E 1F 80 03 \tNONE\t0\t0

INFO_DATABASE = Req>1\t\t\t000007DF 08 01 03 xx xx xx xx xx xx \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 02 43 01 01 00 00 00 00 \tNONE\t0\t0


INFO_DATABASE = Req>1\t\t\t000007DF 08 01 04 00 00 00 00 00 00 \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 01 44 00 00 00 00 00 00 \tNONE\t0\t0


//Livedata
//Engine speed: 19840(0.1RPM)
INFO_DATABASE = Req>1\t\t\t000007DF 08 02 01 XX xx xx xx xx xx \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 06 41 XX 1f 00 00 00 37 \tNONE\t0\t0

//>>Vehicle speed: 1305.00 centimeters/sec
INFO_DATABASE = Req>1\t\t\t000007DF 08 02 01 0D xx xx xx xx xx \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 06 41 0D 2F 00 00 00 37 \tNONE\t0\t0

//>>Throttle Position 1215(0.01%)
INFO_DATABASE = Req>1\t\t\t000007DF 08 02 01 11 xx xx xx xx xx \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 06 41 11 1F 00 00 00 37 \tNONE\t0\t0

//>>Engine Coolant Temperature (ECT)=-304(1/16C)
INFO_DATABASE = Req>1\t\t\t000007DF 08 02 01 05 xx xx xx xx xx \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 06 41 05 15 AA 00 00 37 \tNONE\t0\t0

//>>Fuel level 0.00%
INFO_DATABASE = Req>1\t\t\t000007DF 08 02 01 2F xx xx xx xx xx \tNONE\t0\t0
INFO_DATABASE = Res>1\t\t\t000007E8 08 06 41 2F 00 00 00 00 37 \tNONE\t0\t0


###########################################
#         End of DataBase                 #
###########################################
'''



if __name__ == '__main__':
    '''Test'''
    cap_path = 'CaptureTool 3.0.42\\CaptureTool.exe'
    hwid = '0483:5740'
    cap = CaptureTool(cap_path, hwid)
    cap.run()

    if cap.is_connected():
        sim_path = 'sim\\hello.sim'

        dtcs =['P0002','P0003','P0004']
        create_sim(sim_path, dtcs)

        cap.load(sim_path)
        cap.clear_data()

    time.sleep(2)
    cap.close()
