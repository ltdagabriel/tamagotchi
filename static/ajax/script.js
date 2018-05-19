
$(document).ready(loop_load())

function loop_load(){
    $.ajax(
        {
            dataType: 'json',
            url: '/load',
            data: jQuery.param({'id':$('#id_tamagotchi').text()}),
            type: 'POST',
            success: function(response) {
                Object.keys(response).forEach((value)=>{
                    insert_into_value(value,response[value])
                });
                $("#list").html(listMake(response['list']))
                $("#health").attr("style", "width: "+ response['health'].toPrecision(3)+"%;");
                $("#happy").attr("style", "width: "+ response['happy'].toPrecision(3)+"%;");
                $("#hunger").attr("style", "width: "+ response['hunger'].toPrecision(3)+"%;");
                setTimeout(loop_load, 1000);
            },
            error: function(error) {
                console.log(error);
                setTimeout(loop_load, 1000);
            }
        }
    );
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
                    " src='/static/pokemons/"+value.pokemon+"1.gif')}}' "+
                    " style=' width:30px; margin-rigth:0px'"+
                " />"+
                "<button >"+
                "<span aria-hidden='true'>&times;</span>"+
                "</button>"+
            "</div>"
        }
    }
    return test
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
