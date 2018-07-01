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
});



