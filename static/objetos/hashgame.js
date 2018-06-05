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

function Jogo_Da_Velha_Vitoria(board) {
    let linha = 1
    let anterior_linha = null
    let coluna = 1
    let anterior_coluna = null
    let diagonal1 = 1
    let diagonal2 = 1
    let anterior_diagonal1 = null
    let anterior_diagonal2 = null

    for (let i = 0; i < board.length; i++) {
        if (!anterior_diagonal1)
            anterior_diagonal1 = board[i][i]
        else if (anterior_diagonal1 == board[i][i]) {
            diagonal1++
        }
        if (!anterior_diagonal2)
            anterior_diagonal2 = board[2 - i][2 - i]
        else if (anterior_diagonal2 == board[2 - i][2 - i]) {
            diagonal2++
        }


        linha = 1
        anterior_linha = null
        coluna = 1
        anterior_coluna = null

        for (let j = 0; j < board[i].length; j++) {
            if (!anterior_linha)
                anterior_linha = board[i][j]
            else if (anterior_linha == board[i][j]) {
                linha++
            }
            if (!anterior_coluna)
                anterior_coluna = board[j][i]
            else if (anterior_coluna == board[j][i]) {
                coluna++
            }
        }
        if ((linha == 3 && anterior_linha != 'B') || (coluna == 3 && anterior_coluna != 'B')) {
            return true
        }

    }
    if ((diagonal1 == 3 && anterior_diagonal1 != 'B') || (diagonal2 == 3 && anterior_diagonal2 != 'B')) {
        return true
    }
    return false
}

function makeboard(game, key) {
    $.ajax(
        {
            dataType: 'json',
            url: '/user/get',
            type: 'POST',
            success: function (response) {
                let user = response.user

                let minha_vez = false
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


                if (Jogo_Da_Velha_Vitoria(game.board)) {
                    if (game.next == game["player" + adversario + "_piece"]) {
                        $("#next").html("Vitória do jogador " + game["player" + player])
                        console.log("Vitoria do jogador", game["player" + player])
                        alert("O jogador " + game["player" + player] + " adquiriu $ 10,00")
                        UserReward(10, game["player" + player], null)
                    }
                    else {
                        $("#next").html("Vitória do jogador " + game["player" + adversario])
                        UserReward(10, game["player" + adversario], null)
                        console.log("Vitoria do jogador", game["player" + adversario])
                    }
                    inGame = false
                }
                else if (game["player" + adversario] == null) {
                    $("#next").html("Aguardando Adversario!")
                    setTimeout(() => {
                        console.log("Aguardando adversario")
                        Jogo_Da_Velha('Wait', '', key)
                    }, 1000);

                    inGame = true

                }
                else if (game.next == game["player" + player + "_piece"]) {
                    minha_vez = true
                    console.log(player)
                    $("#next").html("Sua Vez, sua peça " + game.next)
                }
                else {
                    $("#next").html("Aguardando jogador adversario")

                    let continua = false
                    for (let i = 0; i < 3; i++) {
                        for (let j = 0; j < 3; j++) {
                            if (game.board[i][j] === 'B') {
                                continua = true
                            }
                        }
                    }
                    if (continua) {
                        setTimeout(() => {
                            console.log("Aguardando adversario")
                            Jogo_Da_Velha('Wait', '', key)
                        }, 1000);
                    }
                    else {
                        $("#next").html("A partida resultou em empate")
                        UserReward(5, game["player" + player], game["player" + adversario])
                        inGame = false

                    }
                }
                game.board.forEach((data, linha) => {
                    data.forEach((value, coluna) => {
                        if (minha_vez && value == 'B') {
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
                                'game':''
                               }),
            type: 'POST',
            success: function(response) {
                let html = "<div class=\"list-group col-sm-12 container\">"
                console.log(response)
                for( let i=0; i<response.games.length; i++){
                    if( response.games[i].player2 == null){
                        html+=
                        "<button class=\"list-group-item list-group-item-action\" onclick=\"Jogo_Da_Velha('Join','',"+response.games[i].key+");\">"+
                        "Entrar na partida de "+ response.games[i].player1+
                        "</button>"
                    }
                }
                html+="</div>"
                $("#game_list").html(html);
                console.log(response)
            },
            error: function(error) {
                console.log(error);
            }
        }
    );
}

function UserReward(money,player1,player2){
    $.ajax(
        {
            dataType: 'json',
            url: '/reward',
            data: jQuery.param({
                    'reward': money,
                    'player1': player1,
                    'player2': player2
            }),
            type: 'POST',
            success: function(response) {
                console.log(response)
            },
            error: function(error) {
                console.log(error);
            }
        }
    )

}