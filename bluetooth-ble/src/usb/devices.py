from typing import Callable
import pyudev
from pyudev import Device

from log import log_line


class DeviceRegistration:

    def __init__(self, device_registration: Callable[[Device], None]):
        self.device_registration = device_registration
        context = pyudev.Context()
        monitor = pyudev.Monitor.from_netlink(context)
        monitor.filter_by(subsystem='input')
        observer = pyudev.MonitorObserver(monitor, self.device_event)
        observer.start()

        for device in context.list_devices(subsystem='input'):
            device_registration(device)

    def device_event(self, event, device):
        if (event == "add"):
            self.device_registration(device)
        log_line(event+":"+str(device))
