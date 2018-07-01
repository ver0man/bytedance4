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

    $('.comment_submit').on('click', function () {

        let data = quill.root.innerHTML;
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

    $('.reply').on('click', function () {

        let comment_card = $(this).closest('.comment');
        let comment_id = comment_card.attr('id').replace('comment', '');

        if (comment_card.has('#quill_editor' + comment_id).length) {
            $('#reply_section' + comment_id).remove();
        } else {
            let reply_quill = $("<div/>", {
                id: 'quill_editor' + comment_id,
                style: 'height: 150px; margin-bottom: 10px;'
            });
            let reply_button = $("<div class='right-align'></div>").append($("<button/>", {
                id: 'comment_submit' + comment_id,
                class: "btn waves-effect waves-light comment_submmit",
                type: 'submit',
                text: '发送'
            }));

            let reply_section = $("<div/>", {class: 'section', id: "reply_section" + comment_id});

            comment_card.append(reply_section.append(reply_quill, reply_button));

            var quill = new Quill('#quill_editor' + comment_id, {
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
        }

    })

    // Display comments
    // preciousContent.innerHTML = JSON.stringify(delta);
});


