$(document).ready(
    function (){
        $('#previewButton').click(
        function (){
            files = $('#file')[0].files
            if(files.length > 0)
            {
                let file = files[0];
                let reader = new FileReader();

                reader.onload = function(event){
                    loadPreview(event.target.result);
                }

                reader.readAsText(file);
            }
            else
            {
                let text = $('#markdown').val();
                loadPreview(text);
            }

        }
        );
});
 function loadPreview(markdown){
    let form = document.createElement('form');
    form.method = 'POST';
    form.target = '_blank';
    form.action = '/admin/add_post/preview';
    form.style.display = 'none';

    let input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'markdown';
    input.value = markdown;
    form.appendChild(input);

    document.body.appendChild(form);
    form.submit()
    document.body.removeChild(form);
 }