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
    var editor = new E('#editor');

    // // 关闭粘贴样式的过滤
    // editor2.customConfig.pasteFilterStyle = true;
    // // 忽略粘贴内容中的图片
    // editor2.customConfig.pasteIgnoreImg = false;
    // // 自定义处理粘贴的文本内容
    // editor2.customConfig.pasteTextHandle = function (content) {
    //     // content 即粘贴过来的内容（html 或 纯文本），可进行自定义处理然后返回
    //     return content + '<p>粘贴？！</p>'
    // };

    editor.customConfig.uploadImgServer = 'image_upload/';
    // editor.customConfig.uploadImgParams = {
    //     // 如果版本 <=v3.1.0 ，属性值会自动进行 encode ，此处无需 encode
    //     // 如果版本 >=v3.1.1 ，属性值不会自动 encode ，如有需要自己手动 encode
    //     images: 'test',
    // };
    editor.customConfig.uploadImgHeaders = {
        'X-CSRFToken': csrftoken,
    };
    editor.customConfig.uploadFileName = 'image';
    // editor.customConfig.uploadImgHooks = {
    //     before: function (xhr, editor, files) {
    //         // 图片上传之前触发
    //         // xhr 是 XMLHttpRequst 对象，editor 是编辑器对象，files 是选择的图片文件
    //         // xhr.setRequestHeader('X-CSRFToken', csrftoken);
    //         // 如果返回的结果是 {prevent: true, msg: 'xxxx'} 则表示用户放弃上传
    //         // return {
    //         //     prevent: true,
    //         //     msg: '放弃上传'
    //         // }
    //     },
    //     success: function (xhr, editor, result) {
    //         // 图片上传并返回结果，图片插入成功之后触发
    //         // xhr 是 XMLHttpRequst 对象，editor 是编辑器对象，result 是服务器端返回的结果
    //
    //     },
    //     fail: function (xhr, editor, result) {
    //         // 图片上传并返回结果，但图片插入错误时触发
    //         // xhr 是 XMLHttpRequst 对象，editor 是编辑器对象，result 是服务器端返回的结果
    //     },
    //     error: function (xhr, editor) {
    //         // 图片上传出错时触发
    //         // xhr 是 XMLHttpRequst 对象，editor 是编辑器对象
    //     },
    //     timeout: function (xhr, editor) {
    //         // 图片上传超时时触发
    //         // xhr 是 XMLHttpRequst 对象，editor 是编辑器对象
    //     },
    //
    //     // 如果服务器端返回的不是 {errno:0, data: [...]} 这种格式，可使用该配置
    //     // （但是，服务器端返回的必须是一个 JSON 格式字符串！！！否则会报错）
    //     customInsert: function (insertImg, result, editor) {
    //         // 图片上传并返回结果，自定义插入图片的事件（而不是编辑器自动插入图片！！！）
    //         // insertImg 是插入图片的函数，editor 是编辑器对象，result 是服务器端返回的结果
    //
    //         // 举例：假如上传图片成功后，服务器端返回的是 {url:'....'} 这种格式，即可这样插入图片：
    //         var url = result.url;
    //         insertImg(url)
    //
    //         // result 必须是一个 JSON 格式字符串！！！否则报错
    //     }
    // };


    // editor2.customConfig.linkImgCheck = function (src) {
    //     console.log(src); // 图片的链接
    //
    //     return true // 返回 true 表示校验成功
    //     // return '验证失败' // 返回字符串，即校验失败的提示信息
    // };
    //

    editor.create();

    $('#article_save').on('click', function (e) {
        $.ajax({
            type: 'POST',
            url: '/articles/save/',
            data: $('#test').html(),
            success: function (result) {
                // location.href = '/articles/'
            }
        });
    })

// Activate FAB
// $('.fixed-action-btn').floatingActionButton({
//     'direction':'top',
// });

});


