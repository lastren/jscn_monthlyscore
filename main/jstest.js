$(document).ready(function(){
    $.ajaxSetup({
        data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
    });

$('.modal').modal({
backdrop:false,
show:false
})

$('#taskModal').on('show.bs.modal', function (event) {
var button = $(event.relatedTarget) // Button that triggered the modal
var taskid = button.data('tid')
var taskdesc = button.data('tdesc')
var taskdone = button.data('tdone')
var tasktype= button.data('type')

var modal = $(this)
modal.find('#taskid').val(taskid)
modal.find('#tasktype').val(tasktype)
modal.find('#desc').val(taskdesc)
modal.find('#done').val(taskdone)


})

    $("#taskmodalsubmit").click(function(){
        var modal = $('#taskModal')
        var reportid = $('#reportid').val()

        var taskid = modal.find('#taskid').val()
        var taskdesc = modal.find('#desc').val()
        var taskdone = modal.find('#done').val()
        var tasktype = modal.find('#tasktype').val()

        $.post("{% url 'main:ajaxedittask' %}",{
            'reportid':reportid,
            'taskid':taskid,
            'taskdesc':taskdesc,
            'taskdone':taskdone,
            'tasktype':tasktype
            },
            function(data,status){
                modal.modal('hide')
                <!--获取从cookie里传过来的tasktype-->
                var tasktype = Cookies.get('tasktype')
                switch(tasktype){
                    case '1':
                        $("#taskareaL").html(data);
                        break;
                    case '2':
                        $("#taskareaS").html(data);
                        break;
                    case '3':
                        $("#taskareaD").html(data);
                        break;
                }
                <!--用完后删除cookie里的tasktype-->
                 Cookies.remove('tasktype');
            });
        });

    $(".deletetask").on("click",function(){
        var taskid = this.data('tid')
        console.log('delete')
        console.log(taskid)
        if(confirm('确认删除？')==true){
            $.post("{% url 'main:ajaxdeletetask' %}",{'taskid':taskid},function(data,status){
                <!--获取从cookie里传过来的tasktype-->
                var tasktype = Cookies.get('tasktype')
                console.log("delete::" + tasktype)
                switch(tasktype){
                    case '1':
                        $("#taskareaL").html(data);
                        break;
                    case '2':
                        $("#taskareaS").html(data);
                        break;
                    case '3':
                        $("#taskareaD").html(data);
                        break;
                }
                <!--用完后删除cookie里的tasktype-->
                Cookies.remove('tasktype');
            });
        }
    });


});