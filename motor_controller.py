from serialport import COM

motor_com = COM('COM4', 9600)
motor_com.open()
try:
    motor_com.send_data('01450\n')
except:
    print('did not send')
finally:
    motor_com.close()
