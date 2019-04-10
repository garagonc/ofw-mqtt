import socket
import logging
from src.outputs.RTDS_UDPlistener_4Nodes_IST import RTDS_UDPlistener_4Nodes_IST as listener
import pickle

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__file__)


class UDP_Interpreter:

    def __init__(self, ip_address, udp_port, max_len):
        self.clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listener = listener(max_len)
        self.ip_address = ip_address
        # UDP_IP_ADDRESS = "134.130.169.38"
        self.udp_port = udp_port
        self.create_server()
        logger.debug("Creating udp object")
    def send_message(self, message):

        if isinstance(message, list):
            message = pickle.dumps(message)
            self.clientSock.sendto(message, (self.ip_address, self.udp_port))
        elif isinstance(message, bytes):
            self.clientSock.sendto(message, (self.ip_address, self.udp_port))
        else:
            self.clientSock.sendto(message.encode('utf-8'), (self.ip_address, self.udp_port))

    def create_server(self):
        logger.debug("Starting UDP server")
        # declare our serverSocket upon which
        # we will be listening for UDP messages
        self.serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # One difference is that we will have to bind our declared IP address
        # and port number to our newly declared serverSock
        self.serverSock.bind((self.ip_address, self.udp_port))
        logger.debug("UDP Server started")

    def udp_receive(self):
        logger.debug("Starting UDP receive")
        while True:
            data, addr = self.serverSock.recvfrom(4096)
            # logger.debug("type data: "+str(type(data)))
            # data=data.decode('utf-8')
            # data=pickle.loads(data)
            logger.debug("Data received @@: "+str(data))
            self.listener.receive(data)
