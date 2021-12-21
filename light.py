from bluepy.btle import Peripheral, ADDR_TYPE_PUBLIC

def color(hexa):    
    hexa = hexa.lstrip("#")

    return [0x7e, 0x07, 0x05, 0x03, int(hexa[0:2], 16), int(hexa[2:4], 16), int(hexa[4:6], 16), 0x00, 0xef]

class Light:
    def __init__(self, address):
        # service id
        self.service_uuid = "0000fff0-0000-1000-8000-00805f9b34fb"

        # characteristic id
        self.characteristic_uuid = "0000fff3-0000-1000-8000-00805f9b34fb"

        # address
        self.address = address

    def setup(self):
        self.peripheral = Peripheral(self.address, addrType=ADDR_TYPE_PUBLIC)
        self.service = self.peripheral.getServiceByUUID(self.service_uuid)
        self.device = self.service.getCharacteristics(self.characteristic_uuid)[0]

    def disconnect(self):
        self.peripheral.disconnect()

    def __enter__(self):       
        return self.setup()
      
    def __exit__(self, _exc_type, exc_value, exc_traceback):
        return self.disconnect()

    # TODO: get color of light
    def get_color(self):
        self.device.read("GET ME COLOR")

    def set_busy(self):
        self.device.write(bytearray(color("#FF0000")))

    def set_free(self):
        self.device.write(bytearray(color("#10ff00")))

