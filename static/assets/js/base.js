$(document).ready(function () {
    // Initialize
    $('.modal').modal();
    // $(".dropdown-trigger").dropdown();
    $('.tabs').tabs();
    $('.carousel').carousel();
    $('.collapsible').collapsible();
    $('.fixed-action-btn').floatingActionButton();
    $('.materialboxed').materialbox();
    $('.sidenav').sidenav();
    $('input#username').characterCounter();


    var elems = document.querySelectorAll('.dropdown-trigger');
    var instances = M.Dropdown.init(elems, {'coverTrigger': false});

    // Get CSRF cookie
    var csrftoken = Cookies.get('csrftoken');

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // Add favorite button
    $('.like').on('click', function () {

        if ($(this).text() === 'favorite_border') {
            $(this).fadeOut(100, function () {
                $(this).text('favorite').fadeIn(10);
            });
            M.toast({
                html: $('<div class="flow-text">Liked~</div>'),
                displayLength: 2000,
                inDuration: 300,
                outDuration: 375,
                classes: 'pink rounded',
            });
        } else {
            $(this).fadeOut(100, function () {
                $(this).text('favorite_border').fadeIn(10);
            });
            M.toast({
                html: $('<div class="flow-text">Unliked</div>'),
                displayLength: 2000,
                inDuration: 300,
                outDuration: 375,
                classes: 'pink rounded',
            })
        }

    });

    // Add favorite button
    $('.bookmark').on('click', function () {

        if ($(this).text() === 'bookmark_border') {
            $(this).fadeOut(100, function () {
                $(this).text('bookmark').fadeIn(10);
            });
            M.toast({
                html: $('<div class="flow-text">Mark!</div>'),
                displayLength: 2000,
                inDuration: 300,
                outDuration: 375,
                classes: 'blue rounded',
            });
        } else {
            $(this).fadeOut(100, function () {
                $(this).text('bookmark_border').fadeIn(10);
            });
            M.toast({
                html: $('<div class="flow-text">Unmark</div>'),
                displayLength: 2000,
                inDuration: 300,
                outDuration: 375,
                classes: 'blue rounded',
            })
        }

    });

});