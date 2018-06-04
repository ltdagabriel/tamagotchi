$(document).ready(()=>{
    load_users()
})
var load_user_error = 0
function load_users() {
    $.ajax({
        dataType: 'json',
        url: '/usuarios',
        type: 'POST',
        success: function (response) {
            if(!response.usuarios){
                return
            }
            let usuarios = response['usuarios']
            let mensagens = response['mensagens']
            let status = response['status']
            let user= ""
            for(let i=0;i< usuarios.length;i++){
                user+="<li id=\"user\" class=\"list-group-item my-list collapse\">\n" +
                    "      <span id=\"help\" class=\"badge\">" +
                                mensagens.length+
                    "      </span>\n" +
                    "      <i id=\"username\">" +
                                usuarios[i].user.username+
                    "      </i>\n" +
                    "      <img id=\"imagem\" class=\"user-icon my-icon\" " +
                    "           src=\"/static/imagens/personagens/"+usuarios[i].user.imagem+"\">\n" +
                    "      <div id=\"mensagem\" class=\"text-left my-msg\">\n" +
                                status+
                    "      </div>\n" +
                    "  </li>"

            }
            $('#online').html(user)

            setTimeout(load_users, 1000);
        },
        error: function (error) {
            load_user_error+=1
            if(load_user_error <= 5){
                setTimeout(load_users, 1000);
            }
            console.error(error)
        }
    })
}