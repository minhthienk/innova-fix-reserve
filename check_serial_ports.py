
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

for port, desc, hwid in check_available_ports():
    print('port', port)
    print('desc', desc)
    print('hwid', hwid)
    print('\n')


'''
1A86:7523 => driver
125E:2806 => bosch
0483:5740 => capture
'''