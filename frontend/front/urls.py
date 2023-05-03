
from django.contrib import admin
from django.urls import path
from .views import view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', view.index , name="index"),
    path('hello/', view.hello, name="hello"),
    path('servicios/', view.servicios, name="servicios"),
    path('peticiones/', view.peticiones, name="peticiones"),
    path('ayuda/', view.ayuda, name="ayuda"),
    path('reset/', view.reset, name="reset"),
]
