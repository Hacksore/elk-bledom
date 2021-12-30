from bluepy.btle import Peripheral, ADDR_TYPE_PUBLIC
import lightutil

# Found some info here
# https://github.com/arduino12/ble_rgb_led_strip_controller
SERVICE_UUID = "0000fff0-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_UUID = "0000fff3-0000-1000-8000-00805f9b34fb"

MAX_CONNECTIONS = 20

class Light:
    def __init__(self, address, interface=0):
        self.peripheral = None
        self.device = None
        self.address = address
        self.interface = interface
        self.state = None
        self.connection_attempts = 0
        self.connected = False

    def setup(self):
        print("attempt", str(self.connection_attempts))
        self.connection_attempts = self.connection_attempts + 1

        # Don't attempt to connect if we reach max connections
        if (self.connection_attempts >= MAX_CONNECTIONS):
            return

        self.peripheral = Peripheral(self.address, iface=self.interface)
        self.service = self.peripheral.getServiceByUUID(SERVICE_UUID)
        self.device = self.service.getCharacteristics(CHARACTERISTIC_UUID)[0]

        print("Connected to light with address", self.address, "successfully")

        self.connected = True

        self.set_free()

    def disconnect(self):
        print("Disconnecting gracefully from light with address", self.address)
        self.peripheral.disconnect()

    def get_state(self):
        return self.state

    def set_busy(self):
        self.set_power(True)

        self.device.write(bytearray(lightutil.color("#FF0000")), withResponse=True)
        self.state = "busy"

    def set_free(self):
        self.set_power(True)

        self.device.write(bytearray(lightutil.color("#10ff00")), withResponse=True)
        self.state = "free"

    def set_power(self, power):
        # 7e 00 04 is_on 00 00 00 00 ef
        is_on = b"\x01" if power else b"\x00" 
        packet = bytearray(b"\x7e\x00\x04" + is_on + b"\x00\x00\x00\x00\xef")
        self.device.write(packet, withResponse=True)

    # write some junk data to see if it's alive or not
    def ping(self):
        if not self.connected:
            return

        try:
            self.device.write(0, withResponse=True)
        except:
            print("failed to ping", self.address)
            # self.state = "free"
            # self.connected = False