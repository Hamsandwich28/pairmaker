function sendRequest(buttonId, userId) {
    const pressedButton = document.querySelector(`#${buttonId}`);
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/person-page-send", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({"userId": userId}));
    xhr.onload = () => {
        let answer = JSON.parse(xhr.responseText);
            if (xhr.readyState == 4 && xhr.status == "200") {
                if (answer.sent == true) {
                    pressedButton.innerHTML = "Запрос отправлен";
                } else {
                    pressedButton.innerHTML = "Запрос был отправлен";
                }
                pressedButton.disabled = true;
            }
    }
}