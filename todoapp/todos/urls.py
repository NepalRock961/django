from django.conf.urls import url
from todos import views, views_api



urlpatterns = [
	url(r'^$',views.index, name ='index'),
	url(r'^create$', views.create, name='create'),
	url(r'^contact$', views.contact, name='contact'),
	url(r'^about$', views.about, name='about'),
	url(r'^save$', views.save, name='save'),
	url(r'^edit/todos/(\d+)/$', views.edit, name='edit'),
	url(r'^api/todos/(\d+)$', views_api.update, name='api_update_todo'),
	url(r'^remove/todos/(\d+)$',views.remove, name='remove'),
	
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^submit$', views.submit, name='submit'),
   url(r'^signup$',views.signup, name='signup'),
	url(r'^submission$',views.submission, name='submission'),

]

