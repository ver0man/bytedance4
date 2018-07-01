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
            url: 'comments/',
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
                class: "btn waves-effect waves-light comment_submit",
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

    });

    // Display comments
    // preciousContent.innerHTML = JSON.stringify(delta);
    var like_button = document.getElementById("like-button");
    if (like_button) {
        like_button.addEventListener("click", doLikeButton);
    }

    function doLikeButton(e) {
        toggleButton(e.target);
    }

    function toggleButton(button) {
        button.classList.remove('liked-shaked');
        button.classList.toggle('liked');
        button.classList.toggle('not-liked');
        button.classList.toggle('fa-heart-o');
        button.classList.toggle('fa-heart');

        if (button.classList.contains("liked")) {
            button.classList.add('liked-shaked');
        }
    }

});


