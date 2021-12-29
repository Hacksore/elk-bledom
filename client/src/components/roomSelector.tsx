import { updateState } from "../service/lights";

function RoomSelector({ id, rooms, onStatusUpdate }: { id: string, rooms: any, onStatusUpdate: Function }) {

  const room = rooms.find((item: any) => item.name === id);

  const handleClick = async (state: string) => {
    await updateState(id, state);
    onStatusUpdate();
  }

  if (!room) {
    return null;
  }

  return (
    <div className="main">
      <h2>{id}</h2>

      <div className="room-selector">
        <button onClick={() => handleClick("free")} className="btn free">
          Free
        </button>
        <button onClick={() => handleClick("busy")} className="btn busy">
          Busy
        </button>

        <div className={`status ${room.state}`}>{room.state}</div>
      </div>

    </div>
  );
}

export default RoomSelector;
