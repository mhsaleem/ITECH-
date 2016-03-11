$(document).ready(function () {
    // Login button click handler
    $('#newPunButton').on('click', function () {
        bootbox
            .dialog({
                title: 'New Pun',
                message: $('#newPunForm'),
                show: false // We will show it manually later
            })
            .on('shown.bs.modal', function () {
                $('#newPunForm')
                    .show()       ;                      // Show the login form
                    //.formValidation('resetForm', true); // Reset form
            })
            .on('hide.bs.modal', function (e) {
                // Bootbox will remove the modal (including the body which contains the login form)
                // after hiding the modal
                // Therefor, we need to backup the form
                $('#newPunForm').hide().appendTo('body');
            })
            .modal('show');
    });

    //$('#tokenfield').tokenfield({
    //    //autocomplete: {
    //    //    source: ['red', 'blue', 'green', 'yellow', 'violet', 'brown', 'purple', 'black', 'white'],
    //    //    delay: 100
    //    //},
    //    showAutocompleteOnFocus: true
    //});
    var maxCharacters = 350;
    var punBody = document.getElementById('punBody');
    var countLabel = document.getElementById('count');
    punBody.maxLength = maxCharacters;
    punBody.onkeyup = function () {
        countLabel.textContent = "Characters left: " + (maxCharacters - this.value.length);
    };
});
