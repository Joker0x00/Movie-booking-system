$(function () {
    addEvent_update_status();
    update_seat();
});

// 获取座位布局
function update_seat_info() {
    var seat_layout = {
        center_offset: 0, // 偏移量
        row: 0,
        col: 0,
        info: '',
    };
    $.ajax({
        url: '/get/seat_info/',
        type: 'post',
        dataType: 'JSON',
        data: {
            sid: $('select[name="sid"]').val()
        },
        async: false,
        success: function (res) {
            console.log(res);
            seat_layout.row = res.data.row;
            seat_layout.col = res.data.col;
            seat_layout.center_offset = res.data.center_offset;
            seat_layout.info = res.data.info;
            console.log(seat_layout)
        },
        error: function () {
            alert('获取座位信息失败');
        }

    })
    console.log(seat_layout);
    return seat_layout;
}

// 根据布局画图
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
            } else if (idx === '2') {
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

function update_seat() {
    $('select[name="sid"]').on("change", function () {
        draw();
        addEvent_update_status();
    });
}


/*
    更新信息并画图
 */
function draw() {
    $('.seats-wrapper').empty();
    $('.row-id-container').empty();
    // console.log(update_seat_info());
    init(update_seat_info());
}


function addEvent_update_status() {
    $('.row').off("click").on('click', '.seat', function () {
        if ($(this).hasClass('sold')) return;
        if ($(this).hasClass('empty')) return;
        let seat = $(this);
        // null -> sold -> empty
        let flag = $(this).hasClass('selected');
        if (!flag) {
            $(this).addClass('selected');
        } else {
            $(this).removeClass('selected');
        }
        update_seat_input();
    });
}



function update_seat_input() {
    seats = $('span[class="seat selected"]');
    seats_info = []
    console.log(seats.length)
    for (let i = 0; i < seats.length; i++) {
        seat = []
        row = seats.eq(i).attr('data-row-id');
        col = seats.eq(i).attr('data-column-id');
        seat.push("'" + row + "'");
        seat.push("'" + col + "'");
        str = '[' + String(seat) + ']'
        seats_info.push(str);
    }
    seats_info = '[' + String(seats_info) + ']'
    $('input[name="oseat"]').val(seats_info);
}