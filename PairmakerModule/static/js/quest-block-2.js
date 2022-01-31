function openTab(evt, tabName) {
    var i, tabcontent, tablinks;

    tabcontent = document.querySelectorAll(".tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    tablinks = document.querySelectorAll(".tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    document.querySelector(`#${tabName}`).style.display = "flex";
    evt.currentTarget.className += " active";
}

function clearBlock(blockname) {
    const radioblocks = document.querySelectorAll(`[name=${blockname}]`);
    const kitelements = document.querySelectorAll(`.${blockname}_kit`);
    for (radio of radioblocks) {
        radio.checked = false;
    }
    for (el of kitelements) {
        el.hidden = true;
    }
}

function resetKit(inputName, inputId) {
    const classObj = document.querySelectorAll(`.${inputName}_kit`);
    for (obj of classObj) {
        obj.hidden = true;
    }
    document.querySelector(`#${inputId}_kit`).hidden = false;
}

window.onload = () => {
    let typenames = ['brows', 'hair', 'eyes', 'lips', 'nose']
    for (typename of typenames) {
        document.querySelector(`#${typename}1`).click();
    }
    document.querySelector(`#startbtn`).click();
}