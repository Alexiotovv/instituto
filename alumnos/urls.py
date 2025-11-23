from django.urls import path
from . import views

app_name = 'alumnos'

urlpatterns = [
    path('', views.lista_alumnos, name='lista_alumnos'),
    path('nuevo/', views.nuevo_alumno, name='nuevo_alumno'),
    path('<int:alumno_id>/', views.detalle_alumno, name='detalle_alumno'),
    path('<int:alumno_id>/editar/', views.editar_alumno, name='editar_alumno'),
    path('<int:alumno_id>/eliminar/', views.eliminar_alumno, name='eliminar_alumno'),
    path('buscar/', views.buscar_alumnos, name='buscar_alumnos'),
]