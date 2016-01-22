from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^index', views.index, name='index'),
    url(r'^submit', views.submit, name='submit'),
    url(r'^next', views.next, name='next'),
    url(r'^prev', views.prev, name='prev'),
    url(r'^add_graph_edges', views.add_graph_edges, name='addGraphEdges'),
    url(r'^remove_graph_edges', views.remove_graph_edges, name='removeEdges'),
    url(r'^end_funciton', views.end_funciton, name='endActiveFuntion'),
    url(r'^stack_up', views.stack_up, name='stackUp'),
    url(r'^stack_down', views.stack_down, name='stackDown'),
    url(r'^go_to_line', views.go_to_line, name='goToLine'),
    url(r'^new_data', views.new_data, name='newData'),
    url(r'^render_graph', views.render_graph, name='renderGraph'),

]
