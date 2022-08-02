# Author: wy
# Time: 2022/7/3 9:49

from django.db import models


class GetNowMovies(models.Model):
    mname = models.CharField(db_column='Mname', max_length=128, db_collation='utf8mb4_0900_ai_ci',
                             primary_key=True)  # Field name made lowercase.
    mtype = models.SmallIntegerField(db_column='Mtype')  # Field name made lowercase.
    minfo = models.CharField(db_column='Minfo', max_length=2000, db_collation='utf8mb4_0900_ai_ci', blank=True,
                             null=True)  # Field name made lowercase.
    mstar = models.CharField(db_column='Mstar', max_length=255,
                             db_collation='utf8mb4_0900_ai_ci')  # Field name made lowercase.
    mlength = models.IntegerField(db_column='Mlength')  # Field name made lowercase.
    mremark = models.DecimalField(db_column='Mremark', max_digits=10, decimal_places=1)  # Field name made lowercase.
    mimage = models.CharField(db_column='Mimage', max_length=255,
                              db_collation='utf8mb4_0900_ai_ci')  # Field name made lowercase.
    stime = models.DateTimeField(db_column='Stime')  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'get_now_movies'


class ShowInfo(models.Model):
    mid = models.BigIntegerField(db_column='Mid')  # Field name made lowercase.
    mname = models.CharField(db_column='Mname', max_length=128,
                             db_collation='utf8mb4_0900_ai_ci')  # Field name made lowercase.
    mtype = models.SmallIntegerField(db_column='Mtype')  # Field name made lowercase.
    minfo = models.CharField(db_column='Minfo', max_length=2000, db_collation='utf8mb4_0900_ai_ci', blank=True,
                             null=True)  # Field name made lowercase.
    mstar = models.CharField(db_column='Mstar', max_length=255,
                             db_collation='utf8mb4_0900_ai_ci')  # Field name made lowercase.
    mlength = models.IntegerField(db_column='Mlength')  # Field name made lowercase.
    mremark = models.DecimalField(db_column='Mremark', max_digits=10, decimal_places=1)  # Field name made lowercase.
    mimage = models.CharField(db_column='Mimage', max_length=255,
                              db_collation='utf8mb4_0900_ai_ci')  # Field name made lowercase.
    loc = models.CharField(max_length=128, db_collation='utf8mb4_0900_ai_ci')
    on_info = models.CharField(max_length=128, db_collation='utf8mb4_0900_ai_ci', blank=True, null=True)
    mison = models.SmallIntegerField(db_column='Mison')  # Field name made lowercase.
    sid = models.BigIntegerField(db_column='Sid', primary_key=True)  # Field name made lowercase.
    snum = models.IntegerField(db_column='Snum')  # Field name made lowercase.
    stime = models.DateTimeField(db_column='Stime')  # Field name made lowercase.
    sprice = models.DecimalField(db_column='Sprice', max_digits=10, decimal_places=2)  # Field name made lowercase.
    smax_sold_ticket = models.IntegerField(db_column='Smax_sold_ticket')  # Field name made lowercase.
    rid = models.BigIntegerField(db_column='Rid')  # Field name made lowercase.
    rname = models.CharField(db_column='Rname', max_length=50,
                             db_collation='utf8mb4_0900_ai_ci')  # Field name made lowercase.
    rsize = models.IntegerField(db_column='Rsize')  # Field name made lowercase.
    rinfo = models.CharField(db_column='Rinfo', max_length=255, db_collation='utf8mb4_0900_ai_ci', blank=True,
                             null=True)  # Field name made lowercase.
    r_col = models.IntegerField(db_column='R_col')  # Field name made lowercase.
    r_row = models.IntegerField(db_column='R_row')  # Field name made lowercase.
    rscreen_offset = models.IntegerField(db_column='Rscreen_offset')  # Field name made lowercase.
    rseat = models.CharField(db_column='Rseat', max_length=2048,
                             db_collation='utf8mb4_0900_ai_ci')  # Field name made lowercase.
    tid = models.BigIntegerField(db_column='Tid')  # Field name made lowercase.
    tlocation = models.CharField(db_column='Tlocation', max_length=255,
                                 db_collation='utf8mb4_0900_ai_ci')  # Field name made lowercase.
    tname = models.CharField(db_column='Tname', max_length=50,
                             db_collation='utf8mb4_0900_ai_ci')  # Field name made lowercase.
    ssold_info = models.CharField(db_column='Ssold_info', max_length=2048,
                                  db_collation='utf8mb4_0900_ai_ci')  # Field name made lowercase.
    sshow_status = models.SmallIntegerField(db_column='Sshow_status')  # Field name made lowercase.
    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'show_info'
