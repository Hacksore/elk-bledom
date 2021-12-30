from light import Light
import os
import threading
import bluepy
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder="static")

print("starting the main server")

# TODO: allow this to be configurable
lights = {
    # this is too far away and it breaks the whole app
    "Sean": Light("FF:FF:A0:45:AA:A0"),
    "Dani": Light("BE:FF:A0:04:B4:6F"),
    "Test": Light("BE:FF:30:04:4A:C3"),
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


@app.route("/api/restart", methods=["POST"])
def handle_restart():
    shutdown_func = request.environ.get("werkzeug.server.shutdown")
    if shutdown_func is None:
        raise RuntimeError("Not running werkzeug")
    shutdown_func()


@app.route("/api/status/all", methods=["GET"])
def handle_all_status():
    return jsonify(
        [
            {"state": value.state, "name": room, "connected": value.connected}
            for (room, value) in lights.items()
        ]
    )


@app.route("/api/powerOff", methods=["POST"])
def handle_power_off():
    for light in lights.values():
        if light.connected:
            light.set_power(False)

    return jsonify({"status": "ok"})


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
        except bluepy.btle.BTLEDisconnectError:
            print("Failed to connect to light", light.address)
            # just try again recursively
            create_light(light)
        except Exception as exc:
            print("Unknown exception:", exc)

    for light in lights.values():
        # create_light(light)
        thread = threading.Thread(target=create_light, args=[light])
        thread.start()


if __name__ == "__main__":

    # light thread
    light_thread = threading.Thread(target=initialize_lights)
    light_thread.start()

    # start flask on new thread
    flask_thread = threading.Thread(target=lambda: app.run(port=80, host="0.0.0.0"))
    flask_thread.start()

    # join the light thread back to the main thread?
    light_thread.join()
