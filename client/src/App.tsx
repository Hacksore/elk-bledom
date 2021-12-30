import { useEffect, useState } from "react";
import RoomSelector from "./components/roomSelector";
import { getAllStatus, powerAllOff, updateState } from "./service/lights";

function App() {
  const [rooms, setRooms] = useState([]);

  useEffect(() => {
    handleAllStatus();

    // long poll as sockets are kinda overkill here
    setInterval(() => {
      handleAllStatus();
    }, 10 * 1000);
  }, []);

  const handleAllStatus = async () => {
    const rooms = await getAllStatus();
    setRooms(rooms);
  };

  return (
    <div className="main">
      {rooms.map(
        (r: any) =>
          r.connected && <RoomSelector key={r.name} rooms={rooms} onStatusUpdate={handleAllStatus} id={r.name} />
      )}

      {rooms.length <= 0 && <h2>Can't connect to rooms</h2>}

      <hr style={{ marginTop: 40 }} />

      <div style={{ display: "flex", flexDirection: "column" }}>
        <button className="small-btn restart" onClick={() => fetch("/api/restart", { method: "post" })}>
          Restart
        </button>
        <button
          className="small-btn"
          onClick={async () => {
            await powerAllOff();
            handleAllStatus();
          }}
        >
          Power Off
        </button>
      </div>
    </div>
  );
}

export default App;
