import sys
import os
from os import path
from sim_template import sim_template
from dtc_converter import dtc2hex
import autoit


import serial
import serial.tools.list_ports

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
    """docstring for CaptureTool"""
    def __init__(self, path, hwid, autoit_exe_path):
        self.path = path
        self.port = ser_hwid_to_port(hwid)
        self.handle = None
        self.autoit_exe_path = autoit_exe_path

    def write_cmd(self, cmd):
        with open('temp', 'w') as file_object:
            file_object.write(cmd)


    def read_cmd_result(self):
        with open('temp', 'r') as file_object:
            result = file_object.read()
        return result

    def run(self):
        #create sim folder
        if not os.path.exists('sim'):
            os.mkdir('sim')
        #create init sim file
        with open('sim\\capinit.sim', 'w') as file_object:
            file_object.write('')

        cmd = 'RUN' + '\n'
        cmd += self.path + '\n'
        cmd += self.port
        self.write_cmd(cmd)
        os.system(self.autoit_exe_path)

        if 'successful' in self.read_cmd_result():
            self.handle = self.read_cmd_result().replace('run successful: ','')
        return self.read_cmd_result()


    def load(self, sim_path):
        if self.handle!=None:

            cmd = 'LOAD' + '\n'
            cmd += self.handle + '\n'
            cmd += sim_path
            self.write_cmd(cmd)
            os.system(self.autoit_exe_path)
            return self.read_cmd_result()
        else:
            return 'capture load failed: no handle'

    def is_data_existing(self):
        if self.handle!=None:
            cmd = 'IS_DATA_EXISTING' + '\n'
            cmd += self.handle + '\n'
            self.write_cmd(cmd)
            os.system(self.autoit_exe_path)
            if self.read_cmd_result()=='true':
                return True
            else:
                return False
        else:
            return 'capture load failed: no handle'

    def clear_data(self):
        if self.handle!=None:
            cmd = 'CLEAR_DATA' + '\n'
            cmd += self.handle + '\n'
            self.write_cmd(cmd)
            os.system(self.autoit_exe_path)
            return self.read_cmd_result()
        else:
            return 'capture load failed: no handle'



if __name__ == '__main__':
    cap_path = 'CaptureTool 3.0.42\\CaptureTool.exe'
    com_port = 'COM6'
    cap = CaptureTool(cap_path, com_port)
    cap.run()


    dtcs =['P0000','P0001','P0002']
    create_sim('sim\\hello.sim', dtcs)
    cap.load('hello.sim')
    print(cap.is_data_existing())
    cap.clear_data()

