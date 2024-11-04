// MADE WITH CHATGPT
// Function to handle form validation
(function () {
    'use strict';

    // Fetch all the forms we want to apply custom Bootstrap validation to
    var forms = document.querySelectorAll('.needs-validation');
    var submitButtons = document.querySelectorAll('.submit'); // Button class for submission

    // Loop over each button and attach a click event listener
    Array.prototype.slice.call(submitButtons).forEach(function (button) {
        button.addEventListener('click', function (event) {
            // Prevent default button behavior
            event.preventDefault();

            let isValid = true; // Assume the form is valid

            // Loop over each form and validate
            Array.prototype.slice.call(forms).forEach(function (form) {
                // Check validity of the form
                if (!form.checkValidity()) {
                    isValid = false; // Mark as invalid if any form is invalid
                    event.stopPropagation(); // Stop propagation if invalid
                }

                // Add Bootstrap validation classes
                form.classList.add('was-validated');
            });

            // If the form is valid, show the modal
            if (isValid) {
                console.log('add clicked');
                let title = $('#title').val(); // Get the title value
                $('.modal-body p').html('Are you sure you want to save the alterations to post titled <strong>' + title + '</strong>?');
                $('#edit-modal').modal("show"); // Show the modal
            }
        }, false);
    });

    // Handle modal confirmation for adding post
    $('#modal-edit-yes').click(function() {
        // Submit the form once the user confirms
        $('#editForm').submit(); // Trigger form submission
        // Optionally reset the form after a successful submission
    });
})();
