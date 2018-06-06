$(document).ready(() => {
    sessionStorage.setItem("chat", "open")
    loadmensagems()
})

function toglechat() {
    if(sessionStorage.chat === "open"){
        $("#chat").attr({'class': ''})
        sessionStorage.setItem("chat", "close")
    }
    else{
        $("#chat").attr({'class': 'collapse'})
        sessionStorage.setItem("chat", "open")
    }
}
function loadmensagems() {
    $.ajax(
        {
            dataType: 'json',
            url: '/mensagem',
            data: "",
            type: 'GET',
            success: function (response) {
                console.log(response)
                let msg=""
                for(let i=0;i<response.length;i++){
                    msg+="<p>"+response[i]+"</p>"
                }
                $("#chat_mensagens").html(msg)

                setTimeout(loadmensagems, 1000)
            },
            error: function (error) {
                console.log(error);
            }
        }
    );
}