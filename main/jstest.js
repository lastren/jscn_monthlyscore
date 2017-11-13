$(document).ready(function(){
    $.ajaxSetup({
        data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
    });

    $('#datetimepicker').datetimepicker({
        language:'zh-CN',
        format:"yyyy-MM",
        autoclose: true,
        startView:3,
        minView:3
    }).on('changeDate', function(ev){
         $.post("{% url 'main:ajaxgetreports' %}",{
            'month':ev.date.valueOf()
            },
            function(data,status){
                $("#reportlistarea").html(data);
            });
        });

});

