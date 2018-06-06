$(document).ready(() => {
    load_tamagotchi_list()
    sessionStorage.setItem("id", "")

    load_tamagotchi(Number(sessionStorage.id))
})

function setTamaID(id) {
    sessionStorage.setItem("id", id.toString())
}


var load_tamagotchi_error = 0
var load_tamagotchi_list_error = 0

function tamagotchiActions(action, value, id) {
    // alert("/tamagotchi/"+id+"/"+action+"/"+value)
    $.ajax(
        {
            dataType: 'json',
            url: '/tamagotchi/update',
            data: jQuery.param({'id': id, 'value': value, 'action': action}),
            type: 'POST',
            success: function (response) {
                console.log(response)
            },
            error: function (error) {
                console.log(error);
            }
        }
    );
}

function load_tamagotchi(id) {
    $.ajax({
        dataType: 'json',
        url: '/tamagotchi',
        data: jQuery.param({'id': id}),
        type: 'POST',
        success: function (response) {
            let x
            if (response.length) {
                x = response[0]
            }
            if (x) {
                if (!sessionStorage.id) {
                    sessionStorage.setItem("id", x.tamagotchi.id.toString())
                }
                $("#pokeinfo").attr({"class": ""})
                $("#nome").text("[" + x.pokemon.nome + "] " + x.tamagotchi.name)
                $("#idade").text(x.tamagotchi.age)

                if ($("#tama_img").attr("src") != ("/static/imagens/pokemons/" + x.pokemon.img))
                    $("#tama_img").attr({"src": "/static/imagens/pokemons/" + x.pokemon.img})

                progress("health", x.tamagotchi.health)
                progress("happy", x.tamagotchi.happy)
                progress("hunger", x.tamagotchi.hunger)
            }
            else {
                $("#pokeinfo").attr({"class": "collapse"})
            }
            if (load_tamagotchi_error < 5) {
                setTimeout(() => {
                    load_tamagotchi(Number(sessionStorage.id))
                }, 500);
            }
            else {
                window.location.href = ("/")
            }
        },
        error: function (error) {
            load_tamagotchi_error += 1
            if (load_tamagotchi_error < 5) {
                setTimeout(() => {
                    load_tamagotchi(Number(sessionStorage.id))
                }, 1 * 1000);
            }
            else {
                window.location.href = ("/logout")
            }
            console.error("error ", id)
        }
    })
}

function progress(id, value) {
    let color = 'progress-bar-success'
    if (value < 60) {
        color = 'progress-bar-warning'
    }
    if (value < 30) {
        color = 'progress-bar-danger'
    }
    $("#" + id).attr({
        "class": "progress-bar " + color,
        "style": "width:" + value + "%; font-size: 6px",
        "aria-valuenow": value
    })
}


function load_tamagotchi_list() {
    $.ajax({
        dataType: 'json',
        url: '/tamagotchis/user',
        type: 'POST',
        success: function (response) {
            let tamagotchis = ""

            for (let i = 0; i < response.length; i++) {
                tamagotchis +=
                    "<a href=\"#\" id=\"tama\" onclick='setTamaID(" + response[i].tamagotchi.id + ")' class=\"list-group-item\">\n" +
                    "   <span id=\"tama_msg\" class=\"badge\">" +
                    response[i].tamagotchi.state.length +
                    "</span>\n" +
                    "   <img id=\"tama_imagem\" class=\"tama-icon\" src=\"/static/imagens/pokemons/" + response[i].pokemon.img + "\">\n" +
                    "   <i id=\"tama_name\">" +
                    response[i].tamagotchi.name +
                    "   </i>\n" +
                    "</a>"
            }
            $('#tamalist').html(tamagotchis)

            if (load_tamagotchi_list_error < 5) {
                setTimeout(load_tamagotchi_list, 1 * 1000);
            }
            else {
                window.location.href = ("/logout")
            }
        },
        error: function (error) {
            load_tamagotchi_list_error += 1
            if (load_tamagotchi_list_error < 5) {
                setTimeout(load_tamagotchi_list, 1 * 1000);
            }
            else {
                window.location.href = ("/logout")
            }
            console.error(error)
        }
    })
}