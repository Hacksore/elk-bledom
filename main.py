from sys import excepthook
from aiohttp import web
from light import Light
import bluepy
import asyncio

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


async def setup_lights(app: web.Application):
    print("connecting to lights...")
    loop = asyncio.get_running_loop()
    results = []

    for light in lights.values():
        try:
            print("pairing to light", light.address)
            
            result = await loop.run_in_executor(
                None, light.setup)
            results.append(result)

            print("default thread pool", result)


        except bluepy.btle.BTLEDisconnectError as ex: 
            print("failed to connect to light", light.address)            

    await asyncio.gather(results)

app = web.Application()
app.add_routes(routes)
app.on_startup.append(setup_lights)

if __name__ == "__main__":
    web.run_app(app)
    
    