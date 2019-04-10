import json
import logging

import time

#from senml import senml
import senml as senml

from src.communications.MQTTClient import MQTTClient


logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__file__)

class OutputController:

    def __init__(self, output_config=None):
        logger.info("Output Class started")
        self.output_config=output_config
        self.mqtt={}
        self.output_mqtt = {}
        self.client_id = "IST_Optimization"

        if output_config is not None:
            self.init_mqtt()

    def init_mqtt(self):
        ###Connection to the mqtt broker
        try:
            for key, value in self.output_config.items():
                for key2, value2 in value.items():
                    if (value2["mqtt"]["host"] or value2["mqtt"]["host"].isspace()):
                        host = value2["mqtt"]["host"]
                        topic = value2["mqtt"]["topic"]
                        qos = 0
                        if "qos" in value2["mqtt"]:
                            qos = value2["mqtt"]["qos"]
                        self.output_mqtt[key2] = {"host": host, "topic": topic, "qos": qos}
                        if bool(self.mqtt):
                            if host in self.mqtt:
                                logger.debug("Already connected to the host " + host)
                            else:
                                logger.debug("Creating mqtt client with the host: " + str(host))
                                self.mqtt[str(host)] = MQTTClient(str(host), 1883, self.client_id)
                        else:
                            logger.debug("Creating mqtt client with the host: " + str(host))
                            self.mqtt[str(host)] = MQTTClient(str(host), 1883, self.client_id)
                            logger.debug("Self.mqtt: " + str(self.mqtt))
        except Exception as e:
            logger.error(e)



    def publishController(self, data):
        current_time = int(time.time())
        senml_data = self.senml_message_format(data, current_time)
        #logger.debug("senml: " + json.dumps(senml_data, indent=4, sort_keys=True))
        try:
            for key, value in senml_data.items():
                v = json.dumps(value)
                if key in self.output_mqtt.keys():
                    value2 = self.output_mqtt[key]
                    topic = value2["topic"]
                    host = value2["host"]
                    qos = value2["qos"]
                    self.mqtt[str(host)].sendResults(topic, v,qos)
        except Exception as e:
            logger.error(e)



    def senml_message_format(self, data, time):
        new_data = {}
        u = "W"
        for key, value in data.items():
            #logger.debug("key: "+str(key)+" value "+str(value))
            meas_list = []
            meas = senml.SenMLMeasurement()
            meas.name = key
            meas.time = time
            meas.value = value
            meas.unit = u
            meas_list.append(meas)
            doc = senml.SenMLDocument(meas_list)
            new_data[key] = doc.to_json()
        #logger.debug("Topic MQTT Senml message: "+str(new_data))
        return new_data



