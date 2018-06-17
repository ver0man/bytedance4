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

    // Use wangEditor
    var E = window.wangEditor;
    var editor = new E('#editor-toolbar', '#editor');

    // 关闭粘贴样式的过滤
    editor.customConfig.pasteFilterStyle = true;
    // 忽略粘贴内容中的图片
    editor.customConfig.pasteIgnoreImg = false;
    // 自定义处理粘贴的文本内容
    editor.customConfig.pasteTextHandle = function (content) {
        // return content + '<p>粘贴做什么？！</p>'
        return content;
    };
    // For images
    editor.customConfig.uploadImgServer = 'image_upload/';
    // For django requirement
    editor.customConfig.uploadImgHeaders = {
        'X-CSRFToken': csrftoken,
    };

    editor.create();

    $('#article_save').on('click', function (e) {

        var body = editor.txt.html();
        var filterbody = filterXSS(body);

        var data = $('#editing_article').serializeArray();
        data.push({name: 'body', value: filterbody});

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
    })

// Activate FAB
// $('.fixed-action-btn').floatingActionButton({
//     'direction':'top',
// });

});


