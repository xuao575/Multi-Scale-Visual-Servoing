from serialport import *

motor_com = COM('COM4', 9600)
motor_com.open()
motor_com.send_data('10900\n')
# while motor_com.get_data(over_time=10) == '':
#     motor_com.send_data('11800\n')
