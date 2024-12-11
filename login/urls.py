from django.urls import path
from .views import login_view, register

urlpatterns = [
    path('', login_view, name='login'),  # Agora acessível como /login/
    path('register/', register, name='register'),
]
