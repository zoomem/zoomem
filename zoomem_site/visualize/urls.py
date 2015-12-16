from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^submit', views.submit, name='submit'),
    url(r'^next', views.next, name='next'),
    url(r'^prev', views.prev, name='prev'),
    url(r'^first', views.first, name='first'),
    url(r'^go_to', views.go_to, name='go_to'),

]
