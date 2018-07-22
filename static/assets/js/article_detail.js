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

    // $.ajax({
    //     type: 'POST',
    //     url: 'load_comments/',
    //     data: '',
    //     success: function (result) {
    //         $('#comments').html(result);
    //         quill.setContents([{insert: '\n'}]);
    //     },
    //     fail: function (result) {
    //         $('#modal-login').open();
    //     }
    // });

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

//     quill.on('text-change', function(delta, oldDelta, source) {
//   if (source == 'api') {
//     console.log("An API call triggered this change.");
//   } else if (source == 'user') {
//     console.log("A user action triggered this change.");
//   }
// });

    $(document).on('click', '.comment_submit', function () {

        let quill_instance = Quill.find($(this).parent().siblings("[id^=quill_editor]")[0]);
        let data = {'comment': quill_instance.root.innerHTML};

        // Test for parent comment
        let is_reply = $(this).closest('div.section').attr('id');
        if (is_reply) {
            data['parent'] = is_reply.replace('reply_section', '');
        }

        $.ajax({
            type: 'POST',
            url: 'post_comments/',
            data: data,
            success: function (result) {
                $('#comments').html(result);
                quill.setContents([{insert: '\n'}]);
            },
            fail: function (result) {
                $('#modal-login').open();
            }
        });
    });

    $(document).on('click', '.reply', function () {

        let comment_card = $(this).closest('.comment');
        let comment_id = comment_card.attr('id').replace('comment', '');

        if (comment_card.next().has('#quill_editor' + comment_id).length) {
            $('#reply_section' + comment_id).remove();
        } else {
            let reply_quill = $("<div/>", {
                id: 'quill_editor' + comment_id,
                style: 'height: 150px; margin-bottom: 10px;'
            });
            let reply_button = $("<div class='right-align'></div>").append($("<button/>", {
                id: 'comment_submit' + comment_id,
                class: "btn waves-effect waves-light comment_submit",
                type: 'submit',
                text: '发送'
            }));

            let reply_section = $("<div/>", {class: 'section', id: "reply_section" + comment_id});

            comment_card.after(reply_section.append(reply_quill, reply_button));

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

    });

    $(document).on('click', '.comment_like', function () {
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

    // function materialize_pagination() {
    //     let page_current = $('#article_comments_pagination > .endless_page_current > strong').html();
    //     $('#article_comments_pagination > .endless_page_current').replaceWith("<li class='active'><a href='#!'>" + page_current + "</a></li>");
    //     $('#article_comments_pagination > .endless_page_link').wrap("<li class='waves-effect'></li>");
    // }
    //
    // $.endlessPaginate({
    //     onCompleted: function (context, fragment) {
    //         materialize_pagination();
    //     }
    // });
    //
    // materialize_pagination();

});


