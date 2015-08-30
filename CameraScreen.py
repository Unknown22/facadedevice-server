# Imports
import time
import numpy

from PyTango import AttrQuality, AttrWriteType, DispLevel, DevState, DebugIt
from PyTango.server import Device, DeviceMeta, attribute, command, run
from PyTango.server import device_property

from facadedevice import Facade, FacadeMeta
from facadedevice import device as proxy_module
from facadedevice import proxy_command, proxy_attribute
from facadedevice import proxy, logical_attribute


# Example
class CameraScreen(Facade):
    __metaclass__ = FacadeMeta

    # Proxy
    PLCDevice = proxy("PLCDevice")

    # Proxy attributes
    StatusIn = proxy_attribute(
        device="OPCDevice",
        attr="InStatusTag",
        dtype=bool)

    StatusOut = proxy_attribute(
        device="OPCDevice",
        attr="OutStatusTag",
        dtype=bool)

    # Logical attributes
    @logical_attribute(dtype=bool)
    def Error(self, data):
        return data["StatusIn"] == data["StatusOut"]

    # Proxy commands
    MoveIn = proxy_command(
        device="OPCDevice",
        attr="InCmdTag",
        value=1)

    MoveOut = proxy_command(
        device="OPCDevice",
        attr="OutCmdTag",
        value=1)

    # State
    def state_from_data(self, data):
        if data['Error']:
            return DevState.FAULT
        return DevState.INSERT if data['StatusIn'] else DevState.EXTRACT

    # Status
    def status_from_data(self, data):
        if data['Error']:
            return "Conflict between IN and OUT informations"
        return "IN" if data['StatusIn'] else "OUT"

    @command
    def Reset(self):
        self.devices["PLCDevice"].Reset()

if __name__ == "__main__":
    run([CameraScreen])