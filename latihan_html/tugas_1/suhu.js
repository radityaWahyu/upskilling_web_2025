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

setInterval(updateSuhu, 2000);
updateSuhu();
