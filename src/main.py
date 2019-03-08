import logging
from communications.udp_interpreter import UDP_Interpreter as udp
from inputs.dataReceiver import DataReceiver as MQTT_Data_Receiver
import time
from threading import Thread

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__file__)

def send_udp_message(udp_object):
    logger.debug("UDP sender started")
    UDP_IP_ADDRESS = "127.0.0.1"
    UDP_PORT_NO = 6789
    Message = "Hello, Server"
    while True:
        logger.debug("Sending message through UDP")
        udp_object.send_message(Message,UDP_IP_ADDRESS, UDP_PORT_NO)
        time.sleep(5)


if __name__ == '__main__':
    """
        format:
        api_category command_name required args 
        eg:
        
    """

    logger.info("Service started")



    udp_object = udp()
    thread_udp_receive = Thread(target=udp_object.udp_receive)
    thread_udp_receive.start()
    logger.debug("Receive thread started")
    #thread_udp_send = Thread(target=send_udp_message(udp_object))
    #thread_udp_send.start()
    thread_udp_receive.join()
    #thread_udp_send.join()

    MQTT_Receiver = MQTT_Data_Receiver(optimization_data)
    while True:
       pass


