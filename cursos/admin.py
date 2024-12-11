from django.contrib import admin
from .models import Curso, ClienteCursos, Notification
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Profile

# Inline para adicionar cursos diretamente no perfil do usuário
class ClienteCursosInline(admin.TabularInline):
    model = ClienteCursos
    extra = 1  # Permite adicionar vários cursos diretamente no admin de usuários

# Configuração para o modelo Curso
@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'horario', 'local', 'numero_alunos', 'preco')
    search_fields = ('nome', 'codigo', 'turma', 'semestre')
    list_filter = ('local', 'semestre')

# Configuração para o modelo ClienteCursos
@admin.register(ClienteCursos)
class ClienteCursosAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'curso', 'tipo_aquisicao')
    search_fields = ('usuario__username', 'curso__nome')
    list_filter = ('tipo_aquisicao',)

# Configuração para o modelo Notification
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'is_read')
    search_fields = ('user__username', 'message')
    list_filter = ('is_read', 'created_at')

# Customização do admin de usuários para incluir o Inline de ClienteCursos
class CustomUserAdmin(UserAdmin):
    inlines = [ClienteCursosInline]

# Desregistrar o modelo padrão de usuários e registrar com as customizações
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'cpf')  # Mostra o usuário e o CPF na listagem
    search_fields = ('user__username', 'cpf')  # Permite busca por nome de usuário e CPF

