from pyb import USB_VCP
import time

usb = USB_VCP()

while True:
    if (usb.isconnected()):
        usb.write('f')
        time.sleep(5)
