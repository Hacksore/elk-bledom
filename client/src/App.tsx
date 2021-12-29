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
    }, 30 * 1000)
  }, []);

  const handleAllStatus = async () => {
    const rooms = await getAllStatus();
    setRooms(rooms);
  };

  return (
    <div className="main">
      <RoomSelector rooms={rooms} onStatusUpdate={handleAllStatus} id="room1" />
      <RoomSelector rooms={rooms} onStatusUpdate={handleAllStatus} id="room2" />
    </div>
  );
}

export default App;
