from .forms import UserRegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('cursos:painel_cursos')  # Redireciona para o painel de cursos
        else:
            messages.error(request, 'Username or password is incorrect.')
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        # Obter dados do formulário
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Verificar se as senhas correspondem
        if password1 != password2:
            messages.error(request, 'As senhas não coincidem.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'O nome de usuário já existe.')
        else:
            # Criar o usuário
            User.objects.create_user(username=username, password=password1)
            messages.success(request, 'Conta criada com sucesso! Faça login.')
            return redirect('login')

    # Definir form como vazio para evitar erros
    form = None
    return render(request, 'register.html', {'form': form})
