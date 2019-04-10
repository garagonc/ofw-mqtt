"""
Created on Aug 13 11:03 2018

@author: nishit
"""
import json
import logging
from abc import ABC, abstractmethod

import datetime
from math import floor

from senml import senml

from src.inputs.dataReceiver import DataReceiver

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__file__)


class BaseDataReceiver(DataReceiver, ABC):

    def __init__(self, config_input):

        try:
            super().__init__(config_input)
        except Exception as e:
            logger.error(e)


    def on_msg_received(self, payload):
        try:
            logger.debug("payload "+str(payload))
            self.start_of_day = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
            senml_data = json.loads(payload)
            formated_data = self.add_formated_data(senml_data)
            self.data = formated_data.copy()
            logger.debug("data "+str(self.data))
            self.data_update = True
        except Exception as e:
            logger.error(e)

    def add_formated_data(self, json_data):
        doc = None
        try:
            doc = senml.SenMLDocument.from_json(json_data)
        except Exception as e:
            pass
        if not doc:
            try:
                meas = senml.SenMLMeasurement.from_json(json_data)
                doc = senml.SenMLDocument([meas])
            except Exception as e:
                pass
        if doc:
            base_data = doc.base
            bn, bu = None, None
            if base_data:
                bn = base_data.name
                bu = base_data.unit
            data = {}
            index = {}
            doc.measurements = sorted(doc.measurements, key=lambda x: x.time)
            for meas in doc.measurements:
                n = meas.name
                u = meas.unit
                v = meas.value
                t = meas.time
                if not u:
                    u = bu
                # dont check bn
                if not n:
                    n = self.generic_name
                try:
                    v = self.unit_value_change(v, u)
                    if n not in index.keys():
                        index[n] = 0
                    if n not in data.keys():
                        data[n] = {}
                    data[n][index[n]] = v
                    index[n] += 1
                except Exception as e:
                    logger.error("error " + str(e) + "  n = " + str(n))
            logger.debug("data: " + str(data))
            return data
        return {}

    @abstractmethod
    def unit_value_change(self, value, unit):
        pass

