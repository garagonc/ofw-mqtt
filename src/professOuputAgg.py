"""
Created on Apr 08 14:26 2019

@author: nishit
"""
import logging
import threading

import time

from src.inputs.inputController import InputController
from src.utils.updDataConversion import UDPDataConversion

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__file__)

class ProfessOutputAgg(threading.Thread):

    def __init__(self, config, udp, max_len):
        super().__init__()
        self.input_controler = InputController(config)
        self.upd = udp
        self.max_len = max_len
        self.config = config
        self.positions = {}
        self.build_position_map(self.config)
        logger.info("position map = "+ str(self.positions))

    def build_position_map(self, data):
        if data is not None and isinstance(data, dict):
            for key, val in data.items():
                if isinstance(val, dict):
                    if "position" in val.keys():
                        self.positions[key] = int(val["position"])
                    else:
                        self.build_position_map(val)

    def run(self):
        while True:
            logger.info("@@@@@@@@ run ")
            data = self.input_controler.get_data()
            logger.info("######################################")
            logger.info(data)
            data = self.aggregate(data)
            logger.info(data)
            data = self.to_upd(data)
            self.upd_send_message(data)
            time.sleep(30)


    def aggregate(self, raw_data):
        data = [0] * self.max_len
        for key, val in raw_data.items():
            if key in self.positions.keys():
                data[self.positions[key]] = float(val[0])
        return data

    def to_upd(self, data):
        data = UDPDataConversion.convert_to_udf_data(data)
        return data

    def upd_send_message(self, data):
        self.upd.send_message(data, )