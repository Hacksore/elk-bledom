from light import Light
import bluepy
import threading
from flask import Flask, jsonify, request

app = Flask(__name__)

# TODO: allow this to be configurable
lights = {
    "room1": Light("FF:FF:A0:45:AA:A0"),
    "room2": Light("BE:FF:A0:04:B4:6F"),
    "room3": Light("BE:FF:30:04:4A:C3"),
    # "room0": Light("BE:FF:30:04:4A:C4"),
}


@app.route("/api/update", methods=["POST"])
def handle_update_light():
    body = request.json
    print(body)
    room = body["room"]
    state = body["state"]

    # TODO: investigate why the light just dies sometimes
    light = lights[room]

    if state == "busy":
        light.set_busy()
        return jsonify(
            {
                "message": "success",
                "status": "busy",
            }
        )

    if state == "free":
        light.set_free()
        return jsonify(
            {
                "message": "success",
                "status": "free",
            }
        )

    return jsonify({"error": "Shit didnt go as planned"})


@app.route("/api/status", methods=["POST"])
def handle_status():
    body = request.json
    room = body["room"]
    return jsonify({"status": lights[room].get_state()})


@app.route("/api/status/all", methods=["GET"])
def handle_all_status():
    return jsonify(
        [
            {"state": value.state, "name": room, "connected": value.connected}
            for (room, value) in lights.items()
        ]
    )


def initialize_lights():
    def create_light(light):
        try:
            light.setup()
        except bluepy.btle.BTLEDisconnectError as ex:
            print(
                "Failed to connect to light",
                light.address,
                "on interface",
                light.interface,
            )
            # just try again recursively
            create_light(light)
        except Exception as exc:
            print("Unknown exception:", exc)

    for light in lights.values():
        create_light(light)


def destroy_lights():
    def destroy_light(light):
        print("Disconnecting from light with address", light.address)
        if light and hasattr(light, "peripheral"):
            light.disconnect()

    for light in lights.values():
        destroy_light(light)


# start light thread
light_thread = threading.Thread(target=initialize_lights)
light_thread.start()

if __name__ == "__main__":
    app.run(debug=False)
