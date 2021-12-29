from light import Light
import os
import threading
import bluepy
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder="static")

print("starting the main server")

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


# Serve React App
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(app.static_folder + "/" + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")


def initialize_lights():
    print("connecting to lights...")
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


if __name__ == "__main__":

    # light thread
    light_thread = threading.Thread(target=initialize_lights)
    light_thread.start()
    
    # start flask on new thread
    flask_thread = threading.Thread(target = lambda: app.run(port=8080, host="0.0.0.0"))
    flask_thread.start()

    # join the light thread back to the main thread?
    light_thread.join()
