const websocketUrl = `ws://${location.host}/dashboard`;
var websocket;
const boxLoading = document.getElementById("box-loading");
const textLdr = document.getElementById("text-ldr");
const boxLdr = document.getElementById("box-ldr");
const sunIcon = document.getElementById("sun-icon");
const moonIcon = document.getElementById("moon-icon");
const dataTemp = document.getElementById("dt-temp");
const dataPressure = document.getElementById("dt-pressure");
const dataAltitude = document.getElementById("dt-altitude");
const dataLdr = document.getElementById("dt-ldr");
const pump1 = document.getElementById("pump-1");
const pump2 = document.getElementById("pump-2");
const lamp1 = document.getElementById("lamp-1");
const lamp2 = document.getElementById("lamp-2");
const jadwalTable = document.getElementById("table-jadwal");
const jadwalTableTbody = jadwalTable.getElementsByTagName("tbody")[0];
let statusLamp1;

const ctx = document.getElementById("sensorChart").getContext("2d");
const chart = new Chart(ctx, {
  type: "line",
  data: {
    labels: [],
    datasets: [
      {
        label: "Data Suhu Ruangan",
        data: [],
        borderColor: "rgb(246, 81, 116)",
        tension: 0.3,
        fill: false,
      },
    ],
  },
  options: {
    scales: {
      x: { title: { display: true, text: "Time" } },
      y: { title: { display: true, text: "Data Suhu" } },
    },
  },
});

function updateClock() {
  const now = new Date(); // Get current date and time
  let hours = now.getHours();
  let minutes = now.getMinutes();
  let seconds = now.getSeconds();

  // Pad single-digit numbers with a leading zero
  hours = hours < 10 ? "0" + hours : hours;
  minutes = minutes < 10 ? "0" + minutes : minutes;
  seconds = seconds < 10 ? "0" + seconds : seconds;

  const timeString = `${hours}:${minutes}:${seconds}`;
  // const dateString = `${now.toDateString()}`; // Get formatted date string

  document.getElementById("clock").innerHTML = `${timeString}`;
}

function addChartData(value) {
  const time = new Date().toLocaleTimeString();
  chart.data.labels.push(time);
  chart.data.datasets[0].data.push(value);
  if (chart.data.labels.length > 20) {
    chart.data.labels.shift();
    chart.data.datasets[0].data.shift();
  }
  chart.update();
}

function removeDataTable() {
  if (jadwalTableTbody) {
    jadwalTableTbody.innerHTML = "";
  }
}

async function fetchJadwal() {
  try {
    removeDataTable();

    const response = await fetch("http://192.168.56.210:8000/api/jadwal", {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });
    const dataJadwal = await response.json();
    dataJadwal.forEach((row) => {
      const rowData = jadwalTableTbody.insertRow();
      rowData.insertCell(0).textContent = row.hari;
      rowData.insertCell(1).textContent = row.jam;
      rowData.insertCell(2).textContent = row.deskripsi;
    });

    // console.log(dataJadwal);
  } catch (error) {
    console.error("Error fetch data");
  }
}

function onOpenWebsocket(event) {
  // websocket.send("mulai");
  console.log("Memulai koneksi ke websocket");
}

function onCloseWebsocket(event) {
  console.log("Koneksi websocket terputus");
}

function onResponseWebsocket(event) {
  boxLoading.style.display = "none";

  console.log("message diterima");

  const response = JSON.parse(event.data);

  if ("temperature" in response) {
    dataTemp.innerText = response.temperature;
    addChartData(response.temperature);
  }

  if ("pressure" in response) {
    dataPressure.innerText = response.pressure;
  }

  if ("altitude" in response) {
    dataAltitude.innerText = response.altitude;
  }

  if ("ldr_signal" in response) {
    if (response.ldr_signal == 1) {
      boxLdr.style.backgroundColor = "#fff";
      boxLdr.style.color = "#291E04";
      textLdr.style.color = "#291E04";
      moonIcon.style.display = "none";
      sunIcon.style.display = "block";
    } else {
      boxLdr.style.backgroundColor = "#291E04";
      boxLdr.style.color = "#fff";
      textLdr.style.color = "#fff";
      moonIcon.style.display = "block";
      sunIcon.style.display = "none";
    }
  }

  if ("lamp_1" in response) {
    statusLamp1 = response.lamp_1;
    styleElement(lamp1, response.lamp_1);
  }

  if ("lamp_2" in response) {
    statusLamp2 = response.lamp_2;
    styleElement(lamp2, response.lamp_2);
  }

  if ("pump_1" in response) {
    statusPump1 = response.pump_1;
    styleElement(pump1, response.pump_1);
  }

  if ("pump_2" in response) {
    statusPump2 = response.pump_2;
    styleElement(pump2, response.pump_2);
  }
}

function styleElement(element, status) {
  const icon = element.firstElementChild;

  if (status == 1) {
    element.style.backgroundColor = "#1A77F2";
    element.style.color = "#fff";
    element.style.borderColor = "#005fd8";
    icon.style.stroke = "#fff";
  } else {
    element.style.backgroundColor = "#fff";
    element.style.color = "#000";
    element.style.borderColor = "#e5e5e5";
    icon.style.stroke = "#000";
  }
}

function initializeWebsocket() {
  console.log("Opening websocket mikropython");
  websocket = new WebSocket(websocketUrl);
  websocket.onopen = onOpenWebsocket;
  websocket.onmessage = onResponseWebsocket;
  websocket.onclose = onCloseWebsocket;
}

lamp1.addEventListener("click", async function (event) {
  event.preventDefault();
  let dataLamp1;

  lamp1.setAttribute("disabled", "");
  lamp1.children[1].innerHTML = "Loading...";

  if (statusLamp1 == 1) {
    dataLamp1 = 0;
  } else {
    dataLamp1 = 1;
  }

  try {
    const response = await fetch("/api/lamp1", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: dataLamp1 }),
    });
    const data = await response.json();
    statusLamp1 = data.status;
    styleElement(lamp1, data.status);
    console.log(data);
  } catch (error) {
    console.error("Error turning on the lamp:", error);
  } finally {
    lamp1.removeAttribute("disabled");
    lamp1.children[1].innerHTML = "Lampu Ruangan 1";
  }
});

lamp2.addEventListener("click", async function (event) {
  event.preventDefault();
  let dataLamp2;

  lamp2.setAttribute("disabled", "");
  lamp2.children[1].innerHTML = "Loading...";

  if (statusLamp2 == 1) {
    dataLamp2 = 0;
  } else {
    dataLamp2 = 1;
  }

  try {
    const response = await fetch("/api/lamp2", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: dataLamp2 }),
    });
    const data = await response.json();
    statusLamp2 = data.status;
    styleElement(lamp2, data.status);
    console.log(data);
  } catch (error) {
    console.error("Error turning on the lamp:", error);
  } finally {
    lamp2.removeAttribute("disabled");
    lamp2.children[1].innerHTML = "Lampu Ruangan 2";
  }
});

pump1.addEventListener("click", async function (event) {
  event.preventDefault();
  let dataPump1;

  pump1.setAttribute("disabled", "");
  pump1.children[1].innerHTML = "Loading...";

  if (statusPump1 == 1) {
    dataPump1 = 0;
  } else {
    dataPump1 = 1;
  }

  try {
    const response = await fetch("/api/pump1", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: dataPump1 }),
    });
    const data = await response.json();
    statusPump1 = data.status;
    styleElement(pump1, data.status);
    console.log(data);
  } catch (error) {
    console.error("Error turning on pompa 1", error);
  } finally {
    pump1.removeAttribute("disabled");
    pump1.children[1].innerHTML = "Pompa Ruangan 1";
  }
});

pump2.addEventListener("click", async function (event) {
  event.preventDefault();
  let dataPump2;

  pump2.setAttribute("disabled", "");
  pump2.children[1].innerHTML = "Loading...";

  if (statusPump2 == 1) {
    dataPump2 = 0;
  } else {
    dataPump2 = 1;
  }

  try {
    const response = await fetch("/api/pump2", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: dataPump2 }),
    });
    const data = await response.json();
    statusPump2 = data.status;
    styleElement(pump2, data.status);
    console.log(data);
  } catch (error) {
    console.error("Error turning on pompa 2", error);
  } finally {
    pump2.removeAttribute("disabled");
    pump2.children[1].innerHTML = "Pompa Ruangan 2";
  }
});

window.addEventListener("DOMContentLoaded", function () {
  initializeWebsocket();
  fetchJadwal();
  updateClock();
  setInterval(fetchJadwal, 2000);
  setInterval(updateClock, 1000);
});
