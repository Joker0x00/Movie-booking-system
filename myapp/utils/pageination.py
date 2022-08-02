# # Author: wy
# # Time: 2022/7/1 8:23
#
# class Pagination(object):
#
#     def __init__(self, request, query_set, page_size, page_param="page"):
#         page = request.GET.get(page_param, "1")
#         if page.isdecimal():
#             page = int(page)
#         else:
#             page = 1
#         self.page = page
#         self.page_size = page_size
#         self.start = (page - 1) * page_size
#         self.end = page * page_size
#         self.page_querySet = query_set[self.start:self.end]
#
#
#
from django.utils.safestring import mark_safe

class Pagination(object):
    def __init__(self, current_page, all_count, q="", query_info="", per_page_num=10, pager_count=9):
        """
        封装分页相关数据
        :param current_page: 当前页
        :param all_count:    数据库中的数据总条数
        :param per_page_num: 每页显示的数据条数
        :param pager_count:  最多显示的页码个数

        用法:
        queryset = model.objects.all()
        page_obj = Pagination(current_page,all_count)
        page_data = queryset[page_obj.start:page_obj.end]
        获取数据用page_data而不再使用原始的queryset
        获取前端分页样式用page_obj.page_html
        """

        self.q = q
        self.query_info = query_info
        try:
            current_page = int(current_page)
        except Exception as e:
            current_page = 1

        if current_page < 1:
            current_page = 1

        self.current_page = current_page

        self.all_count = all_count
        self.per_page_num = per_page_num

        # 总页码
        all_pager, tmp = divmod(all_count, per_page_num)
        if tmp:
            all_pager += 1
        self.all_pager = all_pager

        self.pager_count = pager_count
        self.pager_count_half = int((pager_count - 1) / 2)

    @property
    def start(self):
        return (self.current_page - 1) * self.per_page_num

    @property
    def end(self):
        return self.current_page * self.per_page_num

    def page_html(self):
        print(self.q + " " + self.query_info)
        # 如果总页码 < 11个：
        if self.all_pager <= self.pager_count:
            pager_start = 1
            pager_end = self.all_pager + 1
        # 总页码  > 11
        else:
            # 当前页如果<=页面上最多显示11/2个页码
            if self.current_page <= self.pager_count_half:
                pager_start = 1
                pager_end = self.pager_count + 1

            # 当前页大于5
            else:
                # 页码翻到最后
                if (self.current_page + self.pager_count_half) > self.all_pager:
                    pager_end = self.all_pager + 1
                    pager_start = self.all_pager - self.pager_count + 1
                else:
                    pager_start = self.current_page - self.pager_count_half
                    pager_end = self.current_page + self.pager_count_half + 1

        page_html_list = []
        # 添加前面的nav和ul标签
        page_html_list.append('''
                    <nav aria-label='Page navigation >'
                    <ul class='pagination'>
                ''')
        first_page = '<li><a href="?q=%s&query_info=%s&page=%s">首页</a></li>' % (self.q, self.query_info, 1)
        page_html_list.append(first_page)

        if self.current_page <= 1:
            prev_page = '<li class="disabled"><a href="#">上一页</a></li>'
        else:
            prev_page = '<li><a href="?q=%s&query_info=%s&page=%s">上一页</a></li>' % (self.q, self.query_info, self.current_page - 1,)

        page_html_list.append(prev_page)

        for i in range(pager_start, pager_end):
            if i == self.current_page:
                temp = '<li class="active"><a href="?q=%s&query_info=%s&page=%s">%s</a></li>' % (self.q, self.query_info, i, i,)
            else:
                temp = '<li><a href="?q=%s&query_info=%s&page=%s">%s</a></li>' % (self.q, self.query_info, i, i,)
            page_html_list.append(temp)

        if self.current_page >= self.all_pager:
            next_page = '<li class="disabled"><a href="#">下一页</a></li>'
        else:
            next_page = '<li><a href="?q=%s&query_info=%s&page=%s">下一页</a></li>' % (self.q, self.query_info, self.current_page + 1,)
        page_html_list.append(next_page)

        last_page = '<li><a href="?q=%s&query_info=%s&page=%s">尾页</a></li>' % (self.q, self.query_info, self.all_pager,)
        page_html_list.append(last_page)
        search_field = """
                        <div class="text-center">
            <form method="get" action="" class="navbar-form">
                <div style="display: inline">
                    <input type="text" class="form-control" placeholder="页码" name="page">
                </div>
                <button type="submit" class="btn btn-default" style="display: inline">
                    跳转
                </button>
            </form>
        </div>
                        """
        page_html_list.append(search_field)

        # 尾部添加标签
        page_html_list.append('''
                                           </nav>
                                           </ul>
                                       ''')
        return mark_safe(''.join(page_html_list))
