"""
Created on Apr 10 11:42 2019

@author: nishit
"""
import logging
import struct


logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__file__)

class UDPDataConversion:

    @staticmethod
    def tofloat(data):
        x = struct.unpack('>f', data)[0]
        #x = struct.unpack('>f', struct.pack('4B', *data))[0]
        return x

    @staticmethod
    def convert_from_udf_data(data, num_data):
        out = [0] * num_data
        for i in range(0, num_data):
            out[i] = UDPDataConversion.tofloat(data[(4 * i):(4 + 4 * i)])
        logger.info("received: " + str(out) + " type " + str(type(out)))
        return out

    @staticmethod
    def fromfloat(data):
        x = struct.pack('>f', data)
        return x

    @staticmethod
    def convert_to_udf_data(data):
        out = None
        for i in range(0, len(data)):
            if out is None:
                out = UDPDataConversion.fromfloat(data[i])
            else:
                out += UDPDataConversion.fromfloat(data[i])
        logger.info("received: " + str(out) + " type " + str(type(out)) + " len " + str(len(out)))
        return out