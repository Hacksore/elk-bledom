export const updateState = async (room: string, state: string) => {
  const data = await fetch("/api/update", {
    method: "POST",
    body: JSON.stringify({
      room,
      state
    }),
    headers: {
      "Content-Type": "application/json"
    }
  }).then(res => res.json());

  return data;
};

export const powerAllOff = async () => {
  const data = await fetch("/api/powerOff", {
    method: "POST",
  }).then(res => res.json());

  return data;
};

export const getAllStatus = async () => {
  const data = await fetch("/api/status/all").then(res => res.json());

  return data;
};
