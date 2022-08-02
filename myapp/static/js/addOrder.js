$(function () {
    get_movies();
    update_theaterInput();
    update_roomInput();
    update_timeInput();
    update_sid();
    submit();
    init_something();
    addEvent_confirm();
});

function init_something() {
    $('input[name="oseat"]').attr('readonly', '');
}

function get_movies() {
    $.ajax({
        url: '/get/movies/',
        type: 'post',
        dataType: 'JSON',
        data: {},
        success: function (res) {
            sel = $('select[name="movie"]')
            sel.append('<option value="" selected="">---------</option>');
            cnt = res['data'].length;
            for (let i = 0; i < cnt; i++) {
                sel.append('<option value="' + res['data'][i]['mid'] + '" >' + res['data'][i]['mid'] + ' - ' + res['data'][i]['mname'] + '</option>');
            }
        },
        error: function (res) {
            alert('获取电影信息失败');
        }
    })
}


function update_theaterInput() {
    $('select[name="movie"]').on("change", function () {
        $.ajax({
            url: '/get/theaters/',
            type: 'post',
            dataType: 'JSON',
            data: {
                mid: $(this).val(),
            },
            success: function (res) {
                sel = $('select[name="theater"]');
                sel.empty();
                sel.append('<option value="" selected="">---------</option>');
                cnt = res['data'].length;
                for (let i = 0; i < cnt; i++) {
                    sel.append('<option value="' + res['data'][i]['tid'] + '" >' + res['data'][i]['tid'] + ' - ' + res['data'][i]['tname'] + '</option>');
                }
            },
            error: function (res) {
                alert('获取影院信息失败');
            }
        });
    });
}

//根据影院数据填充放映厅
function update_roomInput() {
    $('select[name="theater"]').on("change", function () {
        $.ajax({
            url: '/get/room/',
            type: 'post',
            dataType: 'JSON',
            data: {
                movie: $('select[name="movie"]').val(),
                theater: $(this).val(),
            },
            success: function (res) {
                sel = $('select[name="room"]');
                sel.empty();
                sel.append('<option value="" selected="">---------</option>');
                cnt = res['data'].length;
                for (let i = 0; i < cnt; i++) {
                    sel.append('<option value="' + res['data'][i]['rid'] + '" >' + res['data'][i]['rid'] + ' - ' + res['data'][i]['rname'] + '</option>');
                }
            },
            error: function (res) {
                alert('获取放映厅信息失败');
            }
        });
    });
}

function update_timeInput() {
    $('select[name="room"]').on("change", function () {
        $.ajax({
            url: '/get/time/',
            type: 'post',
            dataType: 'JSON',
            data: {
                movie: $('select[name="movie"]').val(),
                theater: $('select[name="theater"]').val(),
                room: $(this).val(),
            },
            success: function (res) {
                sel = $('select[name="time"]');
                sel.empty();
                sel.append('<option value="" selected="">---------</option>');
                cnt = res['data'].length;
                for (let i = 0; i < cnt; i++) {
                    sel.append('<option value="' + res['data'][i] + '" >' + res['data'][i] + '</option>');
                }
            },
            error: function (res) {
                alert('获取放映厅信息失败');
            }
        });
    });
}

function update_sid() {
    $('select[name="time"]').on("change", function () {
        $.ajax({
            url: '/get/sid/',
            type: 'post',
            dataType: 'JSON',
            data: {
                movie: $('select[name="movie"]').val(),
                theater: $('select[name="theater"]').val(),
                room: $('select[name="room"]').val(),
                time: $(this).val()
            },
            success: function (res) {
                sel = $('select[name="sid"]');
                sel.empty();
                sel.append('<option value="" selected="">---------</option>');
                cnt = res['data'].length;
                for (let i = 0; i < cnt; i++) {
                    sel.append('<option value="' + res['data'][i] + '" >' + res['data'][i] + '</option>');
                }
            },
            error: function (res) {
                alert('获取放映信息失败');
            }
        });
    });
}


function submit() {
    $('div[name="submit"]').click(function () {
        uid = $('select[name="uid"]').val();
        sid = $('select[name="sid"]').val();
        oseat = $('input[name="oseat"]').val();
        errors = []
        if (! uid) {
            errors.push('用户名为空');
        }
        if (! sid) {
            errors.push('放映编号为空');
        }
        if (! oseat) {
            errors.push('座位号为空');
        }
        if (errors.length) {
            alert_errors(errors);
            return;
        }
        $.ajax({
            url: '/check/order/',
            type: 'post',
            dataType: 'JSON',
            data: {
                op: 'admin',
                uid: $('select[name="uid"]').val(),
                sid: $('select[name="sid"]').val(),
                oseat: $('input[name="oseat"]').val()
            },
            success: function (res) {
                if (res['status'] == 'success') {
                    $('#form').submit();
                } else {
                    errors = res['errors'];
                    alert_errors(errors);
                }
            }
        });
    });
}

function alert_errors(errors) {
    info_box = $('div[name="info-box"]')
    info_box.css('display', 'block');
    $('div[name="tips"]').empty();
    for (i in errors) {
        $('div[name="tips"]').append('<p class="tip">' + errors[i] + '</p>')
    }
}


function addEvent_confirm() {
            $('#confirm-btn').click(function () {
                $('div[name="info-box"]').css('display', 'none');
            });
        }