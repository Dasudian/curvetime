# -*- coding: utf-8 -*-
import jwt, json
from django.conf import settings
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django_redis import get_redis_connection
from rest_framework import status
from curvetime.utils import ecode


class JwtTokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        return

    def process_response(self, request, response):
        return response


class RedisMiddleware(MiddlewareMixin):
    def process_request(self, request):
        return

    def process_response(self, request, response):
        return response


class DataAPIMiddleware(MiddlewareMixin):
    def process_request(self, request):
        return

    def process_response(self, request, response):
        return response
