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
            console.log(url) // url 即插入图片的地址
        },

        linkCheck: function (text, link) {
            console.log(text); // 插入的文字
            console.log(link); // 插入的链接

            return true // 返回 true 表示校验成功
            // return '验证失败' // 返回字符串，即校验失败的提示信息
        }
    };
//     // 关闭粘贴样式的过滤
//     editor.customConfig.pasteFilterStyle = true;
//     // 忽略粘贴内容中的图片
//     editor.customConfig.pasteIgnoreImg = false;
//     // 自定义处理粘贴的文本内容
//     editor.customConfig.pasteTextHandle = function (content) {
//         return content + '<p>记得注明出处：华尔街扛把子哦～</p>';
//     };
//     // For images
//     editor.customConfig.uploadImgServer = 'image_upload/';
//     // For django requirement
//     editor.customConfig.uploadImgHeaders = {
//
//     };
//     editor.customConfig.linkImgCallback = function (url) {
//     console.log(url) // url 即插入图片的地址
// }

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

    $("#cover_img_select").imagepicker();
    // $("#cover_img_select").data('picker').sync_picker_with_select();


});


