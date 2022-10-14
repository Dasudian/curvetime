from rest_framework import serializers
from curvetime.db.models import StockFeature, StockFeature2
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict
from django.db.models import Sum
from datetime import datetime
import json
from curvetime.env.stock_env import WINDOW_SIZE


class StockFeatureSerializer(serializers.ModelSerializer):
    frame = serializers.SerializerMethodField('get_frame')
    class Meta:
        model = StockFeature
        fields = ['frame']

    def get_frame(self, obj):
        frame = obj.frame
        return json.loads(frame)


class StockFeature2Serializer(serializers.ModelSerializer):
    frame = serializers.SerializerMethodField('get_frame')
    class Meta:
        model = StockFeature2
        fields = ['frame']

    def get_frame(self, obj):
        frame = obj.frame
        return json.loads(frame)



class DebtFeatureSerializer(serializers.ModelSerializer):
    frame = serializers.SerializerMethodField('get_frame')
    class Meta:
        model = DebtFeature
        fields = ['frame']

    def get_frame(self, obj):
        frame = obj.frame
        return json.loads(frame)


class Pagination(PageNumberPagination):
    page_size = WINDOW_SIZE
    page_size_query_param = 'row'
    page_query_param = "page"

    def get_paginated_response(self, data):
        return Response(
            {'code': 200, 'msg': 'ok', 'data': {'list': data, 'total': self.page.paginator.count}})
