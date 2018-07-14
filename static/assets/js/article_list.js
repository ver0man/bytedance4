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

    var $grid = $('.grid').masonry({
        // options
        itemSelector: '.grid-item',
        columnWidth: '.grid-sizer',
        gutter: '.gutter-sizer',
        percentPosition: true,
        stagger: 30,
    });

    // get Masonry instance
    var msnry = $grid.data('masonry');

    // Start the infinite scroll
    $('.infinite-container').infiniteScroll({
        // options
        path: '.infinite-more-link',
        append: '.grid-item',
        outlayer: msnry,
        status: '.loading',
        history: false,
    });

    // Add favorite button
    $('.like').on('click', function () {

        if ($(this).text() === 'favorite_border') {
            $('.like').fadeOut(100, function () {
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
            $('.like').fadeOut(100, function () {
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
            $('.bookmark').fadeOut(100, function () {
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
            $('.bookmark').fadeOut(100, function () {
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



