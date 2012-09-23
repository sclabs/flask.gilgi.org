window.onload = setStatus;

function setStatus() {
    document.getElementById('tsstatus').innerHTML += 'Offline';
    document.getElementById('tsbar').style.display = 'none';
    alert("stuff happened");
}