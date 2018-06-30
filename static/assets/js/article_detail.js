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


    var quill = new Quill('#quill_editor', {
        modules: {
            toolbar: [
                [{header: [1, 2, 3, false]}],
                ['bold', 'italic', 'underline'],
                [{'list': 'ordered'}, {'list': 'bullet'}, {'indent': '-1'}, {'indent': '+1'}],
                ['image', 'link']
            ]
        },
        placeholder: '输入回复',
        theme: 'snow'  // or 'bubble'
    });

    console.log(quill.getContents());
//     quill.on('text-change', function(delta, oldDelta, source) {
//   if (source == 'api') {
//     console.log("An API call triggered this change.");
//   } else if (source == 'user') {
//     console.log("A user action triggered this change.");
//   }
// });

    $('#comment_submmit').on('click', function () {

        let data = quill.root.innerHTML;
        console.log(data);
        // Test for parent comment
        // if (xxx) {
        //
        // }
        $.ajax({
            type: 'POST',
            url: 'comments/',
            data: {'comment': data},
            success: function (result) {
                $('#comments').html(result);
                // quill.setContents([{insert: '\n'}]);
            },
            fail: function (result) {
                console.log('failed comment');
                $('#modal-login').open();
            }
        });
    });

    // Display comments
    // preciousContent.innerHTML = JSON.stringify(delta);
});


