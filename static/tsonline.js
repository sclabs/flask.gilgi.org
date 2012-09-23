window.onload = tsOnline;

function tsOnline() {
    document.getElementById('tsstatus').innerHTML += 'Online';
    document.getElementById('tsbar').style.display = 'none';
}