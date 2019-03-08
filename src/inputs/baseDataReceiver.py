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

from inputs.dataReceiver import DataReceiver

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
            self.data.update(formated_data)
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
            doc.measurements = sorted(doc.measurements, key=lambda x: x.time)
            bucket = 0
            if len(doc.measurements) > 0:
                self.length = len(doc.measurements)
                meas = doc.measurements[0]
                bucket = self.time_to_bucket(meas.time)
            for meas in doc.measurements:
                n = meas.name
                u = meas.unit
                v = meas.value
                t = meas.time
                if not u:
                    u = bu
                # dont check bn
                """
                if bn and n and bn != n:
                    n = bn + n
                """
                if not n:
                    """
                    if not bn:
                        n = self.generic_name
                    else:
                        n = bn
                    """
                    n = self.generic_name
                try:
                    v = self.unit_value_change(v, u)
                    bucket_key = str(self.current_day_index) + "_" + str(bucket)
                    bucket += 1
                    if bucket >= self.total_steps_in_day:
                        bucket = 0
                        self.current_day_index += 1
                        if self.current_day_index >= self.number_of_bucket_days:
                            self.current_day_index = 0
                    data[bucket_key] = v
                    """
                    if n not in index.keys():
                        index[n] = 0
                    if n not in data.keys():
                        data[n] = {}
                    data[n][index[n]] = v
                    index[n] += 1
                    """
                except Exception as e:
                    logger.error("error " + str(e) + "  n = " + str(n))
            logger.debug("data: " + str(data))
            return data
        return {}

    @abstractmethod
    def unit_value_change(self, value, unit):
        pass

