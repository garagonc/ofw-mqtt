import struct

from src.utils.config_output import config as config_output
import json
import logging

from src.outputs.outputController import OutputController
from src.utils.updDataConversion import UDPDataConversion

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__file__)


class RTDS_UDPlistener_4Nodes_IST:
    """
    Listen for UDP messages on a given port. IP and port have to be specified in calvin-application file
    Output:
      data_out1 : Data received on the UDP port will be sent as tokens.
      data_out2 : Data received on the UDP port will be sent as tokens.
      data_out3 : Data received on the UDP port will be sent as tokens.
      data_out4 : Data received on the UDP port will be sent as tokens.
      data_outE : Data received on the UDP port will be sent as tokens.
    """

    def __init__(self, max_len):
        logger.debug("Initializing")
        self.listener = None
        self.output_config = config_output
        self.output = OutputController(self.output_config)
        self.NumData = max_len
        # self.receive()

    def receive(self, data):
        self.out = UDPDataConversion.convert_from_udf_data(data, self.NumData)
        self.share_senml()

    def share_senml(self):
        data_out = {}
        # _log.debug("config: " + json.dumps(self.output_config, indent=4, sort_keys=True))
        for key, value in self.output_config.items():
            # _log.debug("key: " + str(key))
            for key2, value2 in value.items():
                # _log.debug("counter: " + str(value2["position"]) + " key " + str(key) + " key2 " + str(key2) + " data " + str(self.out[value2["position"]]))
                data_out[key2] = self.out[value2["position"]]

        logger.debug("data out: " + json.dumps(data_out, indent=4, sort_keys=True))
        self.output.publishController(data_out)