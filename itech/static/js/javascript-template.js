$(document).ready(function () {
    var url = window.location.href;
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
                    .show();                      // Show the login form
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

    $(document).on('click', '.upbutton', function () {
        var x = $(this).attr('upvoteurl')
        $.get(x, function () {
            $.ajax({
                url: url,
                success: function (data) {
                    // grab the inner html of the returned div
                    // so you don't nest a new div#refresh-this-div on every call
                    var html = $(data).filter('#timeline').html();
                    $('#timeline').html(html);
                }
            });
        })
    });

    $(document).on('click', '.downbutton', function () {
        var x = $(this).attr('downvoteurl');
        $.get(x, function () {
            $.ajax({
                url: url,
                success: function (data) {
                    // grab the inner html of the returned div
                    // so you don't nest a new div#refresh-this-div on every call
                    var html = $(data).filter('#timeline').html();
                    console.log(html)
                    $('#timeline').html(html);
                }
            });
        })
    });
    var notification = $('#pun_posted_confirm')
    msg = $.cookie('message')
    if (msg) {
        notification.show()
        setTimeout(function () {
            notification.fadeOut().empty();
        }, 2000);
    };

    var maxCharacters = 350;
    var punBody = document.getElementById('punBody');
    var countLabel = document.getElementById('count');
    punBody.maxLength = maxCharacters;
    punBody.onkeyup = function () {
        countLabel.textContent = "Characters left: " + (maxCharacters - this.value.length);
    };
});


