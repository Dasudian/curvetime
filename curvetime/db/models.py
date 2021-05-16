import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField


class Stocks(models.Model):
    code = models.CharField(max_length=20, null=True)   #股票代码
    name = models.CharField(max_length=40, null=True)   #股票名称
    pe = models.FloatField(null=True)   #市盈率
    capital = models.FloatField(null=True)  #市值
    class Meta:
        db_table = 'stockai_stocks'
        ordering = ['code']

class User(models.Model):
    username = models.CharField(max_length=20, null=True)
    password = models.CharField(max_length=40, null=True)
    class Meta:
        db_table = 'ct_user'


class StockPrice(models.Model):
    code = models.CharField(max_length=20, null=True)   #股票代码
    time = models.CharField(max_length=40, null=True)
    open = models.FloatField(null=True)
    close = models.FloatField(null=True)
    price = models.FloatField(null=True)
    high = models.FloatField(null=True)
    low = models.FloatField(null=True)
    ask = models.FloatField(null=True)
    bid = models.FloatField(null=True)
    volume = models.FloatField(null=True)
    amount = models.FloatField(null=True)
    ask_v1 = models.FloatField(null=True)
    ask1 = models.FloatField(null=True)
    ask_v2 = models.FloatField(null=True)
    ask2 = models.FloatField(null=True)
    ask_v3 = models.FloatField(null=True)
    ask3 = models.FloatField(null=True)
    ask_v4 = models.FloatField(null=True)
    ask4 = models.FloatField(null=True)
    ask_v5 = models.FloatField(null=True)
    ask5 = models.FloatField(null=True)
    bid_v1 = models.FloatField(null=True)
    bid1 = models.FloatField(null=True)
    bid_v2 = models.FloatField(null=True)
    bid2 = models.FloatField(null=True)
    bid_v3 = models.FloatField(null=True)
    bid3 = models.FloatField(null=True)
    bid_v4 = models.FloatField(null=True)
    bid4 = models.FloatField(null=True)
    bid_v5 = models.FloatField(null=True)
    bid5 = models.FloatField(null=True)
    class Meta:
        db_table = 'stockai_price'
        ordering = ['time', 'code']


class StockFeature(models.Model):
    time = models.CharField(max_length=40, null=True, unique=True)
    frame = models.JSONField(null=True)
    class Meta:
        db_table = 'stockai_feature'
        ordering = ['time']
