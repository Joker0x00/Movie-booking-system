import datetime
import decimal
import time
from myapp.utils.get_code import check_code

from django.shortcuts import render, redirect
from django import forms
from myapp import models
from myapp import view_models
from myapp.utils.bootstrap import BootstrapModelFrom
from myapp.utils.pageination import Pagination
from django.utils.safestring import mark_safe
from myapp.utils.encrypt import md5
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.db.models import Avg, Max, Min, Count, Sum


# Create your views here.


# class UserModelForm(BootstrapModelFrom):


class LoginForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True,
    )

    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True,
    )

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


class RegisterForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    password1 = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True,
    )

    password2 = forms.CharField(
        label='重复密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True,
    )

    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True,
    )

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


class AdminUserModelForm(BootstrapModelFrom):
    class Meta:
        model = models.Admin
        fields = ['aname', 'apwd','acreate']
        widgets = {
            'apwd': forms.PasswordInput(attrs={'class': 'form-control'}, render_value=True)  # 设置样式
        }

    def clean_apwd(self):
        return md5(self.cleaned_data.get('apwd'))


class AdminUserEditModelForm(BootstrapModelFrom):
    class Meta:
        model = models.Admin
        fields = ['aname', 'acreate']


class AdminTheaterModelForm(BootstrapModelFrom):
    class Meta:
        model = models.Theater
        fields = ['tid', 'tname', 'tlocation']


class AdminMovieModelForm(BootstrapModelFrom):
    bootstrap_exlude_fields = ['img']

    class Meta:
        model = models.Movie
        fields = '__all__'


class AdminRoomModelForm(BootstrapModelFrom):
    class Meta:
        model = models.Room
        fields = ['rname', 'rsize', 'rinfo', 'tid', 'r_row', 'r_col', 'rseat', 'rscreen_offset']


class AdminShowModelForm(BootstrapModelFrom):
    class Meta:
        model = models.Show
        fields = ['mid', 'rid', 'stime', 'sprice', 'smax_sold_ticket', 'ssold_info', 'sshow_status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [
            (1, '12'),
            (2, '13')
        ]


class AdminOrderModelForm(BootstrapModelFrom):
    class Meta:
        model = models.Order
        fields = ['uid', 'sid', 'oseat', 'ostatus']


class UserModelForm(BootstrapModelFrom):
    class Meta:
        model = models.User
        fields = '__all__'
        widgets = {
            'upassword': forms.PasswordInput(attrs={'class': 'form-control'}, render_value=True)  # 设置样式
        }

    def clean_upassword(self):
        return md5(self.cleaned_data.get('upassword'))


class UserEditModelForm(BootstrapModelFrom):
    class Meta:
        model = models.User
        fields = ['uname', 'usex', 'ubirthday', 'uemail', 'uaccount']


def index(request):
    on_movie = models.Movie.objects.filter(mstatus=2)
    upcoming_movie = models.Movie.objects.filter(mstatus=1)
    print(upcoming_movie)
    return render(request, 'index.html', {'now': on_movie, 'upcoming': upcoming_movie})


def user_info(request):
    uid = request.session.get('info')
    if not uid:
        return render(request, '404.html')
    uid = uid['id']
    user = models.User.objects.filter(uid=uid).first()
    if request.method == 'GET':
        form = UserEditModelForm(instance=user)
        return render(request, 'user_info.html', {"user": user, "form": form, 'id': uid})

    form1 = UserEditModelForm(data=request.POST, instance=user)
    if form1.is_valid():
        form1.save()
        return redirect('/user/info/')
    else:
        return render(request, 'user_info.html', {"form": form1, 'id': uid})


def movie_list(request):
    catId = request.GET.get('catid')
    sourceId = request.GET.get('sourceid')
    # types = ['爱情', '喜剧', '动画', '剧情', '恐怖', '科幻', '悬疑', '犯罪', '家庭', '青春', '奇幻', '战争']
    sources = ['', '大陆', '美国', '韩国', '日本', '香港', '台湾', '英国']
    movieList = models.Movie.objects.all()
    if catId:
        print("1")
        movieList = movieList.filter(mtype=int(catId))
    if sourceId:
        print("2")
        movieList = movieList.filter(**{'mloc__contains': sources[int(sourceId)]})
    print(movieList)

    return render(request, 'movies.html', {'movieList': movieList, 'c1': catId, 'c2': sourceId})


def admin_userList(request):
    data_dict = {}
    value = request.GET.get('q', "")
    info = request.GET.get('query_info', "")
    choice = 0
    if value:
        if info == 'create_id':
            data_dict = {'acreate': value}
            choice = 3
        elif info == 'name':
            data_dict = {'aname__contains': value}
            choice = 2
        else:
            data_dict = {'aid__contains': value}
            choice = 1
    res = models.Admin.objects.filter(**data_dict)

    queryset = res
    current_page = request.GET.get('page')
    all_count = queryset.count()

    page_obj = Pagination(current_page, all_count, value, info)
    page_data = queryset[page_obj.start:page_obj.end]
    html = page_obj.page_html()
    return render(request, 'admin_list.html', {"users": page_data, "q": value, "c": choice, "html": html})


def admin_addUsers(request):
    if request.method == 'GET':
        form = AdminUserModelForm()
        return render(request, 'admin_addAdmin.html', {"form": form})
    form = AdminUserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list')
    else:
        print(form.errors)
    return render(request, 'admin_addAdmin.html', {"form": form})


def admin_deleteUser(request, id):
    if models.Admin.objects.count() == 1:
        return redirect('/admin/list')
    else:
        models.Admin.objects.filter(aid=id).first().delete()
        return redirect('/admin/list')


def admin_editUser(request, id):
    admin = models.Admin.objects.filter(aid=id).first()
    print('fasdfasfd')
    if request.method == 'GET':
        form = AdminUserEditModelForm(instance=admin)
        return render(request, 'admin_editAdmin.html', {"admin": admin, "form": form, 'id': id})

    form1 = AdminUserEditModelForm(data=request.POST, instance=admin)
    if form1.is_valid():
        form1.save()
        return redirect('/admin/list')
    else:
        return render(request, 'admin_editAdmin.html', {"form": form1, 'id': id})


def admin_theaterList(request):
    data_dict = {}
    value = request.GET.get('q', "")
    info = request.GET.get('query_info', "")
    choice = 0
    if value:
        if info == 'name':
            data_dict = {'tname__contains': value}
            choice = 2
        elif info == 'location':
            data_dict = {'tlocation__contains': value}
            choice = 3
        else:
            data_dict = {'tid__contains': value}
            choice = 1

    res = models.Theater.objects.filter(**data_dict)

    queryset = res
    current_page = request.GET.get('page')
    all_count = queryset.count()

    page_obj = Pagination(current_page, all_count, value, info)
    page_data = queryset[page_obj.start:page_obj.end]
    html = page_obj.page_html()

    return render(request, 'admin_theaterList.html', {"objs": page_data, "q": value, "c": choice, "html": html})


def admin_addTheater(request):
    if request.method == 'GET':
        form = AdminTheaterModelForm()
        return render(request, 'admin_addTheater.html', {"form": form})
    form = AdminTheaterModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/theater/list')
    else:
        print(form.errors)
    return render(request, 'admin_addTheater.html', {"form": form})


def admin_deleteTheater(request, id):
    models.Theater.objects.filter(tid=id).first().delete()
    return redirect('/admin/theater/list')


def admin_editTheater(request, id):
    admin = models.Theater.objects.filter(tid=id).first()
    if request.method == 'GET':
        form = AdminTheaterModelForm(instance=admin)
        return render(request, 'admin_editTheater.html', {"admin": admin, "form": form})

    form1 = AdminTheaterModelForm(data=request.POST, instance=admin)
    if form1.is_valid():
        form1.save()
        return redirect('/admin/theater/list')
    else:
        return render(request, 'admin_editTheater.html', {"form": form1})


def admin_movieList(request):
    data_dict = {}
    value = request.GET.get('q', "")
    info = request.GET.get('query_info', "")
    choice = 0
    if value:
        if info == 'name':
            data_dict = {'mname__contains': value}
            choice = 2
        elif info == 'type':
            data_dict = {'mtype__contains': value}
            choice = 3
        elif info == 'star':
            data_dict = {'mstar__contains': value}
            choice = 4
        else:
            data_dict = {'mid__contains': value}
            choice = 1

    res = models.Movie.objects.filter(**data_dict)

    queryset = res
    current_page = request.GET.get('page')
    all_count = queryset.count()

    page_obj = Pagination(current_page, all_count, value, info)
    page_data = queryset[page_obj.start:page_obj.end]
    html = page_obj.page_html()

    return render(request, 'admin_movieList.html', {"objs": page_data, "q": value, "c": choice, "html": html})


def admin_addMovie(request):
    if request.method == 'GET':
        form = AdminMovieModelForm()
        return render(request, 'admin_addMovie.html', {"form": form})
    form = AdminMovieModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        print(form.cleaned_data)
        form.save()
        return redirect('/admin/movie/list')
    else:
        print(form.errors)
    return render(request, 'admin_addMovie.html', {"form": form})


def admin_deleteMovie(request, id):
    models.Movie.objects.filter(mid=id).first().delete()
    return redirect('/admin/movie/list')


def admin_editMovie(request, id):
    admin = models.Movie.objects.filter(mid=id).first()
    if request.method == 'GET':
        form = AdminMovieModelForm(instance=admin)
        return render(request, 'admin_editMovie.html', {"admin": admin, "form": form})

    form1 = AdminMovieModelForm(data=request.POST, instance=admin, files=request.FILES)
    if form1.is_valid():
        print(form1.cleaned_data)
        form1.save()
        return redirect('/admin/movie/list')
    else:
        return render(request, 'admin_editMovie.html', {"form": form1})


def admin_roomList(request):
    data_dict = {}
    value = request.GET.get('q', "")
    info = request.GET.get('query_info', "")
    choice = 0
    if value:
        if info == 'name':
            data_dict = {'rname__contains': value}
            choice = 2
        elif info == 'tname':
            tobjs = models.Theater.objects.filter(tname__contains=value)
            tid = []
            for tobj in tobjs:
                tid.append(tobj.tid)
            data_dict = {'tid__in': tid}
            choice = 3
        else:
            data_dict = {'rid__contains': value}
            choice = 1
    res = models.Room.objects.filter(**data_dict)
    queryset = res
    current_page = request.GET.get('page')
    all_count = queryset.count()

    page_obj = Pagination(current_page, all_count, value, info)
    page_data = queryset[page_obj.start:page_obj.end]
    html = page_obj.page_html()

    return render(request, 'admin_roomList.html', {"objs": page_data, "q": value, "c": choice, "html": html})


def admin_addRoom(request):
    if request.method == 'GET':
        form = AdminRoomModelForm()
        return render(request, 'admin_addRoom.html', {"form": form})
    form = AdminRoomModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/room/list')
    else:
        print(form.errors)
    return render(request, 'admin_addRoom.html', {"form": form})


def admin_deleteRoom(request, id):
    models.Room.objects.filter(rid=id).first().delete()
    return redirect('/admin/room/list')


def admin_editRoom(request, id):
    admin = models.Room.objects.filter(rid=id).first()
    if request.method == 'GET':
        form = AdminRoomModelForm(instance=admin)
        return render(request, 'admin_editRoom.html', {"admin": admin, "form": form})

    form1 = AdminRoomModelForm(data=request.POST, instance=admin)
    if form1.is_valid():
        form1.save()
        return redirect('/admin/room/list')
    else:
        return render(request, 'admin_editRoom.html', {"form": form1})


def admin_showList(request):
    data_dict = {}
    value = request.GET.get('q', "")
    info = request.GET.get('query_info', "")
    choice = 0
    if value:
        if info == 'name':
            data_dict = {'rname__contains': value}
            choice = 2
        elif info == 'tname':
            tobjs = models.Theater.objects.filter(tname__contains=value)
            tid = []
            for tobj in tobjs:
                tid.append(tobj.tid)
            data_dict = {'tid__in': tid}
            choice = 3
        else:
            data_dict = {'rid__contains': value}
            choice = 1
    res = models.Show.objects.filter(**data_dict)
    queryset = res
    current_page = request.GET.get('page')
    all_count = queryset.count()

    page_obj = Pagination(current_page, all_count, value, info)
    page_data = queryset[page_obj.start:page_obj.end]
    html = page_obj.page_html()

    return render(request, 'admin_showList.html', {"objs": page_data, "q": value, "c": choice, "html": html})


def admin_addShow(request):
    if request.method == 'GET':
        form = AdminShowModelForm()
        return render(request, 'admin_addShow.html', {"form": form})
    form = AdminShowModelForm(data=request.POST)
    if form.is_valid():
        if models.Movie.objects.filter(mid=form.cleaned_data.get('mid').mid).first().mstatus == 4:
            models.Movie.objects.filter(mid=form.cleaned_data.get('mid').mid).update(mstatus=2)
        form.save()
        return redirect('/admin/show/list')
    else:
        print(form.errors)
    return render(request, 'admin_addShow.html', {"form": form})


def admin_deleteShow(request, id):
    models.Show.objects.filter(sid=id).first().delete()
    return redirect('/admin/show/list')


def admin_editShow(request, id):
    admin = models.Show.objects.filter(sid=id).first()
    if request.method == 'GET':
        form = AdminShowModelForm(instance=admin)
        return render(request, 'admin_editShow.html', {"admin": admin, "form": form})

    form1 = AdminShowModelForm(data=request.POST, instance=admin)
    if form1.is_valid():
        form1.save()
        return redirect('/admin/show/list')
    else:
        return render(request, 'admin_editShow.html', {"form": form1})


def admin_orderList(request):
    data_dict = {}
    value = request.GET.get('q', "")
    info = request.GET.get('query_info', "")
    choice = 0
    if value:
        if info == 'name':
            data_dict = {'rname__contains': value}
            choice = 2
        elif info == 'tname':
            tobjs = models.Theater.objects.filter(tname__contains=value)
            tid = []
            for tobj in tobjs:
                tid.append(tobj.tid)
            data_dict = {'tid__in': tid}
            choice = 3
        else:
            data_dict = {'rid__contains': value}
            choice = 1
    res = models.Order.objects.filter(**data_dict)
    queryset = res
    current_page = request.GET.get('page')
    all_count = queryset.count()

    page_obj = Pagination(current_page, all_count, value, info)
    page_data = queryset[page_obj.start:page_obj.end]
    html = page_obj.page_html()

    return render(request, 'admin_orderList.html', {"objs": page_data, "q": value, "c": choice, "html": html})


def admin_addOrder(request):
    if request.method == 'GET':
        form = AdminOrderModelForm()
        return render(request, 'admin_addOrder.html', {'form': form})
    form = AdminOrderModelForm(data=request.POST)
    if form.is_valid():
        if check_order(form):
            print('fasdfasdfaasdf')
            form.save()
            return render(request, 'admin_orderList.html')
        else:
            print(form.errors)
            return render(request, 'admin_addOrder.html', {'form': form})
    else:
        print(form.errors)
        return render(request, 'admin_addOrder.html', {'form': form})


def admin_deleteOrder(request, oid):
    models.Order.objects.filter(oid=id).first().delete()
    return redirect('/admin/order/list')


def admin_editOrder(request, oid):
    admin = models.Order.objects.filter(oid=id).first()
    if request.method == 'GET':
        form = AdminOrderModelForm(instance=admin)
        return render(request, 'admin_editOrder.html', {"admin": admin, "form": form})

    form1 = AdminOrderModelForm(data=request.POST, instance=admin)
    if form1.is_valid():
        form1.save()
        return redirect('/admin/order/list')
    else:
        return render(request, 'admin_editOrder.html', {"form": form1})


def userList(request):
    data_dict = {}
    value = request.GET.get('q', "")
    info = request.GET.get('query_info', "")
    choice = 0
    if value:
        if info == 'name':
            data_dict = {'rname__contains': value}
            choice = 2
        elif info == 'tname':
            tobjs = models.Theater.objects.filter(tname__contains=value)
            tid = []
            for tobj in tobjs:
                tid.append(tobj.tid)
            data_dict = {'tid__in': tid}
            choice = 3
        else:
            data_dict = {'rid__contains': value}
            choice = 1
    res = models.User.objects.filter(**data_dict)
    queryset = res
    current_page = request.GET.get('page')
    all_count = queryset.count()

    page_obj = Pagination(current_page, all_count, value, info)
    page_data = queryset[page_obj.start:page_obj.end]
    html = page_obj.page_html()

    return render(request, 'admin_userList.html', {"objs": page_data, "q": value, "c": choice, "html": html})


def addUser(request):
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'admin_addUser.html', {"form": form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        form.save()
        return redirect('/admin/user/list')
    else:
        print(form.errors)
    return render(request, 'admin_addUser.html', {"form": form})


def deleteUser(request, id):
    models.User.objects.filter(uid=id).first().delete()
    return redirect('/admin/user/list')


def editUser(request, id):
    admin = models.User.objects.filter(uid=id).first()
    if request.method == 'GET':
        form = UserEditModelForm(instance=admin)
        return render(request, 'admin_editUser.html', {"admin": admin, "form": form, 'uid': id})

    form1 = UserEditModelForm(data=request.POST, instance=admin)
    if form1.is_valid():
        form1.save()
        return redirect('/admin/user/list')
    else:
        return render(request, 'admin_editUser.html', {"form": form1, 'uid': id})


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    form = LoginForm(data=request.POST)

    if form.is_valid():
        code = form.cleaned_data.pop('code')
        user_code = request.session.get('image_code', '')
        if code.upper() != user_code.upper():
            form.add_error('code', '验证码错误')
            return render(request, 'login.html', {'form': form})
        user_obj = models.User.objects.filter(uname=form.cleaned_data['username'],
                                              upassword=form.cleaned_data['password']).first()

        if not user_obj:

            form.add_error('password', '用户名或密码错误')
            print(form.errors)
            return render(request, 'login.html', {'form': form})
        else:
            request.session['info'] = {'id': str(user_obj.uid), 'name': user_obj.uname}
            request.session.set_expiry(60 * 60 * 24 * 7)
            return redirect('/index/')
    else:
        return render(request, 'login.html', {"form": form})


def logout(request):
    request.session['info'] = None
    return redirect('/index/')


def admin_login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'admin_login.html', {'form': form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        code = form.cleaned_data.pop('code')
        user_code = request.session.get('image_code', '')
        if code.upper() != user_code.upper():
            form.add_error('code', '验证码错误')
            return render(request, 'login.html', {'form': form})
        user_obj = models.Admin.objects.filter(aname=form.cleaned_data['username'],
                                               apwd=form.cleaned_data['password']).first()
        if not user_obj:
            form.add_error('password', '用户名或密码错误')
            return render(request, 'admin_login.html', {'form': form})
        else:
            request.session['admin'] = {'id': str(user_obj.aid), 'name': user_obj.aname}
            request.session.set_expiry(60 * 60 * 24 * 7)  # 7 天免密登录
            return redirect('/admin/list/')
    else:
        print(form.errors)
        return render(request, 'admin_login.html', {"form": form})


def admin_logout(request):
    request.session['admin'] = None
    return redirect('/admin/login/')


def get_movie(request):
    id = request.GET.get('id')
    if not id:
        return None
    movie = models.Movie.objects.filter(mid=id).first()

    return render(request, 'get_movie.html', {'movie': movie})


def confirm_order(request):
    uid = request.session['info']['id']
    ticket_data = request.GET
    tickets = ticket_data['tickets'].split(' ')
    new_tickets = []

    for ticket in tickets:
        new_tickets.append(ticket.split('-'))
    sid = int(ticket_data['sid'])
    user = models.User.objects.filter(uid=uid).first()
    show = models.Show.objects.filter(sid=sid).first();
    price = int(ticket_data['num']) * show.sprice
    return render(request, 'confirm_order.html',
                  {'user': user, 'show': show, 'total_price': price, 'tickets': new_tickets})


def add_order(request):
    if request.method == 'GET':
        return redirect('/index/')
    form = AdminOrderModelForm(data=request.POST)
    if form.is_valid():
        if check_order(form):
            form.save()
            return redirect('/user/order/')
        else:
            print(form.errors)
            return render(request, 'confirm_order.html', {'form': form})
    else:
        print(form.errors)
        return render(request, '404.html')


# 再次复核订单是否合法，如果合法则写入数据库
def check_order(form):
    oseat = form.cleaned_data['oseat']
    show = form.cleaned_data['sid']
    user = form.cleaned_data['uid']
    seat_info = show.ssold_info
    user_account = user.uaccount
    seat_list = eval(oseat)
    num = len(seat_list)
    total_price = num * show.sprice
    col = show.rid.r_col
    new_seatList = seat_info
    if total_price > user_account:
        form.add_error('uid', '余额不足，请充值')
        return False
    print(seat_info)
    for t in seat_list:
        idx = (int(t[0]) - 1) * col + (int(t[1]) - 1)
        print(idx)
        if seat_info[idx] == '2' or seat_info[idx] == '1':
            form.add_error('oseat', '选座冲突')
            return False
        else:
            new_seatList = new_seatList[:idx] + '1' + new_seatList[idx + 1:]
    showObj = models.Show.objects.filter(sid=show.sid).first()
    showObj.ssold_info = new_seatList
    showObj.snum += num
    showObj.save()
    user.uaccount -= total_price
    user.save()
    return True


def select_theater(request):
    data_dict = {}
    value = request.GET.get('q', "")
    info = request.GET.get('query_info', "")
    choice = 0
    data_dict = {}
    if value:
        if info == 'name':
            data_dict['tname__contains'] = value
            choice = 2
        elif info == 'location':
            data_dict['tlocation__contains'] = value
            choice = 3
        else:
            data_dict['tid__contains'] = value
            choice = 1
    mid = request.GET['mid']

    if mid:
        movie = models.Movie.objects.filter(mid=mid).first()
        data_dict['mid'] = mid
        data_dict['sshow_status'] = 0
        # res = view_models.ShowInfo.objects.filter(**data_dict).values('tname', 'tlocation').distinct().order_by('tname')
        res = view_models.ShowInfo.objects.filter(**data_dict).values('tname', 'tlocation', 'tid').annotate(
            min_price=Min('sprice'))
        return render(request, 'select_theater.html', {"movie": movie, "objs": res, "q": value, "c": choice})


def select_detail(request):
    data_dict = {}
    value = request.GET.get('q', "")
    info = request.GET.get('query_info', "")
    choice = 0
    data_dict = {}
    if value:
        if info == 'name':
            data_dict['tname__contains'] = value
            choice = 2
        elif info == 'location':
            data_dict['tlocation__contains'] = value
            choice = 3
        else:
            data_dict['tid__contains'] = value
            choice = 1
    tid = request.GET['tid']
    mid = request.GET['mid']

    if mid and tid:
        movie = models.Movie.objects.filter(mid=mid).first()
        theater = models.Theater.objects.filter(tid=tid).first()
        shows = view_models.ShowInfo.objects.filter(mid=mid, tid=tid)
        lists = []
        show_time_list = {}
        for show in shows:
            date = show.stime.date()
            lists.append(show.stime.strftime("%m-%d"))
        lists = set(lists)
        lists = list(lists)
        lists.sort()
        new_lists = []
        for d in lists:
            date = d.split('-')
            month = int(date[0])
            day = int(date[1])
            da = str(month) + '月' + str(day) + '日'
            new_lists.append(da)
        print(new_lists)
        for d in new_lists:
            tmp = []
            for show in shows:
                date = show.stime.date()
                if d == str(date.month) + '月' + str(date.day) + '日':
                    tmp.append(show)
            show_time_list[d] = tmp
        # if mid:
        #     movie = models.Movie.objects.filter(mid=mid).first()
        #     data_dict['mid'] = mid
        #     # res = view_models.ShowInfo.objects.filter(**data_dict).values('tname', 'tlocation').distinct().order_by('tname')
        #     res = view_models.ShowInfo.objects.filter(**data_dict).values('tname', 'tlocation').annotate(
        #         min_price=Min('sprice'))

        return render(request, 'select_detail.html',
                      {'time_list': new_lists, "shows": show_time_list, "movie": movie, "theater": theater, "q": value,
                       "c": choice})


def select_seat(request):
    sid = request.GET['sid']
    obj = view_models.ShowInfo.objects.filter(sid=sid).first()
    return render(request, 'select_seat.html', {'obj': obj})


@csrf_exempt
def get_seat_info(request):
    data = request.POST
    t = data.get('sid', '')
    if not t:
        print(1)
        req = request.POST
        rid = req['rid'].split('-')[0]
        room = models.Room.objects.filter(rid=rid).first()
        res = {
            'seat_info': room.rseat,
        }
        return JsonResponse(res)
    else:
        sid = data['sid']
        res = {}
        show = view_models.ShowInfo.objects.filter(sid=sid).first()
        res['info'] = show.ssold_info
        res['row'] = show.r_row
        res['col'] = show.r_col
        res['center_offset'] = show.rscreen_offset
        return JsonResponse({'data': res})


# @csrf_exempt
# def get_theaters(request):
#     theaters = models.Theater.objects.all()
#     res = []
#     for theater in theaters:
#         res.append(theater.tname)
#     return JsonResponse({'data': res})

@csrf_exempt
def get_theaters(request):
    """
    处理 ajax 请求
    根据条件获取电影院信息
    :param request:
    :return:
    """
    mid = request.POST.get('mid')
    print('get_theaters')
    r = []
    if not mid:
        theaters = models.Theater.objects.all()
        for theater in theaters:
            r.append(str(theater.tid) + '-' + theater.tname)
    else:
        theaters = view_models.ShowInfo.objects.filter(mid=mid).values('tid', 'tname').distinct()
        print(theaters)
        for theater in theaters:
            dict = {}
            dict['tid'] = theater['tid']
            dict['tname'] = theater['tname']
            r.append(dict)
        print(r)

    return JsonResponse({'data': r})


@csrf_exempt
def get_movies(request):
    r = []
    movies = models.Movie.objects.all()
    for movie in movies:
        dict = {}
        dict['mid'] = movie.mid
        dict['mname'] = movie.mname
        r.append(dict)
    return JsonResponse({'data': r})


@csrf_exempt
def get_room(request):
    """
    根据电影院选择放映厅
    或者根据电影和电影院选择放映厅
    :param request:
    :return:
    """
    theater = request.POST['theater']
    mid = request.POST.get('movie', '')
    r = []
    tid = theater.split('-')[0]
    filter_dict = {}
    filter_dict['tid'] = tid
    if mid:
        filter_dict['mid'] = mid
    rooms = view_models.ShowInfo.objects.filter(**filter_dict).values('rid', 'rname').distinct()
    for room in rooms:
        dict1 = {}
        dict1['rid'] = room['rid']
        dict1['rname'] = room['rname']
        r.append(dict1)
    print(r)
    return JsonResponse({'data': r})


def user_order(request):
    user_session = request.session.get('info')
    if not user_session:
        return render(request, '404.html')
    uid = user_session['id']
    orders = models.Order.objects.filter(uid=uid, ouser_show_status=1)
    return render(request, 'user_order.html', {'orders': orders})


@csrf_exempt
def cash_check(request):
    status = 'success'
    if (request.method == 'POST'):
        data = request.POST
        if data:
            print(data)
            uid = data['uid']
            sid = data['sid']
            print(sid)
            print(uid)
            oseat = data['oseat']
            seat_list = eval(oseat)
            num = len(seat_list)
            show = models.Show.objects.filter(sid=sid).first()
            user = models.User.objects.filter(uid=uid).first()
            total_price = num * show.sprice
            col = show.rid.r_col
            seat_info = show.ssold_info
            user_account = user.uaccount
            data = {}
            data['errors'] = []

            if total_price > user_account:
                data['errors'].append('余额不足，请充值')
                status = 'fail'
            for t in seat_list:
                idx = (int(t[0]) - 1) * col + (int(t[1]) - 1)
                if seat_info[idx] == '2' or seat_info[idx] == '1':
                    data['errors'].append('选座冲突，请刷新页面后重新选择')
                    status = 'fail'
                    break
            return JsonResponse({'status': status, 'errors': data})
        else:
            status = 'fail'
            return JsonResponse({'status': status, 'errors': ['请求数据为空']})
    else:
        status = 'fail'
        return JsonResponse({'status': status, 'errors': ['请求方式错误']})


@csrf_exempt
def get_time(request):
    theater = request.POST['theater']
    mid = request.POST['movie']
    rid = request.POST['room']
    tid = theater.split('-')[0]
    print(mid, rid, tid)
    r = []
    shows = view_models.ShowInfo.objects.filter(tid=tid, mid=mid, rid=rid).values('stime')
    for show in shows:
        r.append(show['stime'])
    print(shows)
    return JsonResponse({'data': r})


@csrf_exempt
def get_sid(request):
    theater = request.POST['theater']
    mid = request.POST['movie']
    rid = request.POST['room']
    tid = theater.split('-')[0]
    time = request.POST['time']
    r = []
    shows = view_models.ShowInfo.objects.filter(tid=tid, mid=mid, rid=rid, stime=time).values('sid')
    for show in shows:
        r.append(show['sid'])
    print(shows)
    return JsonResponse({'data': r})


def refund(request):
    data = request.GET
    if not data:
        return render(request, '404.html')
    oid = data['oid']
    order = models.Order.objects.filter(oid=oid).first()
    if not order:
        return render(request, 'invalid_option.html')
    if order.ostatus == 2 or order.ostatus == 3:  # 已完成或已退票 为非法操作
        return render(request, 'invalid_option.html')
    show = order.sid
    uid = order.uid.uid
    price = show.sprice
    sid = show.sid
    seat_str = show.ssold_info
    oseat = order.oseat
    seat_list = eval(oseat)
    col = show.rid.r_col
    new_seatList = ""
    num = len(seat_list)
    for t in seat_list:
        idx = (int(t[0]) - 1) * col + (int(t[1]) - 1)
        new_seatList = new_seatList[:idx] + '0' + new_seatList[idx + 1:]
    new_user = models.User.objects.filter(uid=uid).first()
    new_show = models.Show.objects.filter(sid=sid).first()

    new_show.snum -= 1
    new_show.ssold_info = new_seatList
    new_user.uaccount += show.sprice * num

    order.ostatus = 3

    new_show.save()
    new_user.save()
    order.save()
    if data['user'] == '1':
        return redirect('/user/order/')
    else:
        return redirect('/admin/order/list/')


"""
    支持删除订单记录
    如果订单状态为未完成，则支持删除前退票
"""


def delete_order(request):
    data = request.GET
    if not data:
        return render(request, '404.html')
    oid = data['oid']
    order = models.Order.objects.filter(oid=oid).first()
    if not order:
        return render(request, 'invalid_option.html')
    if order.ostatus == 1:
        show = order.sid
        uid = order.uid.uid
        price = show.sprice
        sid = show.sid
        seat_str = show.ssold_info
        oseat = order.oseat
        seat_list = eval(oseat)
        col = show.rid.r_col
        new_seatList = ""
        num = len(seat_list)
        for t in seat_list:
            idx = (int(t[0]) - 1) * col + (int(t[1]) - 1)
            new_seatList = new_seatList[:idx] + '0' + new_seatList[idx + 1:]
        new_user = models.User.objects.filter(uid=uid).first()
        new_show = models.Show.objects.filter(sid=sid).first()

        new_show.snum -= 1
        new_show.ssold_info = new_seatList
        new_user.uaccount += show.sprice * num

        order.ostatus = 3

        new_show.save()
        new_user.save()
    order.delete()
    return redirect('/admin/order/list/')


def order_hide(request):
    data = request.GET
    if not data:
        return render(request, 'invalid_option.html')
    oid = data['oid']
    order = models.Order.objects.filter(oid=oid).first()
    if not order:
        return render(request, 'invalid_option.html')
    order.ouser_show_status = 0
    order.save()
    return redirect('/user/order/')


@csrf_exempt
def user_recharge(request):
    data = request.POST
    if data:
        uid = data['uid']
        user = models.User.objects.filter(uid=uid).first()
        if user and data['recharge_num']:
            user.uaccount += decimal.Decimal(data['recharge_num']).quantize(decimal.Decimal("0.00"))
            print(user.uaccount)
            print('fdsafadsfas')
            user.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'})


def get_code(request):
    """
    获得图片验证码
    :param request:
    :return:
    """
    from io import BytesIO
    # 生成图片验证码
    img, code_string = check_code()
    # 将字符串写入当前请求登录的用户session中
    request.session['image_code'] = code_string
    # 给session设置60s有效期
    request.session.set_expiry(60)
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def user_register(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'user_register.html', {'form': form})
    form = RegisterForm(data=request.POST)

    if form.is_valid():
        code = form.cleaned_data.pop('code')
        user_code = request.session.get('image_code', '')
        pwd1 = form.cleaned_data.get('password1', '')
        pwd2 = form.cleaned_data.get('password2', '')
        if pwd1 != pwd2:
            form.add_error('password2', '两次密码输入不一致')
            return render(request, 'user_register.html', {'form': form})
        if code.upper() != user_code.upper():
            form.add_error('code', '验证码错误')
            return render(request, 'user_register.html', {'form': form})
        user_obj = models.User.objects.filter(uname=form.cleaned_data['username']).first()
        # 用户名不存在，可以注册
        if not user_obj:
            # 注册成功
            models.User.objects.create(uname=form.cleaned_data['username'],
                                       upassword=md5(form.cleaned_data['password1']))
            # 保存session
            user = models.User.objects.filter(uname=form.cleaned_data['username']).first()
            request.session['info'] = {'id': user.uid, 'name': user.uname}
            request.session.set_expiry(60 * 60 * 1)
            # 自动登录并跳转到首页
            return redirect('/index/')
        else:
            # 用户名已存在 反馈报错信息
            form.add_error('username', '该用户名已存在')
            return render(request, 'user_register.html', {"form": form})
    else:
        return render(request, 'user_register.html', {"form": form})


@csrf_exempt
def change_pwd(request):
    data = request.POST
    status = 'success'
    if data:
        id = data.get('uid', '')
        pwd = data.get('pwd', '')
        if id and pwd:
            user = models.User.objects.filter(uid=id).first()
            user.upassword = md5(pwd)
            user.save()
        else:
            status = 'fail'
    else:
        status = 'fail'
    return JsonResponse({'status': status})


@csrf_exempt
def change_admin_pwd(request):
    data = request.POST
    status = 'success'

    if data:
        id = data['id']
        pwd = data['pwd']
        if id and pwd:
            user = models.Admin.objects.filter(aid=id).first()
            user.apwd = md5(pwd)
            user.save()
        else:
            status = 'fail'
    else:
        status = 'fail'
    return JsonResponse({'status': status})
