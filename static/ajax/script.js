
$(document).ready(()=>{
    loop_load()
})

var inGame = false
var newError = 1

function loop_load(){
    
        $.ajax(
            {
            dataType: 'json',
            url: '/load',
            data: jQuery.param({'id':$('#id_tamagotchi').text()}),
            type: 'POST',
            success: function(response) {
                let error=response['error']
                if (error){
                    console.log(error)
                }
                
                $("#imagem_pokemon").attr('style', "width:"+ response['pokemon'].width)
                
                $("#list").html(listMake(response['list']))
                
                $("#health").attr("style", "width: "+ response['health'].toPrecision(3)+"%;");
                $("#health").text(response['health'].toPrecision(3)+"%");
                
                $("#happy").attr("style", "width: "+ response['happy'].toPrecision(3)+"%;");
                $("#happy").text(response['happy'].toPrecision(3)+"%");
                
                $("#hunger").attr("style", "width: "+ response['hunger'].toPrecision(3)+"%;");
                $("#hunger").text(response['hunger'].toPrecision(3)+"%");
                
                $("#age").html(seconds2time(response['age']));

                $("#cenario").attr("style", 
                        "height: 500px;"+
                        "background-size: 100%;"+
                        "background-repeat: no-repeat;"+
                        "background-image: url('/static/cenarios/"+response['pokemon'].cenario+".jpg');");
                // generate_list()
                newError = 1
                if(inGame){
                    setTimeout(loop_load, 10000);
                }
                else{
                    setTimeout(loop_load, 2100);
                }

            },
            error: function(error) {
                setTimeout(loop_load, 10000* newError);
                newError +=1
            }
        });
    
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
function Jogo_Da_Velha_Vitoria(board){
    let linha = 1
    let anterior_linha = null
    let coluna = 1
    let anterior_coluna = null
    let diagonal1 = 1
    let diagonal2 = 1
    let anterior_diagonal1 = null
    let anterior_diagonal2 = null

    for(let i=0;i<board.length;i++){
        if (!anterior_diagonal1)
            anterior_diagonal1 = board[i][i]
        else if(anterior_diagonal1 == board[i][i]){
            diagonal1++
        }
        if (!anterior_diagonal2)
                anterior_diagonal2 = board[2-i][2-i]
        else if(anterior_diagonal2 == board[2-i][2-i]){
            diagonal2++
        }


        linha = 1
        anterior_linha = null
        coluna = 1
        anterior_coluna = null

        for(let j=0;j<board[i].length;j++){
            if (!anterior_linha)
                anterior_linha = board[i][j]
            else if(anterior_linha == board[i][j]){
                linha++
            }
            if (!anterior_coluna)
                anterior_coluna = board[j][i]
            else if(anterior_coluna == board[j][i]){
                coluna++
            }
        }
        if((linha==3 && anterior_linha != 'B') || (coluna==3 && anterior_coluna != 'B')){
            return true
        }

    }
    if((diagonal1==3 && anterior_diagonal1 != 'B') || (diagonal2==3 && anterior_diagonal2 != 'B')){
        return true
    }
    return false
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
            success: function(response) {
                console.log(response)
            },
            error: function(error) {
                console.log(error);
            }
        }
    )

}


function Prepare_Jogo_Da_Velha(game,key){
    $.ajax(
        {
            dataType: 'json',
        url: '/user/get',
        type: 'POST',
        success: function(response) {
            user = response.user
            let minha_vez = false
            let adversario = 2
            let player = 1
            inGame = true

            if(response.idle> 30){
                inGame = false
                return
            }

            if (user == game.player2){
                player = 2
                adversario = 1
            }
            if (Jogo_Da_Velha_Vitoria(game.board)){
                if(game.next == game["player"+adversario+"_piece"]){
                    $("#next").html("Vitória do jogador " + game["player"+player] )
                    console.log("Vitoria do jogador",game["player"+player])
                    alert("Adquirido $ 10,00")
                    UserReward(10, game["player"+player], null)
                }
                else{
                    $("#next").html("Vitória do jogador " + game["player"+adversario] )
                    UserReward(10, game["player"+adversario], null)
                    console.log("Vitoria do jogador",game["player"+adversario])
                }
                inGame = false
            }
            else if(game["player"+adversario] == null){
                $("#next").html("Aguardando Adversario!")

                let continua= true
                for(let i=0;i<3;i++){
                    for(let j=0;j<3;j++){
                        if(game.board[i][j] === 'B'){
                            continua = false
                        }
                    }
                }
                if(continua){
                    setTimeout( ()=>{
                        console.log("Aguardando adversario")
                        Jogo_Da_Velha('Wait','',key)
                        }, 1000);
                    UserReward(5, game["player"+player], game["player"+adversario])
                }
                else{
                    inGame = true
                }
            }
            else if(game.next == game["player"+player+"_piece"]){
                minha_vez = true
                console.log(player)
                $("#next").html("Sua Vez, sua peça " + game.next)
            }
            else{
                $("#next").html("Aguardando jogador adversario")
                setTimeout( ()=>{
                    console.log("Aguardando a vez do jogador ", game["player"+adversario])
                    Jogo_Da_Velha('Wait','',key)
                    }, 1000);
            }
            
            game.board.forEach((data,linha)=>{
                data.forEach((value,coluna)=>{
                    if(minha_vez && value == 'B'){
                        $("#"+linha+coluna).html(
                            "<button onclick=\"Jogo_Da_Velha('Move','" + linha+coluna + "',"+key+");\">"+
                                "<img class=\"col-sm-12\" src=\"/static/games/"+value+".png\" />"+
                            "</button>"
                        );
                    }
                    else{
                        $("#"+linha+coluna).html("<img class=\"col-sm-12\" src=\"/static/games/"+value+".png\" />");
                    }
                })
            })
        },
        error: function(error) {
            console.log(error);
        }
    }
    );
    
}

function Jogo_Da_Velha(comand, param, game_id){
    $.ajax(
        {
            dataType: 'json',
            url: '/games/jogo_da_velha',
            data: jQuery.param({
                                'game_name': 'Jogo_da_Velha',
                                'comand': comand,
                                'param': param,
                                'game':game_id
                               }),
            type: 'POST',
            success: function(response) {
                if(response.game){
                    console.log(response)
                    Prepare_Jogo_Da_Velha(response.game,response.key)
                }
            },
            error: function(error) {
                console.log(error);
            }
        }
    );
}

function listMake(tamagotchi){
    let test="";
    for (let i = 0; i < tamagotchi.length; i++){
        let value= tamagotchi[i]
        if( value.state != 'Morto'){
            test+=
            "<div>"+
                "<a href='/tamagotchi/"+value.id+"'>"+
                    value.name+
                "</a>"+
                "<img"+
                    " onmouseover='bigImg(this)'' onmouseout='normalImg(this)'"+
                    " src='/static/pokemons/"+value.pokemon.img+".gif')}}' "+
                    " style=' width:32px; margin-rigth:0px'"+
                " />"+
                "<button onClick='deleteTamagotchi("+value.id+")' class='close'>"+
                    "<span aria-hidden='true'>&times;</span>"+
                "</button>"+
            "</div>"
        }
    }
    return test
}
function deleteTamagotchi(id){
    $.ajax(
        {
            dataType: 'json',
            url: '/tamagotchi/del',
            data: jQuery.param({'id': id}),
            type: 'POST',
            success: function(response) {
                console.log(response)
            },
            error: function(error) {
                console.log(error);
            }
        }
    );
}
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

function drop(ev, id) {
    ev.preventDefault();
    let data = ev.dataTransfer.getData("text")
    let i= data.indexOf("_")
    tamagotchiActions(data.slice(0,i),data.slice(i+1),id)
}
function tamagotchiActions(action,value,id){
    // alert("/tamagotchi/"+id+"/"+action+"/"+value)
    $.ajax(
        {
            dataType: 'json',
            url: '/tamagotchi/update/'+action,
            data: jQuery.param({'id': id, 'value': value}),
            type: 'POST',
            success: function(response) {
                console.log(response)
            },
            error: function(error) {
                console.log(error);
            }
        }
    );
}

function seconds2time (time) {
    let seconds= parseInt(time,10) 
    let day = Math.floor(seconds/(60*60*24))
    seconds = seconds - day*(60*60*24)
    let hours = Math.floor(seconds/(60*60))
    seconds = seconds - hours*(60*60)
    let minutes = Math.floor(seconds/(60))
    seconds = seconds - minutes*(60) 

    let life_time= "";
    if(day){
        life_time= life_time + day + " dias "
    }
    if(hours){
        if (hours<10){
            life_time= life_time +"0"+ hours + "h :"
        }
        else{
            life_time= life_time + hours + "h :"
        }
    }
    life_time= life_time + minutes + "m :"
    life_time= life_time + seconds.toPrecision(2) + "s"
    
    return life_time
}
