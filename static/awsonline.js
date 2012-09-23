window.onload = setStatus;

function setStatus() {
    document.getElementById('awsstatus').innerHTML += 'Online';
    document.getElementById('awsbar').style.display = 'none';
}