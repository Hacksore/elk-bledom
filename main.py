from sys import excepthook
from aiohttp import web
from light import Light
import bluepy
import asyncio
import functools

routes = web.RouteTableDef()

# TODO: make sure to handle reconnecting
lights = {
    "room1": Light("FF:FF:A0:45:AA:A0"),
    "room2": Light("BE:FF:A0:04:B4:6F"),
}

@routes.post("/update")
async def handle_update_light(request):
    body = await request.json()
    room = body["room"]
    method = body["method"]

    # TODO: investigate why the light just dies sometimes
    light = lights[room]

    if method == "busy":
        light.set_busy()
        return web.json_response({
            "message": "status changed to busy"
        })

    if method == "free":
        light.set_free()
        return web.json_response({
            "message": "status changed to free"
        })

    return web.json_response({
        "error": "Shit didnt go as planned"
    })


@routes.get("/status")
async def handle_index(request):
    text = "Ok"
  
    return web.Response(text=text)


async def lights_startup(app: web.Application):
    print("Connecting to lights...")

    loop = asyncio.get_running_loop()

    def setup_light(light):
        try:
            print("Pairing to and setting up light with address", light.address)
            light.setup()
        except bluepy.btle.BTLEDisconnectError as ex:
            print("Failed to connect to light", light.address)

        except Exception as exc:
            print("Unknown exception:", exc)
        else:
            print("Connected to light with address", light.address, "successfully")

    results = []

    for light in lights.values():
        # results.append(loop.run_in_executor(None, functools.partial(setup_light, light)))d
        setup_light(light)

    #await asyncio.wait(results, timeout=0.5)

async def lights_shutdown(app: web.Application):
    print("Disconnecting lights...")
    loop = asyncio.get_running_loop()

    def destroy_light(light):
        print("Disconnecting from light with address", light.address)
        
        # Only lights with a peripherals are properly connected
        if hasattr(light, 'peripheral'):
            light.disconnect()

    results = []

    for light in lights.values():
        results.append(loop.run_in_executor(None, functools.partial(destroy_light, light)))

    await asyncio.wait(results, timeout=1.5)

app = web.Application()
app.add_routes(routes)
# Connect web server startup & shutdown to light connection/disconnection
app.on_startup.append(lights_startup)
app.on_shutdown.append(lights_shutdown)

if __name__ == "__main__":
    web.run_app(app)
    
    