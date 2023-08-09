# this script is for usb port connection

import time
import threading
import serial.tools.list_ports


# class for serial communication with the cat via usb
class USB_cats:

    def __init__(self):
        self.ports_dict = {}
        self.available = 0
        self.right = []
        self.left = []
        self.running = False
        self.get_devices()

        x = threading.Thread(target=self.monitor_ports, args=(), daemon=True)
        x.start()

    # finds connected devices and sorts them into left and right
    def get_devices(self):

        self.running = True
        self.ports_dict = {}

        ports_object = serial.tools.list_ports.comports()
        self.available = len(ports_object)
        print(f'available_usb-cats: {self.available}')

        for i in range(self.available):

            str_port = str(ports_object[i])
            # print(str_port)

            split_port = str_port.split(' ')
            comm_port = (split_port[0])

            serial_comm = serial.Serial(comm_port, baudrate=115200, timeout=1)
            serial_comm.write('are_you_a_cat'.encode())
            serial_comm.flush()

            time.sleep(0.1)

            cat_version = serial_comm.readline().decode("utf-8")[:-2]
            serial_comm.close()
            print(f'cat_version: >{cat_version}<')

            if not cat_version:
                print('>cat_version< is empty')
            else:
                self.ports_dict[cat_version] = comm_port

        self.right.clear()
        self.left.clear()

        for device in list(self.ports_dict.keys()):    # sort devices
            if 'CL' in device:
                self.left.append(device)
            else:
                self.right.append(device)

        self.running = False

    # monitors usb ports for changes
    def monitor_ports(self):
        ports_count_old = len(serial.tools.list_ports.comports())
        while True:
            time.sleep(0.5)
            ports_count = len(serial.tools.list_ports.comports())
            # print(f'ports count {ports_count}')
            if ports_count != ports_count_old:
                ports_count_old = ports_count
                self.get_devices()


devices = USB_cats()


# print(usb_cats)
# print(devices.left)
# print(devices.right)