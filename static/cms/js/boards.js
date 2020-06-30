var clajax = {
    'get': function (args) {
        args['method'] = 'get';
        this.ajax(args);
    },
    'post': function (args) {
        args['method'] = 'post';
        this.ajax(args);
    },
    'ajax': function (args) {
        // 设置csrftoken
        this._ajaxSetup();
        $.ajax(args);
    },
    '_ajaxSetup': function () {
        $.ajaxSetup({
            'beforeSend': function (xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    var csrftoken = $('meta[name=csrf-token]').attr('content');
                    xhr.setRequestHeader("X-CSRFToken", csrftoken)
                }
            }
        });
    }
};

$(function () {
    $("#add-board-btn").click(function (event) {
        event.preventDefault();
        clalert.alertOneInput({
            'text': '请输入板块名称！',
            'placeholder': '板块名称',
            'confirmCallback': function (inputValue) {
                clajax.post({
                    'url': '/cms/aboard/',
                    'data': {
                        'name': inputValue
                    },
                    'success': function (data) {
                        if (data['code'] === 200) {
                            window.location.reload();
                        } else {
                            clalert.alertInfo(data['message']);
                        }
                    }
                });
            }
        });
    });
});

$(function () {
    $(".edit-board-btn").click(function () {
        var self = $(this);
        var tr = self.parent().parent();
        var name = tr.attr('data-name');
        var board_id = tr.attr("data-id");

        clalert.alertOneInput({
            'text': '请输入新的板块名称！',
            'placeholder': name,
            'confirmCallback': function (inputValue) {
                clajax.post({
                    'url': '/cms/uboard/',
                    'data': {
                        'board_id': board_id,
                        'name': inputValue
                    },
                    'success': function (data) {
                        if (data['code'] === 200) {
                            window.location.reload();
                        } else {
                            clalert.alertInfo(data['message']);
                        }
                    }
                });
            }
        });
    });
});


$(function () {
    $(".delete-board-btn").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var board_id = tr.attr('data-id');
        clalert.alertConfirm({
            "msg": "您确定要删除这个板块吗？",
            'confirmCallback': function () {
                clajax.post({
                    'url': '/cms/dboard/',
                    'data': {
                        // form  input name value
                        'board_id': board_id
                    },
                    'success': function (data) {
                        if (data['code'] === 200) {
                            window.location.reload();
                        } else {
                            clalert.alertInfo(data['message']);
                        }
                    }
                })
            }
        });
    });
});