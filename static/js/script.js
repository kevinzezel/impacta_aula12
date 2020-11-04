$('#menu_consultar').on('click',function(){
    $('#menu_consultar').addClass("active");
    $('#menu_cadastrar').removeClass("active");
    $('#menu_deletar').removeClass("active");
    $('#menu_alterar').removeClass("active");

    $('#consultar').css('display','');
    $('#cadastrar').css('display','none');
    $('#deletar').css('display','none');
    $('#alterar').css('display','none');
});
$('#menu_cadastrar').on('click',function(){
    $('#menu_cadastrar').addClass("active");
    $('#menu_consultar').removeClass("active");
    $('#menu_deletar').removeClass("active");
    $('#menu_alterar').removeClass("active");

    $('#consultar').css('display','none');
    $('#cadastrar').css('display','');
    $('#deletar').css('display','none');
    $('#alterar').css('display','none');
});
$('#menu_alterar').on('click',function(){
    $('#menu_cadastrar').removeClass("active");
    $('#menu_consultar').removeClass("active");
    $('#menu_deletar').removeClass("active");
    $('#menu_alterar').addClass("active");

    $('#consultar').css('display','none');
    $('#cadastrar').css('display','none');
    $('#deletar').css('display','none');
    $('#alterar').css('display','');
});
$('#menu_deletar').on('click',function(){
    $('#menu_cadastrar').removeClass("active");
    $('#menu_consultar').removeClass("active");
    $('#menu_deletar').addClass("active");
    $('#menu_alterar').removeClass("active");

    $('#consultar').css('display','none');
    $('#cadastrar').css('display','none');
    $('#deletar').css('display','');
    $('#alterar').css('display','none');
});

// $('#formulario').on('submit',function(){
//     if (($('#rg').val() == '') || 
//     ($('#primeiro_nome').val() == '') || 
//     ($('#ultimo_nome').val() == '')|| 
//     ($('#telefone').val() == '')|| 
//     ($('#email').val() == '')|| 
//     ($('comentarios').val() == '')){
//         alert('Preencha todos os campos!!!');
//         return false
//     }else{
//         return true
//     }
// });