$(function () {
            addEvent_input();
            get_theater();
            addEvent_select_theater();
        });

        function get_theater() {
            $.ajax({
                url: '/get/theaters/',
                type: 'post',
                dataType: 'JSON',
                success: function (res) {
                    sel = $('select[name="theater"]')
                    sel.append('<option value="" selected="">---------</option>');
                    cnt = res['data'].length;
                    for (let i = 0; i < cnt; i++) {
                        sel.append('<option value="' + res['data'][i] + '">' + res['data'][i] + '</option>');
                    }
                },
                error: function (res) {
                    console.log(res)
                }
            })
        } // 获取所有的电影院信息

        function addEvent_select_theater() {
            $('select[name="theater"]').on("change", function () {
                $.ajax({
                    url: '/get/room/',
                    type: 'post',
                    dataType: 'JSON',
                    data: {
                        theater: $(this).val(),
                    },
                    success: function (res) {
                        sel = $('select[name="rid"]');
                        sel.empty();
                        sel.append('<option value="" selected="">---------</option>');
                        cnt = res['data'].length;
                        for (let i = 0; i < cnt; i++) {
                            sel.append('<option value="' + res['data'][i]['rid'] + '" >' + res['data'][i]['rid'] + ' - ' + res['data'][i]['rname'] + '</option>');
                        }
                    },
                });
            });
        } // 根据影院数据填充放映厅

        function addEvent_input() {
            $('select[name="rid"]').on("change", function () {
                $.ajax({
                    url: '/get/seat_info/',
                    type: 'post',
                    dataType: 'JSON',
                    data: {
                        rid: $(this).val(),
                    },
                    success: function (res) {
                        $('input[name="ssold_info"]').val(res['seat_info']);
                    },
                });
            });
        } // 根据选择的放映厅更新座位信息