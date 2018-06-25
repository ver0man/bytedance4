$(document).ready(function () {

    // Get CSRF cookie
    var csrftoken = Cookies.get('csrftoken');

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $('#article').find('p').css('font', '1.5em');
    $('#article').find('p').addClass('float-text');
    $('#article').find('img').addClass('materialboxed responsive-img');

    $('.materialboxed').materialbox();


});


