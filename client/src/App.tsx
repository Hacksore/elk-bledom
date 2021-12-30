import { useEffect, useState } from "react";
import RoomSelector from "./components/roomSelector";
import { getAllStatus, updateState } from "./service/lights";

function App() {
  const [rooms, setRooms] = useState([]);

  useEffect(() => {
    handleAllStatus();

    // long poll
    setInterval(() => {
      handleAllStatus();
    }, 30 * 1000);
  }, []);

  const handleAllStatus = async () => {
    const rooms = await getAllStatus();
    setRooms(rooms);
  };

  return (
    <div className="main">
      {rooms.map((r: any) => (
        r.connected && <RoomSelector key={r.name} rooms={rooms} onStatusUpdate={handleAllStatus} id={r.name} />
      ))}

      {rooms.length <= 0 && (
        <h2>Can't connect to rooms</h2>
      )}
      <button className="small-btn" onClick={() => fetch("/api/restart", { method: "post" })}>Restart app</button>
    </div>
  );
}

export default App;
