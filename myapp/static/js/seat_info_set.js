$(function () {

    /*
        {#0: 可选#}
        {#1: 已售#}
        {#2: 无位置#}
     */
    draw();
    addEvent_update_seat();
    addEvent_input();
    addEvent_update_status();
});

// 根据输入框中的变量影响 座位布局
function update_seat_info() {
    let seat_layout = {
        center_offset: 0, // 偏移量
        row: 0,
        col: 0,
        info: '',
    };
    seat_layout.row = $('input[name="r_row"]').val();
    seat_layout.col = $('input[name="r_col"]').val();
    seat_layout.center_offset = $('input[name="rscreen_offset"]').val();
    seat_layout.info = $('input[name="rseat"]').val();
    count = seat_layout.row * seat_layout.col;
    if (seat_layout.info.length != count) {
        let str = '';
        for (let i = 0; i < count; i++) {
            str += '0';
        }
        seat_layout.info = str;
        $('input[name="rseat"]').val(str);
    }
    return seat_layout;
}

function init(seat_layout) {
    $('.screen-container').css('left', seat_layout.center_offset + 'px');
    // console.log(seat_layout.info);
    str = seat_layout.info;
    for (let i = 0; i < seat_layout.row; i++) {
        $('.seats-block .seats-wrapper').append('<div class="row" rowid=' + i + '></div>');
        $('.row-id-container').append('<span class="row-id">' + (i + 1) + '</span>');
        for (let j = 0; j < seat_layout.col; j++) {
            let idx = str[i * seat_layout.col + j];
            if (idx === '0') {
                $('.seats-block .seats-wrapper .row').eq(i).append('<span class="seat" data-column-id="' + (j + 1) + '" data-row-id="' + (i + 1) + '" status="' + idx + '"></span>');
            } else if (idx === '1') {
                $('.seats-block .seats-wrapper .row').eq(i).append('<span class="seat sold" data-column-id="' + (j + 1) + '" data-row-id="' + (i + 1) + '"status="' + idx + '"></span>');
            } else if (idx === '2'){
                $('.seats-block .seats-wrapper .row').eq(i).append('<span class="seat empty" data-column-id="' + (j + 1) + '" data-row-id="' + (i + 1) + '"status="' + idx + '"></span>');
            }
        }
    }

    w = $('.seats-wrapper').width();
    if (w > 550) {
        $('.seats-block .screen-container .screen').css('width', $('.seats-wrapper').width() + 'px');
    }
    $('.screen-container').css('left', seat_layout.center_offset + 'px');
}

function addEvent_input() {
    $('input[class="form-control"]').on("input propertychange", function () {
        draw();
        addEvent_update_status();
    });
}

/*
    通过点击按钮 将自定义座位布局 转换 布局字符串 并画图
 */
function addEvent_update_seat() {
    $('button[id="update-info"]').click(function () {
        $('.seats-wrapper').empty();
        $('.row-id-container').empty();
        addEvent_update_status();
        init(update_seat_info());
    });
}

/*
    更新信息并画图
 */
function draw() {
    $('.seats-wrapper').empty();
    $('.row-id-container').empty();
    init(update_seat_info());
    update_size();
}

function get_string() {
    return $('input[name="rseat"]').val();
}


function addEvent_update_status() {
    $('.row').off("click").on('click', '.seat', function () {
        let seat = $(this);
        // null -> sold -> empty
        let status = seat.attr('status');
        seat.attr('status', (status + 1) % 3);
        status = seat.attr('status');
        if (status == 0) {
            seat.removeClass('sold');
            seat.removeClass('empty');
            seat.addClass('seat');
        } else if (status == 1) {
            seat.removeClass('sold');
            seat.removeClass('empty');
            seat.addClass('sold');
        } else {
            seat.removeClass('sold');
            seat.removeClass('empty');
            seat.addClass('empty');
        }
        cols = $('input[name="r_col"]').val();
        r = seat.attr('data-row-id');
        c = seat.attr('data-column-id');
        input = $('input[name="rseat"]');
        old_str = input.val();
        target = (r - 1) * cols + Number(c - 1);
        new_str = old_str.substring(0, target) + status + old_str.substring(target + 1);
        input.val(new_str);

        update_size();
    });
}

function get_size() {
    str = get_string();
    let res = 0;
    for (let i = 0; i < str.length; i ++) {
        if (str[i] == '0') res ++;
    }
    return res;
}

function update_size() {
    input = $('input[name="rsize"]');
    input.val(Number(get_size()));
    // console.log(Number(get_size()));
}
