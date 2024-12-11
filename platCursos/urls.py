from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.conf.urls.i18n import i18n_patterns
from cursos import views  # Substitua app_name pelo nome correto do app
from cursos.views import asaas_webhook


urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('login.urls')),  # Incluindo as URLs do app "login"
    path('', include(('cursos.urls', 'cursos'), namespace='cursos')),  # Incluindo o app "cursos" sem prefixo redundante
    path('logout/', LogoutView.as_view(), name='logout'),  # URL específica para logout
    path('asaas-webhook/', views.asaas_webhook, name='asaas_webhook'),
    path('asaas-webhook/', asaas_webhook, name='asaas_webhook'),
    path('change-password/', PasswordChangeView.as_view(template_name='change_password.html'), name='change_password'),  # Alteração de senha
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
