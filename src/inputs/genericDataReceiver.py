"""
Created on Aug 10 12:11 2018

@author: nishit
"""
import logging

from inputs.baseDataReceiver import BaseDataReceiver

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__file__)

class GenericDataReceiver(BaseDataReceiver):

    def __init__(self,config_input):
        super().__init__(config_input)

    def unit_value_change(self, value, unit):
        return value