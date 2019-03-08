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

        self.start_receivers()

    def start_receivers(self):
        self.internal_receiver = {}
        for key, value in self.config.items():
            #logger.debug("key " + str(key) + " value " + str(value))
            for name, value2 in value.items():
                #logger.debug("key2 "+str(key2)+" value2 "+str(value2))
                for key3, value3 in value2.items():
                    logger.debug("key3 " + str(key3) + " value3 " + str(value3))
                    if key3 == "mqtt":
                        self.internal_receiver[name]=GenericDataReceiver(value3)

        #self.internal_receiver[name] = GenericDataReceiver()




    def parse_input_config(self):
        return 1




    def get_data(self):
        success = False
        while not success:
            current_bucket = self.get_current_bucket()
            logger.info("Get input data for bucket "+str(current_bucket))
            success = self.fetch_mqtt_and_file_data(self.prediction_mqtt_flags, self.internal_receiver, [], [], current_bucket)
            if success:
                success = self.fetch_mqtt_and_file_data(self.non_prediction_mqtt_flags, self.internal_receiver, [], [], current_bucket)
            if success:
                success = self.fetch_mqtt_and_file_data(self.external_mqtt_flags, self.external_data_receiver, [], ["SoC_Value"], current_bucket)
            if success:
                success = self.fetch_mqtt_and_file_data(self.generic_data_mqtt_flags, self.generic_data_receiver, [], [], current_bucket)
        return {None: self.optimization_data.copy()}



    def Stop(self):
        self.stop_request = True
        logger.debug("internal receiver exit start")
        self.exit_receiver(self.internal_receiver)
        logger.debug("external receiver exit start")
        self.exit_receiver(self.external_data_receiver)
        logger.debug("generic receiver exit start")
        self.exit_receiver(self.generic_data_receiver)

    def exit_receiver(self, receiver):
        if receiver is not None:
            for name in receiver.keys():
                receiver[name].exit()

    def set_indexing(self, data):
        new_data = {}
        for name, value in data.items():
            indexing = self.input_config_parser.get_variable_index(name)
            # default indexing will be set to "index" in baseDataReceiver
            if indexing == "None":
                if len(value) >= 1:
                    if isinstance(value, dict):
                        v = value[0]  # 0 is the key
                        new_data[name] = {None: v}
        data.update(new_data)
        return data

    def get_current_bucket(self):
        start_of_day = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        current_time = datetime.datetime.now()
        bucket = floor((current_time - start_of_day).total_seconds() / self.dT_in_seconds)
        if bucket >= self.steps_in_day:
            bucket = self.steps_in_day - 1
        return bucket

    def _compose_command(self):
        # Send power sharing coefficients to RTDS
        # LV Breaker Status
        # data=m1+Ppv_new
        data = self.m1 + self.Ppv_new + self.Qpv_new + self.PV_switch + self.B_switch + self.A_switch + self.Charge
        return data