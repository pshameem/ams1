
from django.urls import path,include
from . import views
from django.conf.urls import url
from django.conf import settings

urlpatterns = [
    url(r'^admin_panel/', include('admin_panel.urls')),
    url(r'^teacher_panel/', include('teacher_panel.urls')),
    url(r'^$', views.login),
    path('logout',views.logout)
]