"""Cinema URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from myapp import views
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media', ),

    path('movies/detail/', views.get_movie),

    path('check/order/', views.cash_check),

    path('get/seat_info/', views.get_seat_info),
    path('get/theaters/', views.get_theaters),
    path('get/room/', views.get_room),
    path('get/movies/', views.get_movies),
    path('get/time/',views.get_time),
    path('get/sid/', views.get_sid),
    path('get/seat_info', views.get_seat_info),

    path('image/code/', views.get_code),


    path('order/add/', views.add_order),
    path('order/confirm/', views.confirm_order),
    path('order/hide/', views.order_hide),

    path('select/theater/', views.select_theater),
    path('select/detail/', views.select_detail),
    path('select/seat/', views.select_seat),
    path('login/', views.login),
    path('logout/', views.logout),

    path('admin/login/', views.admin_login),
    path('admin/logout/', views.admin_logout),

    path('index/', views.index),
    path('user/info/', views.user_info),
    path('user/order/', views.user_order),
    path('movies/', views.movie_list),
    path('user/recharge/', views.user_recharge),
    path('user/register/', views.user_register),
    path('user/change/pwd/', views.change_pwd),

    # 用户表

    path('admin/user/list/', views.userList),
    path('admin/user/add/', views.addUser),
    path('admin/user/<int:id>/delete/', views.deleteUser),
    path('admin/user/<int:id>/edit/', views.editUser),
    path('admin/change/pwd/', views.change_admin_pwd),

    # 管理员

    path('admin/list/', views.admin_userList),
    path('admin/add/', views.admin_addUsers),
    path('admin/<int:id>/delete/', views.admin_deleteUser),
    path('admin/<int:id>/edit/', views.admin_editUser),

    # 电影管理

    path('admin/movie/list/', views.admin_movieList),
    path('admin/movie/add/', views.admin_addMovie),
    path('admin/movie/<int:id>/delete/', views.admin_deleteMovie),
    path('admin/movie/<int:id>/edit/', views.admin_editMovie),

    # 电影院管理

    path('admin/theater/list/', views.admin_theaterList),
    path('admin/theater/add/', views.admin_addTheater),
    path('admin/theater/<int:id>/delete/', views.admin_deleteTheater),
    path('admin/theater/<int:id>/edit/', views.admin_editTheater),

    # 放映厅管理

    path('admin/room/list/', views.admin_roomList),
    path('admin/room/add/', views.admin_addRoom),
    path('admin/room/<int:id>/delete/', views.admin_deleteRoom),
    path('admin/room/<int:id>/edit/', views.admin_editRoom),

    # 放映管理

    path('admin/show/list/', views.admin_showList),
    path('admin/show/add/', views.admin_addShow),
    path('admin/show/<int:id>/delete/', views.admin_deleteShow),
    path('admin/show/<int:id>/edit/', views.admin_editShow),

    # 订单管理

    path('admin/order/list/', views.admin_orderList),
    path('admin/order/add/', views.admin_addOrder),
    path('admin/order/<int:id>/delete/', views.admin_deleteOrder),
    path('admin/order/<int:id>/edit/', views.admin_editOrder),

    # 用户订单处理
    path('order/refund/', views.refund),
    path('order/delete/', views.delete_order)
    # 会员信息
]
