// MADE WITH CHATGPT
    // Function to handle form validation
    (function () {
        'use strict';

        // Fetch all the forms we want to apply custom Bootstrap validation to
        var forms = document.querySelectorAll('.needs-validation');

        // Loop over them and prevent submission if form is invalid
        Array.prototype.slice.call(forms)
            .forEach(function (form) {
                form.addEventListener('submit', function (event) {
                    if (!form.checkValidity()) {
                        event.preventDefault();
                        event.stopPropagation();
                    }

                    form.classList.add('was-validated');
                }, false);
            });
    })();

