from bluepy.btle import Peripheral, ADDR_TYPE_PUBLIC
import lightutil

# Found some info here
# https://github.com/arduino12/ble_rgb_led_strip_controller
SERVICE_UUID = "0000fff0-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_UUID = "0000fff3-0000-1000-8000-00805f9b34fb"

class Light:
    def __init__(self, address, interface=0):
        self.peripheral = None
        self.device = None
        self.address = address
        self.interface = interface
        self.state = None

    def setup(self):
        self.peripheral = Peripheral(self.address, iface=self.interface)
        self.service = self.peripheral.getServiceByUUID(SERVICE_UUID)
        self.device = self.service.getCharacteristics(CHARACTERISTIC_UUID)[0]

        print("Connected to light with address", self.address, "successfully")

        self.set_free()

    def disconnect(self):
        print("Disconnecting gracefully from light with address", self.address)
        self.peripheral.disconnect()

    def get_state(self):
        return self.state

    def set_busy(self):
        self.device.write(bytearray(lightutil.color("#FF0000")), withResponse=True)
        self.state = "busy"

    def set_free(self):
        self.device.write(bytearray(lightutil.color("#10ff00")), withResponse=True)
        self.state = "free"
