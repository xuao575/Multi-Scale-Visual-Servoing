import serial
import time


class COM:
    def __init__(self, port, baud):
        self.port = port
        self.baud = baud
        self.open_com = None
        self.get_data_flag = True
        self.real_time_data = ''

    # return real time data from com
    def get_real_time_data(self):
        return self.real_time_data

    def clear_real_time_data(self):
        self.real_time_data = ''

    # set flag to receive data or not
    def set_get_data_flag(self, get_data_flag):
        self.get_data_flag = get_data_flag

    def open(self):
        try:
            self.open_com = serial.Serial(self.port, self.baud)
        except Exception as e:
            print('Find error in opening com.', e)

    def close(self):
        if self.open_com is not None and self.open_com.isOpen:
            self.open_com.close()

    def send_data(self, data):
        if self.open_com is None:
            self.open()
        print(self.port)
        success_bytes = self.open_com.write(data.encode('UTF-8'))  # .encode('UTF-8')
        return success_bytes

    def get_data(self, over_time=5):
        all_data = ''
        if self.open_com is None:
            self.open()
        start_time = time.time()
        while True:
            end_time = time.time()
            if end_time - start_time < over_time and self.get_data_flag:
                data = self.open_com.read(self.open_com.inWaiting()).decode("gbk")
                data = str(data)
                if data != '':
                    # print(data)
                    all_data = all_data + data
                    self.real_time_data = all_data
                    self.get_data_flag = False
            else:
                self.set_get_data_flag(True)
                break

        return all_data



