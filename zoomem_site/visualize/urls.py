from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^submit', views.submit, name='submit'),
    url(r'^next', views.next, name='next'),
    url(r'^prev', views.prev, name='prev'),
    url(r'^update', views.update, name='update'),
    url(r'^remove_graph_edges', views.remove_graph_edges, name='remove_graph_edges'),
    url(r'^end_funciton', views.end_funciton, name='end_funciton'),
    url(r'^stack_up', views.stack_up, name='stack_up'),
    url(r'^stack_down', views.stack_down, name='stack_down'),
]
