
from django.contrib import admin
from django.urls import path
from .views import view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', view.index , name="index"),
    path('hello/', view.hello, name="hello"),
    path('servicios/', view.servicios, name="servicios"),
    path('peticiones/', view.peticiones, name="peticiones"),
    path('detalle_mensajes/', view.detalle_mensajes, name='detalle_mensajes'),
    path('resumen_pesos/', view.resumen_pesos, name='resumen_pesos'),
    path('prueba_solicitudes/', view.prueba_solicitudes, name='prueba_solicitudes'),
    path('ayuda/', view.ayuda, name="ayuda"),
    path('reset/', view.reset, name="reset"),
    path('abrir_pdf/', view.abrir_pdf, name='abrir_pdf')
]
