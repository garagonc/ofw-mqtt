"""
Created on Jun 27 17:36 2018

@author: nishit
"""

import logging

import time
from abc import ABC, abstractmethod

from random import randrange

from communications.MQTTClient import MQTTClient

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__file__)


class DataReceiver(ABC):

    def __init__(self, topic_params, emptyValue={}):
        super().__init__()
        self.stop_request = False
        self.topic_params = topic_params
        self.emptyValue = emptyValue
        self.data = self.emptyValue.copy()
        self.data_update = False
        self.channel = "MQTT"
        self.topics = None
        self.port = None
        self.host_params = {}

        self.setup()

        self.init_mqtt(self.topics)

    def setup(self):
        self.topics = self.get_internal_channel_params()




    def get_internal_channel_params(self):
        if self.channel == "MQTT":
            topic_qos = []
            host_params = {}
            for k, v in self.topic_params.items():
                if k == "topic":
                    topic_qos.append((v,1))
                elif k == "port":
                    self.port = v
                elif k == "host":
                    self.host = v
            logger.debug("host "+str(self.host))
            logger.debug("port "+str(self.port))
            logger.debug("topic " + str(topic_qos))


            return topic_qos

    def init_mqtt(self, topic_qos):
        logger.info("Initializing mqtt subscription client")
        #if we set it to false here again then it may overwrite previous true value
        #self.redisDB.set("Error mqtt"+self.id, False)
        try:
            if not self.port:
                self.port = 1883
                #read from config
            self.client_id = "client_receive" + str(randrange(100000)) + str(time.time()).replace(".","")
            self.mqtt = MQTTClient(str(self.host), self.port, self.client_id)
            self.mqtt.subscribe(topic_qos, self.on_msg_received)
            while not self.mqtt.subscribe_ack_wait():
                self.mqtt.subscribe(topic_qos, self.on_msg_received)
                logger.error("Topic subscribe missing ack")

            logger.info("successfully subscribed")
        except Exception as e:
            logger.error(e)
            # error for mqtt will be caught by parent
            raise e

    @abstractmethod
    def on_msg_received(self, payload):
        pass

    def get_mqtt_data(self, require_updated, clearData):
        if require_updated == 1 and not self.data:
            require_updated = 0
        while require_updated == 0 and not self.data_update and not self.stop_request:
            logger.debug("wait for data")
            time.sleep(0.5)
        return self.get_and_update_data(clearData)

    def exit(self):
        self.stop_request = True
        if self.channel == "MQTT":
            self.mqtt.MQTTExit()
        logger.info("InputController safe exit")



    def get_and_update_data(self, clearData):
        new_data = self.data.copy()
        self.data_update = False
        if clearData:
            self.data = self.emptyValue.copy()
        return new_data

    def get_data(self, require_updated=0, clearData=False):
        """

        :param require_updated: 0 -> wait for new data
                                1 -> wait for new data if no prev data
                                2 -> return prev data, even if empty
        :return:
        """
        data = {}
        if self.channel == "MQTT":
            data = self.get_mqtt_data(require_updated, clearData)

        return data
