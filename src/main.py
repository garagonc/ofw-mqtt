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
    #UDP_IP_ADDRESS = "134.130.169.38"
    UDP_IP_ADDRESS = "127.0.0.1"
    UDP_PORT_NO = 12345
    data= b'\x00\x00\x00\x00Bk\x1b\x82B!}uB\x9e\x97iB\x93\xe5\x7f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00?\x80\x00\x00?\x80\x00\x00?\x80\x00\x00?\x80\x00\x00E\xec\x87CE\xda\xa2\xd7E\x91\xd3%E\xa8P\x19D\x01\xa0\xccD\x06\xa1\xe7D\t\xa2~C\xc5y\xfe>a\xd6\x13>a\xb3c>a\xd7f>b\x10\xec<^|\xb0<^|\xaa<^|\xab<^|\xb69Q\xb7\x179Q\xb7\x179Q\xb7\x179Q\xb7\x17;\xf4NI;\xf4Wq;\xf36=;\xf24\x1b\xb5\xa1g\xd3\xb5\xa0\xa0+\xb5\x9f\xe3L\xb5\xa1\xc9\xb4\xa2r\xc5\x10>\x08\xb8\x06>\x82y\x88>\xa0\xf4\x00?\x80\x00\x00?\x80\x00\x00?\x80\x00\x00?\x80\x00\x009Q\xb7\x179Q\xb7\x179Q\xb7\x179Q\xb7\x17F\x9d\xe9\x85CK$^B|d\xb2C\x9d\x14\xf9C\x9d\x14`C\x9d\x13\xe4C\x9d\x13\x88'
    logger.debug("data to send: "+str(data))
    logger.debug("type data to send: " + str(type(data)))
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
    thread_udp_send = Thread(target=send_udp_message(udp_object))
    thread_udp_send.start()
    thread_udp_receive.join()
    thread_udp_send.join()



    while True:
       pass


