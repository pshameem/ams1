
from django.urls import path,include
from . import views
from django.conf.urls import url
app_name = "teacher_panel"
urlpatterns = [
    path('', views.index),
    path('add/student',views.add_student),
    path('manage/student',views.manage_student),
    path('snap',views.snap),
    path('attendence',views.attendence_today),
    url(r'^get_subjects_for_teacher/$', views.get_subjects_for_teacher,name="get_subjects_for_teacher"),
    path('attendence/change/status',views.change_attendence,name="today_attendence")
]
