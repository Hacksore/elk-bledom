#! /usr/bin/env python3

# import bluepy

# r1 = bluepy.btle.Peripheral('FF:FF:A0:45:AA:A0')
# r2 = bluepy.btle.Peripheral('BE:FF:A0:04:B4:6F')

# print(r1, r2)

import asyncio

from bleak import BleakClient

address = "24:71:89:cc:09:05"
MODEL_NBR_UUID = "00002a24-0000-1000-8000-00805f9b34fb"

async def main(address):
    async with BleakClient(address) as client:
        model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        print("Model Number: {0}".format("".join(map(chr, model_number))))

asyncio.run(main(address))