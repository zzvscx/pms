from django.conf.urls import url 
import views

urlpatterns = [
    url('^login/', views.login, name='login'),
    url('^logout/', views.logout, name='logout'),
    url('^detail/', views.user_detail, name='user_detail'),
    url('^points/',views.user_points, name='user_points'),
]
