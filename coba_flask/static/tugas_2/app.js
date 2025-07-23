function setStatus(status) {
  document.getElementById("status").textContent = status;

  if (status == "ON") {
    document.getElementById("onButton").style.backgroundColor = "green";
    document.getElementById("offButton").style.backgroundColor = "";
  } else {
    document.getElementById("onButton").style.backgroundColor = "";
    document.getElementById("offButton").style.backgroundColor = "red";
  }
}
