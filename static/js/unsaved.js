// chatgpt
$(document).ready(function() {
    let hasUnsavedChanges = false;

    // Track changes in input and textarea elements
    $('input, textarea').on('input', function() {
        hasUnsavedChanges = true; // Set flag when changes are made
    });

    // Reset the flag when the reset button is clicked
    $('.resetButton').on('click', function() {
        hasUnsavedChanges = false; // Reset flag when button is clicked
        // Optionally, clear the input fields
        $('input, textarea').val(''); // Clear all input and textarea fields
    });

    // Warn user about unsaved changes before leaving
    $(window).on('beforeunload', function(event) {
        if (hasUnsavedChanges) {
            const confirmationMessage = 'You have unsaved changes. Do you really want to leave?';
            event.returnValue = confirmationMessage; // Standard way to trigger the dialog
            return confirmationMessage; // Some browsers require this
        }
    });
});