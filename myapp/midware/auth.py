# Author: wy
# Time: 2022/7/2 18:03


from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class dlyz(MiddlewareMixin):
    def process_request(self, request):
        url = str(request.path_info)
        if url == "/":
            return redirect('/index/')
        if url.startswith('/media/'):
            return
        no_login_url = [
            '/image/code/',
            '/login/',
            '/index/',
            '/admin/login/',
            '/user/register/',
        ]

        if request.path_info in no_login_url:
            return

        admin_url = [
            '/admin/list/',
            '/admin/add/',
            '/admin/<int:id>/delete/',
            '/admin/<int:id>/edit/',
            '/admin/user/list/',
            '/admin/user/add/',
            '/admin/user/<int:id>/delete/',
            '/admin/user/<int:id>/edit/',
            '/admin/movie/list/',
            '/admin/movie/add/',
            '/admin/movie/<int:id>/delete/',
            '/admin/movie/<int:id>/edit/',
            '/admin/theater/list/',
            '/admin/theater/add/',
            '/admin/theater/<int:id>/delete/',
            '/admin/theater/<int:id>/edit/',
            '/admin/room/list/',
            '/admin/room/add/',
            '/admin/room/<int:id>/delete/',
            '/admin/room/<int:id>/edit/',
            '/admin/show/list/',
            '/admin/show/add/',
            '/admin/show/<int:id>/delete/',
            '/admin/show/<int:id>/edit/',
            '/admin/order/list/',
            '/admin/order/add/',
            '/admin/order/<int:id>/delete/',
            '/admin/order/<int:id>/edit/',
        ]

        user_session = request.session.get("info")
        admin_session = request.session.get("admin")
        if user_session:
            if admin_session:
                return
            else:
                if url.startswith('/admin/'):
                    return redirect('/admin/login/')
                else:
                    return
        else:
            if admin_session:
                if url.startswith('/admin/'):
                    print(1)
                    return
                else:
                    print('2')
                    return redirect('/login/')
            else:
                if url.startswith('/admin/'):
                    return redirect('/admin/login/')
                else:
                    return redirect('/login/')