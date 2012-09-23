window.onload = setStatus;

function setStatus() {
    document.getElementById('tsstatus').innerHTML += 'Online';
    document.getElementById('tsbar').style.display = 'none';
}