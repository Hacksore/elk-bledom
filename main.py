from sys import excepthook
from aiohttp import web
from light import Light
import bluepy
import time

routes = web.RouteTableDef()

# TODO: allow this to be configurable
lights = {
    "room1": Light("FF:FF:A0:45:AA:A0"),
    "room2": Light("BE:FF:A0:04:B4:6F"),
    "room3": Light("BE:FF:30:04:4A:C3"),
}

@routes.post("/update")
async def handle_update_light(request):
    body = await request.json()
    room = body["room"]
    state = body["state"]

    # TODO: investigate why the light just dies sometimes
    light = lights[room]

    if state == "busy":
        light.set_busy()
        return web.json_response({
            "message": "success",
            "status": "busy",
        })

    if state == "free":
        light.set_free()
        return web.json_response({
            "message": "success",
            "status": "free",
        })

    return web.json_response({
        "error": "Shit didnt go as planned"
    })


@routes.post("/status")
async def handle_index(request):
    body = await request.json()
    room = body["room"] 
    return web.json_response({
        "status": lights[room].get_state()
    })


async def initialize_lights(app: web.Application):
    def create_light(light):
        try:
            light.setup()
        except bluepy.btle.BTLEDisconnectError as ex:
            print("Failed to connect to light", light.address, "on interface", light.interface)
            # just try again recursively 
            create_light(light)
        except Exception as exc:
            print("Unknown exception:", exc)

    for light in lights.values():
        time.sleep(2)
        create_light(light)

async def destroy_lights(app: web.Application):
    print("Disconnecting lights...")
    def destroy_light(light):
        print("Disconnecting from light with address", light.address)
        if light and hasattr(light, "peripheral"):
            light.disconnect()

    for light in lights.values():
        destroy_light(light)


app = web.Application()

routes.static("/", "./static")
app.add_routes(routes)

# Connect web server startup & shutdown to light connection/disconnection
app.on_startup.append(initialize_lights)
app.on_shutdown.append(destroy_lights)

if __name__ == "__main__":
    web.run_app(app)
    
    