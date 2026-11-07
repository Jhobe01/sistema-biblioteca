from django.contrib import admin
from django.urls import path
urlpatterns = [path('admin/', admin.site.urls)]
admin.site.site_header = 'Biblioteca | Panel de administración'
admin.site.site_title = 'Biblioteca'
admin.site.index_title = 'Gestión del sistema bibliotecario'
