from django.urls import path
from . import views


app_name = 'list'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/detail', views.Detail.as_view(), name='detail')
]