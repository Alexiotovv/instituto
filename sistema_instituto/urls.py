from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from auth_app import views as auth_views_custom

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views_custom.home, name='home'),
    path('login/', auth_views_custom.custom_login, name='login'),
    path('logout/', auth_views_custom.custom_logout, name='logout'),
    path('dashboard/', auth_views_custom.dashboard, name='dashboard'),
    path('register/', auth_views_custom.register, name='register'),
    path('cursos/', include('cursos.urls')),

]
