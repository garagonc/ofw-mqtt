"""
Created on Jul 16 14:13 2018

@author: nishit
"""
import json
import logging

import os
import re

import datetime
from math import floor, ceil
from inputs.genericDataReceiver import GenericDataReceiver

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__file__)


class InputController:

    def __init__(self, config_input=None):
        self.stop_request = False
        self.config = config_input
        self.generic_data_receiver = {}
        self.start_receivers()
        self.optimization_data = {}

    def start_receivers(self):
        for key, value in self.config.items():
            # logger.debug("key " + str(key) + " value " + str(value))
            for name, value2 in value.items():
                # logger.debug("key2 "+str(key2)+" value2 "+str(value2))
                for key3, value3 in value2.items():
                    logger.debug("key3 " + str(key3) + " value3 " + str(value3))
                    if key3 == "mqtt":
                        self.generic_data_receiver[name] = GenericDataReceiver(value3)

        # self.internal_receiver[name] = GenericDataReceiver()

    def parse_input_config(self):
        return 1

    def get_data(self):
        success = False
        while not success:
            success = self.fetch_mqtt_and_file_data(self.generic_data_receiver)
        return self.optimization_data.copy()
    
    def fetch_mqtt_and_file_data(self, receivers):
        for name in receivers.keys():
            logger.debug("mqtt True " + str(name))
            data = receivers[name].get_data()
            self.optimization_data.update(data)
        return True

    
    def Stop(self):
        self.stop_request = True
        logger.debug("generic receiver exit start")
        self.exit_receiver(self.generic_data_receiver)

    def exit_receiver(self, receiver):
        if receiver is not None:
            for name in receiver.keys():
                receiver[name].exit()

    def _compose_command(self):
        # Send power sharing coefficients to RTDS
        # LV Breaker Status
        # data=m1+Ppv_new
        data = self.m1 + self.Ppv_new + self.Qpv_new + self.PV_switch + self.B_switch + self.A_switch + self.Charge
        return data
