from django.conf.urls import url 
import views

urlpatterns = [
    url('^login/',views.login,name='name'),
]
