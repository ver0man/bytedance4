$(document).ready(function () {
    // initialize
    $('#cover_img_select').formSelect();

    // Get CSRF cookie
    var csrftoken = Cookies.get('csrftoken');

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // Use wangEditor
    var E = window.wangEditor;
    var editor = new E('#editor-toolbar', '#editor');
    editor.customConfig = {
        pasteFilterStyle: true,
        pasteIgnoreImg: false,
        pasteTextHandle: function (content) {
            return content + '<p>记得注明出处哦～</p>';
        },
        uploadImgServer: 'image_upload/',
        uploadImgHeaders: {
            'X-CSRFToken': csrftoken,
        },
        linkImgCallback: function (url) {
            // console.log(url) // url 即插 入图片的地址
        },

        linkCheck: function (text, link) {
            // console.log(text); // 插入的文字
            // console.log(link); // 插入的链接

            return true
        },
    };

    editor.create();

    $('#article_save').on('click', function (e) {

        var body = editor.txt.html();
        var filterbody = filterXSS(body);

        var data = $('#editing_article').serializeArray();
        data.push({name: 'body', value: filterbody});
        data.push({name: 'cover', value: $('#cover_img_select').val()});

        $.ajax({
            type: 'POST',
            url: '/editor/save/',
            data: data,
            success: function (result) {
                M.toast({
                    html: result.message,
                    displayLength: 5000,
                    inDuration: 300,
                    outDuration: 375,
                })
            },
            fail: function (result) {
                M.toast({
                    html: '保存失败！',
                    displayLength: 5000,
                    inDuration: 300,
                    outDuration: 375,
                })
            }
        });
    });

    // Function for wrapper
    function materialize_pagination() {
        let page_current = $('#cover_image_pagination > .endless_page_current > strong').html();
        $('#cover_image_pagination > .endless_page_current').replaceWith("<li class='active'><a href='#!'>" + page_current + "</a></li>");
        $('#cover_image_pagination > .endless_page_link').wrap("<li class='waves-effect'></li>");
    }

    $.endlessPaginate({
        onCompleted: function (context, fragment) {
            materialize_pagination();
            $("#cover_img_select").imagepicker();
        }
    });

    materialize_pagination();
    // Function for initialize image picker
    $("#cover_img_select").imagepicker();
    // $("#cover_img_select").data('picker').sync_picker_with_select();


});


