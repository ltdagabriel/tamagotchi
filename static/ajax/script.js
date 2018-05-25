
$(document).ready(()=>{
    loop_load()
})

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
                Object.keys(response).forEach((value)=>{
                    insert_into_value(value,response[value])
                });
                let width = "30px";
                let size= Number(response.pokemon.name.slice(-1));
                if(size == 1){
                    width = "30px"
                }
                else if(size == 2){
                    width = "45px"
                }
                else if(size == 3){
                    width = "60px"
                }
                // let x = Jogo_Da_Velha('Load','','')
                // if(!x.error){
                //     $("#Jogo_da_Velha").modal();
                //     $('#Jogo_da_Velha').on('show.bs.modal', function (event) {
                //       modal.find('.modal-title').text("Game" + x.key)
                //     })
                // }
                
                $("#imagem_pokemon").attr('src', "/static/pokemons/"+ response['pokemon'].name + ".gif")

                $("#list").html(listMake(response['list']))
                $("#health").attr("style", "width: "+ response['health'].toPrecision(3)+"%;");
                $("#cenario").attr("style", 
                        "height: 500px;"+
                        "background-size: 100%;"+
                        "background-repeat: no-repeat;"+
                        "background-image: url('/static/cenarios/"+response['pokemon'].cenario+".jpg');");
                $("#happy").attr("style", "width: "+ response['happy'].toPrecision(3)+"%;");
                $("#hunger").attr("style", "width: "+ response['hunger'].toPrecision(3)+"%;");
                // generate_list()
                setTimeout(loop_load, 1000);

            },
            error: function(error) {
                setTimeout(loop_load, 1000);
            }
        });
    
}
function insert_into_value(to,value){
    if(to == 'age'){
        $("#"+to).html(seconds2time(value));
    }
    else{
    $("#"+to).html(value);
    }
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
                let html = "<div class=\"list-group col-sm-12\">"
                console.log(response)
                for( let i=0; i<response.games.length; i++){
                    if( response.games[i].player2 == null){
                        html+="<button class=\"list-group-item\" onclick=\"Jogo_Da_Velha('Join','',"+response.games[i].key+");\">"+
                        response.games[i].player1 + " vs " + response.games[i].player2 +
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
            
            if (user == game.player2){
                player = 2
                adversario = 1
            }
            if (Jogo_Da_Velha_Vitoria(game.board)){
                if(game.next == game["player"+player+"_piece"]){
                    $("#next").html("Vitória do jogador " + game["player"+player] )
                    console.log("Vitoria do jogador",game["player"+player])
                }
                else{
                    $("#next").html("Vitória do jogador " + game["player"+adversario] )
                    console.log("Vitoria do jogador",game["player"+adversario])
                }
            }
            else if(game["player"+adversario] == null){
                $("#next").html("Aguardando Adversario!")
                
                setTimeout( ()=>{
                    console.log("Aguardando adversario")
                    Jogo_Da_Velha('Wait','',key)
                    }, 1000);
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
                                value+
                            "</button>"
                        );
                    }
                    else{
                        $("#"+linha+coluna).html(value);
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
function getSessionUser(){
    try{

        user = null
        $.ajax(
            {
                dataType: 'json',
            url: '/user/get',
            type: 'POST',
            success: function(response) {
                user = response.user
            },
            error: function(error) {
                console.log(error);
            }
        }
        );
        console.log(user)
        return user
    }
    catch(err){
        console.error(err)
    }
}

function listMake(tamagotchi){
    let test="";
    for (let i = 0; i < tamagotchi.length; i++){
        let value= tamagotchi[i]
        if( value.state != 'Morto'){
            test+=
            "<div class='list-group-item'>"+
                "<a href='/tamagotchi/"+value.id+"'>"+
                    value.name+
                "</a>"+
                "<img"+
                    " onmouseover='bigImg(this)'' onmouseout='normalImg(this)'"+
                    " src='/static/pokemons/"+value.pokemon+".gif')}}' "+
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
