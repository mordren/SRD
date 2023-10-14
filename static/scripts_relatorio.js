var compartimento = 0;

function imprimir(num){    
    for (let i=1; i<num; i++){          
        j = i + 1
        //clone dos formulários
        $('#formInteiro'+i).clone().appendTo('#lugarPracolar').prop('id', 'formInteiro'+j)

        $('#formInteiro'+j).children().find('#titulo'+i).prop('id', 'titulo'+j).text('Compartimento : '+j)
        $('#formInteiro'+j).children().find('#volume'+i).prop('id', 'volume'+j).prop('name', 'volume'+j).on('focusout', function(){ updateVolume() })
        $('#formInteiro'+j).children().find('#combustivel'+i).prop('id', 'combustivel'+j).prop('name', 'combustivel'+j).on('focusout', function(){ updateONU() })
        $('#formInteiro'+j).children().find('#ONU'+i).prop('id', 'ONU'+j).prop('name', 'ONU'+j)
        $('#formInteiro'+j).children().find('#classeRisco'+i).prop('id', 'classeRisco'+j).prop('name', 'classeRisco'+j).val('3')
        $('#formInteiro'+j).children().find('#pressaoVapor'+i).prop('id', 'pressaoVapor'+j).prop('name', 'pressaoVapor'+j).val('NA')
        $('#formInteiro'+j).children().find('#massaVapor'+i).prop('id', 'massaVapor'+j).prop('name', 'massaVapor'+j).val('NA')
        $('#formInteiro'+j).children().find('#tempo'+i).prop('id', 'tempo'+j).prop('name', 'tempo'+j)
        $('#formInteiro'+j).children().find('#volumeAr'+i).prop('id', 'volumeAr'+j).prop('name', 'volumeAr'+j)
        $('#formInteiro'+j).children().find('#neutralizante'+i).prop('id', 'neutralizante'+j).prop('name', 'neutralizante'+j).val('NA')
    }
}

$(document).ready(function(){
    var id = $(".hidden").attr('id')
    $.ajax({
        url: '../buscarRelatorio/'+id,
        type: "GET",
        dataType: "JSON",
        success: function(data){
            $.ajax({
                url: '../buscarComp/'+data['placa'],
                type: "GET",
                dataType: "JSON",
                success: function (data2) { 
                    compartimento = data2['num']
                    imprimir(data2['num'])  
                },
                error: function(errorThown){
                    alert('Erro Compartimento')
                }
            })
        },
        error: function(errorThown){
            alert('Erro Relatório')
        }
    })

    $('#volume1').on("focusout", function(){
        volume = parseInt($('#volume1').val())
        $('#tempo1').val(volume*12)
        $('#volumeAr1').val(volume*168)
    });
});

function updateONU(){   
    num = compartimento
    for (let i=1; i<=num; i++){    
        if($('#combustivel'+i).val() != '')
            $.getJSON('../buscarProduto/'+$('#combustivel1').val(), function(data){
                $.each(data, function(index){
                    $('#ONU'+i).val(data['onu'])
                })
            })
    }
}