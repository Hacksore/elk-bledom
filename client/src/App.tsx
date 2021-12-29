import { useEffect, useState } from "react";
import { getAllStatus, updateState } from "./service/lights";

function App() {
  const [rooms, setRooms] = useState([]);
  useEffect(() => {
    handleAllStatus();
  }, []);

  const handleAllStatus = async () => {
    const rooms = await getAllStatus();
    console.log(rooms);
    setRooms(rooms);
  };

  const handleStatusUpdate = async (state: string) => {
    const response = await updateState("room1", state);
    console.log(response);
  };

  return (
    <div className="main">
      <button onClick={() => handleStatusUpdate("free")} className="btn free">
        Free
      </button>
      <button onClick={() => handleStatusUpdate("busy")} className="btn busy">
        Busy
      </button>

      {rooms.map((room: any) => (
        <h2>{room.name}</h2>
      ))}
    </div>
  );
}

export default App;
