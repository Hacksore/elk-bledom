var roomId;

window.onload = function () {
  console.log("page load");

  if (!localStorage.getItem("roomId")) {
    // ask for a room
    roomId = prompt("Enter your room id");
    // save to load storage
    localStorage.setItem("roomId", roomId.toLowerCase());
  } else {
    roomId = localStorage.getItem("roomId");
  }

  // set room
  // document.getElementsByClassName("current-room")[0].innerHTML = roomId;

  getStatus()
}

function updateStatusText(status) {
  const ele = document.getElementById("status");
  ele.innerHTML = status

  // // add class
  // if (status === "busy") {
  //   ele.classList.add("busy")
  //   ele.classList.remove("free")
  // }

  // if (status === "free") {
  //   ele.classList.add("free")
  //   ele.classList.remove("busy")
  // }

}

function getStatus() {
  fetch("/status", {
    method: "POST",
    body: JSON.stringify({
      room: roomId
    })
  })
    .then(res => res.json())
    .then(res => {
      updateStatusText(res.status)
    })
}

function setStatus(state) {
  fetch("/update", {
    method: "POST",
    body: JSON.stringify({
      room: roomId,
      state: state
    })
  }).then(res => res.json())
    .then(res => {
      console.log(res);
      updateStatusText(res.status);
    })
}
