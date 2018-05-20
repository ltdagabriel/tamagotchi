
$(document).ready(loop_load())

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
                    location.href = "/"
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

                
                $("#imagem_pokemon").html(
                    "<img style='width:"+width+";' "+
                    "onmouseover='bigImg(this)' onmouseout='normalImg(this)'"+
                    "src='/static/pokemons/"+response['pokemon'].name +".gif' />");
                $("#list").html(listMake(response['list']))
                $("#health").attr("style", "width: "+ response['health'].toPrecision(3)+"%;");
                $("#cenario").attr("style", 
                        "height: 500px;"+
                        "background-size: 100%;"+
                        "background-repeat: no-repeat;"+
                        "background-image: url('/static/cenarios/"+response['pokemon'].cenario+".jpg');");
                $("#happy").attr("style", "width: "+ response['happy'].toPrecision(3)+"%;");
                $("#hunger").attr("style", "width: "+ response['hunger'].toPrecision(3)+"%;");
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
    location.href = "/tamagotchi/"+id+"/"+action+"/"+value
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
