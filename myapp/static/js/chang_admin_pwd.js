$(function () {
    confirmPWD();
    hideError();
});
function confirmPWD() {
    $('button[name="confirm-pwd"]').click(function () {
        let pwd1 = $('input[name="pwd1"]').val();
        let pwd2 = $('input[name="pwd2"]').val();
        let tip = $('span[name="error"]');
        if (!pwd1) {
            tip.css('display', 'inline');
            tip.text('密码不能为空');
        }
        else if (pwd1 != pwd2) {
            tip.css('display', 'inline');
            tip.text('两次输入的密码不一致');
        } else {
            // 提交更改密码
            $.ajax({
                url: '/admin/change/pwd/',
                type: 'post',
                dataType: 'JSON',
                data: {
                    id: $('div[name="id"]').text(),
                    pwd: pwd1,
                },
                success: function (res) {
                    if (res.status == 'success') {
                        $('#myModal').modal('toggle');
                        alert('密码修改成功');
                    } else {
                        alert('修改密码失败， 请稍后重试');
                    }
                },
                error: function (res) {
                    alert('修改密码失败，请稍后重试');
                }
            })
        }

    });
}

function hideError() {
    $('input[name="pwd1"]').on('input propertychange', function () {
         $('span[name="error"]').css('display', 'none');
    });
    $('input[name="pwd2"]').on('input propertychange', function () {
         $('span[name="error"]').css('display', 'none');
    });
}