let inGame = false

function Jogo_Da_Velha(comand, param, game_id) {
    $.ajax(
        {
            dataType: 'json',
            url: '/games/jogo_da_velha',
            data: jQuery.param({
                'game_name': 'Jogo_da_Velha',
                'comand': comand,
                'param': param,
                'game': game_id
            }),
            type: 'POST',
            success: function (response) {
                if (response.game) {
                    makeboard(response.game, response.key)
                }
            },
            error: function (error) {
                console.log(error);
            }
        }
    );
}


function makeboard(game, key) {
    $.ajax(
        {
            dataType: 'json',
            url: '/user/get',
            type: 'POST',
            success: function (response) {
                let user = response.user.username

                console.log(game, response)

                let adversario = 2
                let player = 1
                inGame = true

                if (response.idle > 30) {
                    inGame = false
                    return
                }

                if (user == game.player2) {
                    player = 2
                    adversario = 1
                }

                if(game.player_winner){
                    inGame = false

                    make(game, key, false)
                    if(game.player_winner === game['player'+player]){
                        $("#next").html("Vitória do jogador " + game["player" + player])

                        if (game['player'+player+'_msg']){
                            alert(game['player'+player+'_msg'])
                        }
                    }
                    else{
                        $("#next").html("Vitória do jogador " + game["player" + adversario])
                        if (game['player'+adversario+'_msg']){
                            alert(game['player'+adversario+'_msg'])
                        }
                    }
                }
                else if (game["player" + adversario] == null) {
                    $("#next").html("Aguardando Adversario!")
                    make(game, key, false)
                    setTimeout(() => {
                        console.log("Aguardando adversario")
                        Jogo_Da_Velha('Wait', '', key)
                    }, 1000);

                    inGame = true
                }
                else if (game.next === game["player" + player + "_piece"]) {
                    $("#next").html("Sua Vez, sua peça " + game.next)
                    make(game, key, true)
                }
                else{
                    $("#next").html("Aguardando jogador adversario")
                    make(game, key , false)
                    if(game.valid){
                        setTimeout(() => {
                            console.log("Aguardando adversario")
                            Jogo_Da_Velha('Wait', '', key)
                        }, 1000);
                    }
                    else {
                        $("#next").html("A partida resultou em empate")
                        if(game['player'+player+'_msg']){
                            alert(game['player'+player+'_msg'])
                        }
                        inGame = false
                    }
                }
            },
            error: function (error) {
                console.log(error);
            }
        }
    );
}

function generate_list() {
    $.ajax(
        {
            dataType: 'json',
            url: '/games/jogo_da_velha',
            data: jQuery.param({
                'game_name': 'Jogo_da_Velha',
                'comand': 'All',
                'param': '',
                'game': ''
            }),
            type: 'POST',
            success: function (response) {
                let html = "<div class=\"list-group col-sm-12 container\">"
                console.log(response)
                for (let i = 0; i < response.games.length; i++) {
                    if (response.games[i].player2 == null) {
                        html +=
                            "<button class=\"list-group-item list-group-item-action\" onclick=\"Jogo_Da_Velha('Join',''," + response.games[i].key + ");\">" +
                            "Entrar na partida de " + response.games[i].player1 +
                            "</button>"
                    }
                }
                html += "</div>"
                $("#game_list").html(html);
                console.log(response)
            },
            error: function (error) {
                console.log(error);
            }
        }
    );
}
function make(game, key, click) {
    game.board.forEach((data, linha) => {
        data.forEach((value, coluna) => {
            if ( click && value === 'B') {
                $("#" + linha + coluna).html(
                    "<button onclick=\"Jogo_Da_Velha('Move','" + linha + coluna + "'," + key + ");\">" +
                    "<img class=\"col-sm-12\" src=\"/static/imagens/games/" + value + ".png\" />" +
                    "</button>"
                );
            }
            else {
                $("#" + linha + coluna).html("<img class=\"col-sm-12\" src=\"/static/imagens/games/" + value + ".png\" />");
            }
        })
    })
}