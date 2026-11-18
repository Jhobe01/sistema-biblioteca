from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('ingresar/', auth_views.LoginView.as_view(), name='login'),
    path('salir/', auth_views.LogoutView.as_view(), name='logout'),
    path('prestamos/', include('prestamos.urls')),
    path('libros/', include('libros.urls')),
]

admin.site.site_header = 'Biblioteca | Panel de administración'
admin.site.site_title = 'Biblioteca'
admin.site.index_title = 'Gestión del sistema bibliotecario'
