import json
from agora_config import config
from agora_logging import logger
from .messages import IoDataReportMsg, MessageEncoder, RequestMsg
from .message_queue import MessageQueue
from .mqtt_client import MqttClient


class BusClientSingleton:
    _instance = None
    """
    Connects to the mqtt-net-server and handles sending and receiving messages
    """
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
        

    def __init__(self):
        self.bus = MqttClient()
        self.bus.messages = MessageQueue()
        self.use_data_in = False
        self.use_request_in = False
        self.subscriptions = set()
        config.observe("AEA2::BusClient",self.reconnect)

    @property
    def messages(self):
        return self.bus.messages


    def connect(self, sec: float):
        self.configure()
        self.log_config()
        self.bus.start()
        self.bus.connect(sec)


    def log_config(self):
        logger.info("AEA2:BusClient:")
        logger.info(f"--- Server: {self.bus.server}")
        logger.info(f"--- Port: {self.bus.port}")
        logger.info(f"--- Default DeviceId: {IoDataReportMsg.default_device_id}")
        logger.info(f"--- UseDataIn: {'DataIn' in self.subscriptions}")
        logger.info(f"--- UseRequests: {'RequestIn' in self.subscriptions}")
        logger.info("--- Subscriptions:")
        for sub in self.subscriptions:
            logger.info(f"   --- {sub}")


    def disconnect(self):
        self.bus.disconnect()

        
    def reconnect(self, payload):
        logger.info(f"BusClient: Received new configuration")
        self.configure()
        self.log_config()

    
    def is_connected(self):
        return self.bus.is_connected()
    

    def send_message(self, topic, payload):
        if not self.bus.is_connected():
            logger.error("Cannot send message, BusClient is not connected to the broker")
            return 
        self.bus.send_message(payload,topic)


    def send_data(self, msg: IoDataReportMsg, msgTopic="DataOut"):
        payload = json.dumps(msg, cls=MessageEncoder)
        self.send_message(msgTopic, payload)


    def send_request(self, msg: RequestMsg, msgTopic="RequestOut"):
        payload = json.dumps(msg, cls=MessageEncoder)
        self.send_message(msgTopic, payload)


    def configure(self):
        self.bus.server = config["AEA2:BusClient:Server"]
        if self.bus.send_message == "":
            self.bus.server = "127.0.0.1"

        self.bus.port = config["AEA2:BusClient:Port"]
        if self.bus.port == "":
            self.bus.port = "707"        

        self.subscriptions=set()

        self.use_data_in = bool(config["AEA2:BusClient:UseDataIn"])
        if self.use_data_in:
            self.subscriptions.add("DataIn")

        self.use_request_in = bool(config["AEA2:BusClient:UseRequests"])

        if self.use_request_in:
            self.subscriptions.add("RequestIn")

        str_device_id = config["AEA2:BusClient:DeviceId"]
        try:
            IoDataReportMsg.default_device_id = int(str_device_id)
        except:
            IoDataReportMsg.default_device_id = 999
        
        topics = config["AEA2:BusClient:Subscriptions"]
        if topics != "":
            self.subscriptions.union(set(topics))

        self.bus.update_topics(self.subscriptions)


bus_client = BusClientSingleton()