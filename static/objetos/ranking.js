$(document).ready(() => {
    load_ranking()
})
let load_ranking_error = 0

function load_ranking() {
    $.ajax({
        dataType: 'json',
        url: '/tamagotchis',
        type: 'POST',
        success: function (response) {
            let tamagotchis = ""
            console.log(response)

            for (let i = 0; i < response.length; i++) {
                tamagotchis +=
                    "<div class=\"list-group col-sm-6\" style='height: 220px'>\n" +
                    "    <div class=\"list-group-item\">\n" +
                    "<div class='col-sm-8'> "+
                    "       <div class=\"col-sm-3\">\n" +
                    "           Nome:\n" +
                    "       </div>\n" +
                    "       <div id=\"nome\" class=\"col-sm-9\">\n" +
                    "[" + response[i].tamagotchi.name_pokemon + "] " + response[i].tamagotchi.name +
                    "    </div>\n" +
                    "    <div class=\"col-sm-3\">\n" +
                    "        Idade:\n" +
                    "    </div>\n" +
                    "    <div id=\"idade\" class=\"col-sm-9\">\n" +
                    response[i].tamagotchi.age +
                    "                        </div>\n" +
                    "                        <div class=\"col-sm-3\">\n" +
                    "                            Criador:\n" +
                    "                        </div>\n" +
                    "                        <div id=\"idade\" class=\"col-sm-9\">\n" +
                    response[i].tamagotchi.user_name +
                    "                        </div>\n" +
                    "                        <div class=\"col-sm-3\">\n" +
                    "                            Colocação:\n" +
                    "                        </div>\n" +
                    "                        <div id=\"idade\" class=\"col-sm-9\">\n" +
                    (i+1) +
                    "                        </div>\n" +
                        "</div>"+
                    "                        <div class=\"text-center\">\n" +
                    "                            <img src=\"/static/imagens/pokemons/"+response[i].pokemon.img+"\" style=\" height:120px; \">\n" +
                    "                        </div>\n" +
                    "                    </div>\n" +
                    "                </div>"
            }
            $('#ranking').html(tamagotchis)

            if (load_ranking_error < 5) {
                setTimeout(load_ranking, 1 * 1000);
            }
            else {
                window.location.href = ("/logout")
            }
        },
        error: function (error) {
            load_ranking_error += 1
            if (load_ranking_error < 5) {
                setTimeout(load_ranking, 1 * 1000);
            }
            else {
                window.location.href = ("/logout")
            }
            console.error(error)
        }
    })
}