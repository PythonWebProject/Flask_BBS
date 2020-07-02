$(function () {
    $("#captcha-btn").click(function (event) {
        event.preventDefault();
        var email = $("input[name='email']").val();
        if (!email) {
            clalert.alertInfoToast('请输入邮箱');
            return;
        }
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
        clajax.get({
            'url': '/cms/email_captcha/',
            'data': {
                'email': email
            },
            'success': function (data) {
                if (data['code'] === 200) {
                    clalert.alertSuccessToast('邮件发送成功！请注意查收！');
                } else {
                    clalert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
                clalert.alertNetworkError();
            }
        });
    });
});

$(function () {
    $("#submit").click(function (event) {
        event.preventDefault();
        var emailE = $("input[name='email']");
        var captchaE = $("input[name='captcha']");

        var email = emailE.val();
        var captcha = captchaE.val();

        clajax.post({
            'url': '/cms/resetemail/',
            'data': {
                'email': email,
                'captcha': captcha
            },
            'success': function (data) {
                if (data['code'] === 200) {
                    emailE.val("");
                    captchaE.val("");
                    clalert.alertSuccessToast('恭喜！邮箱修改成功！');
                } else {
                    clalert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
                clalert.alertNetworkError();
            }
        });
    });
});