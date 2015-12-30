from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^submit', views.submit, name='submit'),
    url(r'^next', views.next, name='next'),
    url(r'^prev', views.prev, name='prev'),
    url(r'^update', views.update, name='update'),
    url(r'^removeGraphEdges', views.removeGraphEdges, name='removeGraphEdges'),
    url(r'^finishFuncton', views.finishFuncton, name='finishFuncton'),

]
