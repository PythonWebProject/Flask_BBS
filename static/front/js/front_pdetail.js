$(function () {
    $("#comment-btn").click(function (event) {
        event.preventDefault();

        var content = window.ue.getContent();
        var post_id = $("#post-content").attr("data-id");
        clajax.post({
            'url': '/acomment/',
            'data': {
                'content': content,
                'post_id': post_id
            },
            'success': function (data) {
                if (data['code'] === 200) {
                    window.location.reload();
                } else {
                    // clalert.alertInfo(data['message']);
                    clalert.alertConfirm({
                        'msg': '您还未登录，请登录后再评论!!',
                        'cancelText': '继续浏览',
                        'confirmText': '先登录再评论',
                        'cancelCallback': function () {
                            window.location.reload();
                        },
                        'confirmCallback': function () {
                            window.location = '/signin/';
                        }
                    });
                }
            }
        });
    });
});

//初始化UEditor
$(function () {
    var ue = UE.getEditor('editor', {
        'serverUrl': '/ueditor/upload',
        'toolbars': [
            ['fullscreen', 'source', 'undo', 'redo'],
            ['bold', 'italic', 'underline', 'fontborder', 'strikethrough', 'superscript', 'subscript', 'removeformat', 'formatmatch', 'autotypeset', 'blockquote', 'pasteplain', '|', 'forecolor', 'backcolor', 'insertorderedlist', 'insertunorderedlist', 'selectall', 'cleardoc']
        ]
    });
    window.ue = ue;
})