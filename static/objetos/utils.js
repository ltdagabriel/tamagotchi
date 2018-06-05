$(document).ready(() => {
    sessionStorage.setItem("itens", "true")
})

function bigImg(x) {
    x.style.width = "64px";
}

function normalImg(x) {
    x.style.width = "32px";
}

function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev) {
    ev.preventDefault();
    let data = ev.dataTransfer.getData("text")
    let i = data.indexOf("_")
    tamagotchiActions(data.slice(0, i), data.slice(i + 1), Number(sessionStorage.id))
}

function loadItens() {
    if (sessionStorage.itens == "true") {
        $("#itens").attr({'class': ''})
        sessionStorage.setItem("itens", "false")
    }
    else {
        $("#itens").attr({'class': 'collapse'})
        sessionStorage.setItem("itens", "true")
    }
}