compartimento = 5;
$(function() {
    $('#buscarCliente').click(function(){
        console.log($('tentativa de ajax').val())   
        $.get('/buscarCliente/'), function(resposta){
            console.log(resposta)
        }
    });
    $('.fa-pen-to-square').click(function(){
        var my_id = $(this).data('id')        
        $('#semana_hidden').val(my_id);
    });

    $('#placa').on('focusout', function() {
        let placa = $(this).val();
        $.getJSON('/buscarVeiculo/' + placa + '/', function(data) {
            $('#numeroEquipamento').val(data.numeroEquipamento);
            alert('foi');
            $('#compartimento').val(data.qtd_compartimentos);
            $('#CNPJ').val(data.documento);
        });
    });
});

$(document).ready(function(){
    $('#placa').on('focusout', function(){
        placa = $('#placa').val()
        $.getJSON('../buscarComp/'+placa, function(data){
            $('#compartimento').val(data['qtd_compartimentos']);
            $('#numeroEquipamento').val(data['numeroEquipamento']);
        });        
    });
});

function updateVolume(num_comp){    
    volume = parseFloat($('#volume'+num_comp).val())
    $('#tempo'+num_comp).val(volume*12)
    $('#volumeAr'+num_comp).val(volume*168)
}

function updateONU(num_comp){    
    $.getJSON('../buscarProduto/'+$('#combustivel'+num_comp).val(), function(data){
        $.each(data, function(index){
            $('#ONU'+num_comp).val(data['onu'])
        })
    })
}

