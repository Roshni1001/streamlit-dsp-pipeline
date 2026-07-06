import machine
import utime
# Import the custom class from your second project file
from network_handler import TrafficMQTTBridge

# --- Hardware Assignments ---
pot_sensor = machine.ADC(26)      # Replaced Hall sensor with Potentiometer
indicator_led = machine.Pin(14, machine.Pin.OUT)

# --- Initialize Custom Network Module ---
bridge = TrafficMQTTBridge()
bridge.connect_wifi()
bridge.connect_broker()

# --- DSP State Tracking ---
history = []
M_WINDOW = 20
THRESHOLD = 15000  # Adjusted threshold for raw 16-bit ADC inputs (0-65535)

print("\n--- Processing Loop Started. Turn Potentiometer Dial to simulate vehicles ---")

while True:
    # 1. Ingest physical sensor voltage component values
    raw_val = pot_sensor.read_u16()
    
    # 2. Dynamic Baseline Drift Estimation
    history.append(raw_val)
    if len(history) > M_WINDOW:
        history.pop(0)
    baseline = sum(history) / len(history)
    corrected_val = abs(raw_val - baseline)
    
    # 3. Decision Logic Threshold Verification
    event_flag = 0
    if corrected_val > THRESHOLD:
        indicator_led.value(1)  # Fire visual hardware layout change
        event_flag = 1
    else:
        indicator_led.value(0)
        
    # 4. Stream across the network bridge module
    bridge.send_telemetry(raw_val, corrected_val, event_flag)
    
    # Pace loop execution to 10Hz to prevent internet packet crowding
    utime.sleep(0.1)