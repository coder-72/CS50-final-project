$(document).ready(
    function(){
        $('.delete-button').click(
        function (){
        console.log('delete clicked')
            let target = $(this).data('delete-id');
            let name = $(this).data('delete-name');
            $('.modal-body p').html('Are you sure you want to delete the post <strong>' + name + '</strong>?');
            $('#delete-modal').data('delete-id', target);
            $('#delete-modal').modal('show');
        }
        );
        $('#modal-delete-yes').click(
        function (){
            let id = $('#delete-modal').data('delete-id');
            deletePost(id);
            location.reload(true);
        }
        );
});

function deletePost(target_id) {
    $.ajax({
        url: del_endpoint,
        method: 'DELETE',
        contentType: 'application/json',
        data: JSON.stringify({id : target_id}),
        dataType: 'json',
        error: function(xhr, status, error) {console.log(status, error);},
        success: function(response){
            console.log('success deleteing post');
        }
    });

}