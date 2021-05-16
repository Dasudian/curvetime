from django.urls import path

from curvetime.api import views

urlpatterns = [
        path('transaction', views.Transaction.as_view()),
        ]
