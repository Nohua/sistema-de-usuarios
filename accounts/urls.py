from django.urls import path
from .views import (
    login_page,
    home,
    pagina_registro,
    activate,
    logout,
)

urlpatterns = [
    path('home/', home),
    path('', login_page),
    path('logout/', logout, name="termino-sesion"),
    path('registro/', pagina_registro),
    path('activate/<uid>/<token>', activate, name="activate"),
]
