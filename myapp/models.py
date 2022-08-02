from django.db import models


class Admin(models.Model):
    aid = models.BigAutoField(verbose_name='ID', db_column='Aid', primary_key=True,
                              auto_created=True)  # Field name made lowercase.
    aname = models.CharField(verbose_name='管理员用户名', db_column='Aname', max_length=255)  # Field name made lowercase.
    apwd = models.CharField(verbose_name='管理员密码', db_column='Apwd', max_length=255)  # Field name made lowercase.
    acreate = models.ForeignKey('self', models.SET_NULL, verbose_name='创建者ID', db_column='Acreate_id', default='1',
                                blank=True, null=True)  # Field name made lowercase.
    acreate_time = models.DateTimeField(verbose_name='创建时间', db_column='Acreate_time',
                                        auto_now=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'admin'

    def __str__(self):
        return self.aname


class Movie(models.Model):
    mid = models.BigAutoField(verbose_name='ID', db_column='Mid', primary_key=True)  # Field name made lowercase.
    mname = models.CharField(verbose_name='名称', db_column='Mname', max_length=128)  # Field name made lowercase.
    type_choices = [
        (1, '喜剧'),
        (2, '爱情'),
        (3, '动作'),
        (4, '枪战'),
        (5, '犯罪'),
        (6, '悬疑'),
        (7, '家庭'),
        (8, '科幻'),
        (9, '战争'),
        (10, '青春'),
        (11, '动画'),
    ]

    mtype = models.SmallIntegerField(verbose_name='类型', db_column='Mtype',
                                     choices=type_choices)  # Field name made lowercase.
    minfo = models.CharField(verbose_name='简介', db_column='Minfo', max_length=2000, blank=True,
                             null=True)  # Field name made lowercase.
    mstar = models.CharField(verbose_name='主演', db_column='Mstar', max_length=255)  # Field name made lowercase.
    mlength = models.IntegerField(verbose_name='时长', db_column='Mlength')  # Field name made lowercase.
    mremark = models.DecimalField(verbose_name='评分', db_column='Mremark', max_digits=10,
                                  decimal_places=1)  # Field name made lowercase.
    mimg = models.FileField(verbose_name='图片预览', db_column='Mimage', upload_to='img/', max_length=255)
    status = (
        (1, '即将上映'),
        (2, '正在上映'),
        (3, '已下档'),
        (4, '未设置'),
    )
    mstatus = models.SmallIntegerField(verbose_name='电影状态', db_column='Mison', choices=status, default=1)
    mloc = models.CharField(verbose_name='地区', db_column='loc', max_length=128, default='中国大陆', blank=True)
    mon_info = models.CharField(verbose_name='上映信息', db_column='on_info', max_length=128, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'movie'

    def __str__(self):
        return str(self.mid) + " : " + self.mname


class Order(models.Model):
    oid = models.BigAutoField(verbose_name='ID', db_column='Oid', primary_key=True)  # Field name made lowercase.
    uid = models.ForeignKey('User', models.CASCADE, verbose_name='用户ID', db_column='Uid')  # Field name made lowercase.
    sid = models.ForeignKey('Show', models.CASCADE, verbose_name='放映ID', db_column='Sid')  # Field name made lowercase.
    oseat = models.CharField(verbose_name='座位号', db_column='Oseat', max_length=127)  # Field name made lowercase.
    ocreate_time = models.DateTimeField(verbose_name='创建时间', db_column='Ocreate_time',
                                        auto_now=True)  # Field name made lowercase.
    status = (
        (1, '未完成'),
        (2, '已完成'),
        (3, '已退票')
    )
    ostatus = models.SmallIntegerField(verbose_name='订单状态', db_column='Ostatus', choices=status, default=1)
    show_status = (
        (0, '不显示'),
        (1, '显示')
    )
    ouser_show_status = models.SmallIntegerField(verbose_name='订单是否在用户界面显示', db_column='Ouser_show_status',
                                                 choices=show_status, default=1)

    class Meta:
        managed = True
        db_table = 'order'


class Room(models.Model):
    rid = models.BigAutoField(verbose_name='放映厅ID', db_column='Rid', primary_key=True)  # Field name made lowercase.
    rname = models.CharField(verbose_name='名称', db_column='Rname', max_length=50)  # Field name made lowercase.
    rsize = models.IntegerField(verbose_name='容纳人数', db_column='Rsize', default=0)  # Field name made lowercase.
    rinfo = models.CharField(verbose_name='信息', db_column='Rinfo', max_length=255, blank=True, null=True,
                             default=" ")  # Field name made lowercase.
    tid = models.ForeignKey('Theater', models.CASCADE, verbose_name='所属影院',
                            db_column='Tid')  # Field name made lowercase.
    rseat = models.CharField(verbose_name='座位信息', db_column='Rseat', max_length=2048, default="0");
    rscreen_offset = models.IntegerField(verbose_name='银幕偏移量', db_column='Rscreen_offset', default=0);
    r_row = models.IntegerField(verbose_name='行', db_column='R_row', default=0);
    r_col = models.IntegerField(verbose_name='列', db_column='R_col', default=0);

    class Meta:
        managed = True
        db_table = 'room'

    def __str__(self):
        return str(self.rid) + " : " + self.rname


class Show(models.Model):
    sid = models.BigAutoField(verbose_name='ID', db_column='Sid', primary_key=True)  # Field name made lowercase.
    mid = models.ForeignKey(Movie, models.CASCADE, verbose_name='电影选择', db_column='Mid')  # Field name made lowercase.
    rid = models.ForeignKey(Room, models.CASCADE, verbose_name='放映厅选择', db_column='Rid')  # Field name made lowercase.
    snum = models.IntegerField(verbose_name='购票人数', db_column='Snum', default=0)  # Field name made lowercase.
    stime = models.DateTimeField(verbose_name='放映时间', db_column='Stime')  # Field name made lowercase.
    sprice = models.DecimalField(verbose_name='票价', db_column='Sprice', max_digits=10,
                                 decimal_places=2)  # Field name made lowercase.
    smax_sold_ticket = models.IntegerField(verbose_name='每次最大购买票数', db_column='Smax_sold_ticket', default=0);
    ssold_info = models.CharField(verbose_name='售票信息', db_column='Ssold_info', max_length=2048, default='0')
    show_status_choices = (
        (0, '即将开始'),
        (1, '已结束'),
        (2, '已取消')
    )
    sshow_status = models.SmallIntegerField(verbose_name='放映状态', db_column='Sshow_status', choices=show_status_choices,
                                            default=0)

    class Meta:
        managed = True
        db_table = 'show'

    def __str__(self):
        return self.mid.mname + " - " + self.rid.rname


class Theater(models.Model):
    tid = models.BigAutoField(verbose_name='ID', db_column='Tid', primary_key=True)  # Field name made lowercase.
    tname = models.CharField(verbose_name='名称', db_column='Tname', max_length=50,
                             unique=True)  # Field name made lowercase.
    tlocation = models.CharField(verbose_name='地理位置', db_column='Tlocation',
                                 max_length=255)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'theater'

    def __str__(self):
        return self.tname


class User(models.Model):
    sex = (
        (1, '男'),
        (2, '女')
    )

    uid = models.BigAutoField(verbose_name='ID', db_column='Uid', primary_key=True)  # Field name made lowercase.
    uname = models.CharField(verbose_name='用户名', db_column='Uname', max_length=255, unique=True)  # Field name made lowercase.
    upassword = models.CharField(verbose_name='密码', db_column='Upassword', max_length=255)  # Field name made lowercase.
    usex = models.SmallIntegerField(verbose_name='性别', db_column='Usex', choices=sex, blank=True,
                                    null=True)  # Field name made lowercase.
    ubirthday = models.DateField(verbose_name='生日', db_column='Ubirthday', blank=True,
                                 null=True)  # Field name made lowercase.
    uemail = models.CharField(verbose_name='邮箱', db_column='Uemail', max_length=255, blank=True,
                              null=True)  # Field name made lowercase.
    uaccount = models.DecimalField(verbose_name='余额', db_column='Uaccount', max_digits=10, decimal_places=2,
                                   default=0.00)

    class Meta:
        managed = True
        db_table = 'user'

    def __str__(self):
        return str(self.uid) + " - " + self.uname
