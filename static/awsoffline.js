window.onload = setStatus;

function setStatus() {
    document.getElementById('awsstatus').innerHTML += 'Offline';
    document.getElementById('awsbar').style.display = 'none';
}