import logging
from communications.udp_interpreter import UDP_Interpreter as udp
from inputs.inputController import InputController
from utils.config_input import config
import time
from threading import Thread

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__file__)

def send_udp_message(udp_object):
    logger.debug("UDP sender started")
    UDP_IP_ADDRESS = "127.0.0.1"
    UDP_PORT_NO = 6789
    data=[]
    for x in range(1,61):
        data.append(x)
    logger.debug("data to send: "+str(data))
    Message = data
    while True:
        logger.debug("Sending message through UDP")
        udp_object.send_message(Message,UDP_IP_ADDRESS, UDP_PORT_NO)
        time.sleep(10)


if __name__ == '__main__':
    """
        format:
        api_category command_name required args 
        eg:
        
    """

    logger.info("Service started")

    input_controller = InputController(config)


    udp_object = udp()
    thread_udp_receive = Thread(target=udp_object.udp_receive)
    thread_udp_receive.start()
    logger.debug("Receive thread started")
    #thread_udp_send = Thread(target=send_udp_message(udp_object))
    #thread_udp_send.start()
    thread_udp_receive.join()
    #thread_udp_send.join()



    while True:
       pass


