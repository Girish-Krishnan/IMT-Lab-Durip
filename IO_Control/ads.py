import time
import board
import busio
import digitalio

from adafruit_mcp230xx.mcp23017 import MCP23017
from adafruit_ads1x15.ads1015 import ADS1015
from adafruit_ads1x15.analog_in import AnalogIn

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize MCP23017 at 0x20
mcp = MCP23017(i2c, address=0x20)

# Set up A0-A7 as outputs
mcp_pins = []
for pin_num in range(8):
    pin = mcp.get_pin(pin_num)
    pin.direction = digitalio.Direction.OUTPUT
    pin.value = False  # start LOW
    mcp_pins.append(pin)

# Initialize ADS1015s at 0x48 and 0x49
ads1 = ADS1015(i2c, address=0x48)
ads2 = ADS1015(i2c, address=0x49)

# Create AnalogIn channels
ads1_channels = [AnalogIn(ads1, ch) for ch in [0,1,2,3]]
ads2_channels = [AnalogIn(ads2, ch) for ch in [0,1,2,3]]

# Define voltage threshold (adjust as needed)
VOLTAGE_THRESHOLD = 1.5

try:
    while True:
        # Read from ADS1 (map to A0–A3)
        print("ADS1015 #1 readings:")
        for i, ch in enumerate(ads1_channels):
            voltage = ch.voltage
            mcp_pins[i].value = voltage > VOLTAGE_THRESHOLD
            print(f"  Channel {i}: {voltage:.3f} V → {'HIGH' if mcp_pins[i].value else 'LOW'} on A{i}")

        # Read from ADS2 (map to A4–A7)
        print("ADS1015 #2 readings:")
        for i, ch in enumerate(ads2_channels):
            voltage = ch.voltage
            mcp_pins[i + 4].value = voltage > VOLTAGE_THRESHOLD
            print(f"  Channel {i}: {voltage:.3f} V → {'HIGH' if mcp_pins[i + 4].value else 'LOW'} on A{i + 4}")

        print("\n--- Waiting 1 second ---\n")
        time.sleep(1)

except KeyboardInterrupt:
    print("\nExiting cleanly...")
