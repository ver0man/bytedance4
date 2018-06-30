/*
 *
 * login-register modal
 * 
 */

function registerAjax() {
    // Get CSRF cookie
    var csrftoken = Cookies.get('csrftoken');

    // Validate CSRF
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // Handle the register
    $.ajax({
        type: "POST",
        url: '/accounts/register/',
        dataType: 'json',
        // Pass the user selection to the url
        data: $('#register-form').serialize(),
        // data: process_table.rows().data(),
        success: function (result) {
            if (result.status) {
                window.location.replace("/");
            } else {
                // Clean up the password fields..
                $('input[type="password"]').val('');
                // Remove the any previous alert..
                $('#registerFormBox > .alert').remove();
                // Append the alert messages to the register modal
                $('#registerFormBox').append('<div class="red-text" role="alert">\n <strong>' + result.message + '</strong>\n</div>');
            }
        },
    }).fail(function () {
        $('input[type="password"]').val('');
        alert('注册失败')
    })
}

function loginAjax() {
    // Get CSRF cookie
    var csrftoken = Cookies.get('csrftoken');

    // Validate CSRF
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $.post("/accounts/login/", $('#login-form').serialize(), function (result) {
        if (result.status) {
            window.location.replace("/");
        } else {
            $('input[type="password"]').val('');
            $('.login_error').addClass('red-text').html("Invalid email/password combination");
        }
    });

// // /*   Simulate error message from the server   */
// //      shakeModal();
// }
//
// function shakeModal(){
//     $('#modal-login .modal-dialog').addClass('shake');
//              $('.login_error').addClass('alert alert-danger').html("Invalid email/password combination");
//              $('input[type="password"]').val('');
//              setTimeout( function(){
//                 $('#modal-login .modal-dialog').removeClass('shake');
//     }, 1000 );
}

   