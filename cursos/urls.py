from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeView
from .views import update_profile
from .views import listar_cursos, comprar_curso


app_name = 'cursos'

urlpatterns = [
    path('', views.painel_de_cursos, name='painel_cursos'),
    path('painel/', views.painel_de_cursos, name='painel_cursos'),  # URL para o painel de cursos
    path('notificacoes/lidas/', views.mark_notifications_as_read, name='mark_notifications_as_read'),
    path('alterar-senha/', PasswordChangeView.as_view(template_name='change_password.html'), name='change_password'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('atualizar-perfil/', update_profile, name='update_profile'),

    path('cursos/', listar_cursos, name='listar_cursos'),
    path('cursos/comprar/<int:curso_id>/', comprar_curso, name='comprar_curso'),

    #caminho api ASAAS
    path('cursos/pagamento/<int:curso_id>/', views.criar_pagamento, name='criar_pagamento'),

]




