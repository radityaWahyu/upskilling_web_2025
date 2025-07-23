function generateRandomSuhu() {
  return (Math.random() * 10 + 20).toFixed(2);
}

function updateSuhu() {
  const suhu = generateRandomSuhu();

  document.getElementById("suhu").textContent = suhu;
  const fanStatusElement = document.getElementById("fanStatus");

  if (suhu > 25) {
    fanStatusElement.textContent = "ON";
    fanStatusElement.style.color = "green";
  } else {
    fanStatusElement.textContent = "OFF";
    fanStatusElement.style.color = "red";
  }
}

function setStatusRuang1(status) {
  const statusRuang1 = document.getElementById("statusRuang1");
  statusRuang1.textContent = status;

  if (status == "ON") {
    document.getElementById("onButton1").style.backgroundColor = "green";
    document.getElementById("offButton1").style.backgroundColor = "";
    statusRuang1.style.color = "green";
  } else {
    document.getElementById("onButton1").style.backgroundColor = "";
    document.getElementById("offButton1").style.backgroundColor = "red";
    statusRuang1.style.color = "red";
  }
}

function setStatusRuang2(status) {
  const statusRuang2 = document.getElementById("statusRuang2");
  statusRuang2.textContent = status;

  if (status == "ON") {
    document.getElementById("onButton2").style.backgroundColor = "green";
    document.getElementById("offButton2").style.backgroundColor = "";
    statusRuang2.style.color = "green";
  } else {
    document.getElementById("onButton2").style.backgroundColor = "";
    document.getElementById("offButton2").style.backgroundColor = "red";
    statusRuang2.style.color = "red";
  }
}

function setStatusRuang3(status) {
  const statusRuang3 = document.getElementById("statusRuang3");
  statusRuang3.textContent = status;

  if (status == "ON") {
    document.getElementById("onButton3").style.backgroundColor = "green";
    document.getElementById("offButton3").style.backgroundColor = "";
    statusRuang3.style.color = "green";
  } else {
    document.getElementById("onButton3").style.backgroundColor = "";
    document.getElementById("offButton3").style.backgroundColor = "red";
    statusRuang3.style.color = "red";
  }
}

function setStatusRuang4(status) {
  const statusRuang4 = document.getElementById("statusRuang4");
  statusRuang4.textContent = status;

  if (status == "ON") {
    document.getElementById("onButton4").style.backgroundColor = "green";
    document.getElementById("offButton4").style.backgroundColor = "";
    statusRuang4.style.color = "green";
  } else {
    document.getElementById("onButton4").style.backgroundColor = "";
    document.getElementById("offButton4").style.backgroundColor = "red";
    statusRuang4.style.color = "red";
  }
}

setInterval(updateSuhu, 2000);
updateSuhu();
