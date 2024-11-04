$(document).ready(
    function (){
        $('#modal-add-yes').click(
        function (){
            form = document.getElementById('addForm');
            form.submit();
        }
        );

        $('#previewButton').click(
        function (){
            console.log('preview')
            files = $('#file')[0].files
            if(files.length > 0)
            {
                let file = files[0];
                let reader = new FileReader();

                reader.onload = function(event){
                    let text = event.target.result
                    let title = $('#title').val();
                    let subtitle = $('#subtitle').val();
                    let image = $('#image').val();
                    loadPreview(text, title, subtitle, image);
                }

                reader.readAsText(file);
            }
            else
            {
                let text = $('#markdown').val();
                let title = $('#title').val();
                let subtitle = $('#subtitle').val();
                let image = $('#image').val();
                loadPreview(text, title, subtitle, image);
            }

        }
        );
});
 function loadPreview(markdown, title, subtitle, image){
    let form = document.createElement('form');
    form.method = 'POST';
    form.target = '_blank';
    form.action = '/admin/add_post/preview';
    form.style.display = 'none';

    let input1 = document.createElement('input');
    input1.type = 'hidden';
    input1.name = 'markdown';
    input1.value = markdown;
    form.appendChild(input1);

    let input2 = document.createElement('input');
    input2.type = 'hidden';
    input2.name = 'title';
    input2.value = title;
    form.appendChild(input2);

    let input3 = document.createElement('input');
    input3.type = 'hidden';
    input3.name = 'subtitle';
    input3.value = subtitle;
    form.appendChild(input3);

    let input4 = document.createElement('input');
    input4.type = 'hidden';
    input4.name = 'image';
    input4.value = image;
    form.appendChild(input4);

    document.body.appendChild(form);
    form.submit()
    document.body.removeChild(form);
 }