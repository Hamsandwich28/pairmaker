function acceptRequest(idAccepted) {
    const buttonPressed = document.querySelector(`#${idAccepted}`);
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/enter-page-accept-requests", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({ "toUser": idAccepted }));
    xhr.onload = () => {
        let answer = JSON.parse(xhr.responseText);
        if (xhr.readyState == 4 && xhr.status == "200") {
            if (answer.accepted == true) {
                buttonPressed.innerHTML = "Запрос принят";
                buttonPressed.disabled = true;
            }
        }
    }
}