#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
import numpy

from PyTango import AttrQuality, AttrWriteType, DispLevel, DevState, DebugIt
from PyTango.server import Device, DeviceMeta, attribute, command, run
from PyTango.server import device_property

from facadedevice import Facade, FacadeMeta
from facadedevice import device as proxy_module
from facadedevice import proxy_command, proxy_attribute
from facadedevice import proxy, logical_attribute

class FacadeServer(Device):
    __metaclass__ = DeviceMeta


#     Status = proxy_attribute(device="elin",
#                              attr="Current",
#                              dtype=float)

    
    current = attribute(label="Current", dtype=float,
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ_WRITE,
                        unit="A",format="8.4f",
#                         min_value=0.0, max_value=8.5,
#                         min_alarm=0.1, max_alarm=8.4,
#                         min_warning=0.5, max_warning=8.0,
                        fget="get_current",
                        fset="set_current",
                        doc="current")
 
#     noise = attribute(label="Noise",
#                       dtype=((int,),),
#                       max_dim_x=1024, max_dim_y=1024)
# 
    host = device_property(dtype=str)
    port = device_property(dtype=int, default_value=9788)
    
    def init_device(self):
        Device.init_device(self)
        self.__current = 223
        self.set_state(DevState.STANDBY)
  
    def get_current(self):
        return self.__current
   
    def set_current(self, current):
        # should set the power supply current
        self.__current = current
 
    @DebugIt()
    def read_noise(self):
        return numpy.random.random_integers(1000, size=(100, 100))

    @command
    def TurnOn(self):
        # turn on the actual power supply here
        self.set_state(DevState.ON)

    @command
    def TurnOff(self):
        # turn off the actual power supply here
        self.set_state(DevState.OFF)
        
    @command(dtype_in=float, doc_in="Ramp target current",
             dtype_out=bool, doc_out="True if ramping went well, False otherwise")
    def Ramp(self, target_current):
        # should do the ramping
        return True
    

if __name__ == "__main__":
    run([FacadeServer])