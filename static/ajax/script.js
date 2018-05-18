
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
function seconds2time (time) {
    let seconds= parseInt(time,10) 
    let day = Math.floor(time/(60*60*24))
    seconds = time - day*(60*60*24)
    let hours = Math.floor(time/(60*60))
    seconds = time - hours*(60*60)
    let minutes = Math.floor(time/(60))
    seconds = time - minutes*(60) 

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
