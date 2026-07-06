import network
import utime
from umqtt.simple import MQTTClient

class TrafficMQTTBridge:
    def __init__(self, client_id="iitm_dsp_node", broker="broker.hivemq.com"):
        self.client_id = client_id
        self.broker = broker
        self.topic = "iitm/dsp/traffic_telemetry"
        self.client = None

    def connect_wifi(self, ssid="Wokwi-GUEST", password=""):
        print("Connecting to Virtual Wi-Fi...")
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            utime.sleep_ms(100)
        print("Connected! IP Assigned:", wlan.ifconfig()[0])

    def connect_broker(self):
        print("Connecting to MQTT Router...")
        self.client = MQTTClient(self.client_id, self.broker)
        self.client.connect()
        print("MQTT Operational. Streaming active.")

    def send_telemetry(self, raw, corrected, flag):
        """Sends clean CSV packages to Streamlit"""
        payload = f"{raw},{corrected},{flag}"
        try:
            self.client.publish(self.topic, payload)
        except Exception:
            # Automatic reconnection fallback if broker times out
            try:
                self.client.connect()
            except:
                pass