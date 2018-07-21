/*
 *
 * login-register modal
 * 
 */

function registerAjax() {
    if (!$('#tc_checkbox').is(':checked')) {
        $('#tab-register> .alert').remove();
        $('#tc_checkarea').after($('<div class="red-text alert" role="alert"></div>').text('You must agree Terms and Conditions to register in our site.'));
        return
    }
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
                $('#tab-register> .alert').remove();
                // Append the alert messages to the register modal
                var alert = $('<ul></ul>');
                var result_obj = JSON.parse(result);
                for (let key in result_obj) {
                    if (result_obj.hasOwnProperty(key)) {
                        let key_msg = result_obj[key];
                        key_msg.forEach(function (item) {
                            alert.append($('<li></li>').text(item.message));
                        })
                    }
                }
                $('#register-form').after($('<div class="red-text alert" role="alert"></div>').append(alert));
            }
        },
    }).fail(function () {
        $('input[type="password"]').val('');
        alert('System error!');
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

}

