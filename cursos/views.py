from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Curso, Notification, ClienteCursos, Profile
from .forms import UserUpdateForm, ProfileUpdateForm
from .asaas import criar_cobranca_pix
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json



@login_required
def painel_de_cursos(request):
    # Obter todos os cursos
    courses = Curso.objects.all()
    # Obter os cursos adquiridos pelo usuário autenticado
    cliente_cursos = ClienteCursos.objects.filter(usuario=request.user)
    cliente_cursos_dict = {
        cliente_curso.curso.id: cliente_curso.tipo_aquisicao
        for cliente_curso in cliente_cursos
    }

    # Adicionar o status de aquisição ao contexto
    courses_with_status = []
    for course in courses:
        if course.id in cliente_cursos_dict:
            tipo_aquisicao = cliente_cursos_dict[course.id]
        else:
            tipo_aquisicao = "Disponível"

        courses_with_status.append({
            "curso": course,
            "tipo_aquisicao": tipo_aquisicao
        })

    # Obter notificações não lidas
    notifications = Notification.objects.filter(user=request.user, is_read=False)

    return render(request, 'painel_cursos.html', {
        'courses_with_status': courses_with_status,
        'notifications': notifications
    })

@login_required
def mark_notifications_as_read(request):
    if request.method == 'POST':
        # Marca as notificações do usuário autenticado como lidas
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'message': 'Todas as notificações foram marcadas como lidas.'}, status=200)
    else:
        return JsonResponse({'error': 'Método não permitido.'}, status=405)

def update_profile(request):
    if request.method == "POST":
        try:
            user = request.user

            # Garante que o Profile existe
            profile, created = Profile.objects.get_or_create(user=user)

            # Atualiza a foto de perfil
            photo = request.FILES.get('photo')
            if photo:
                profile.photo = photo

            # Atualiza o nome
            name = request.POST.get('name')
            if name:
                user.first_name = name.split(' ')[0]
                user.last_name = ' '.join(name.split(' ')[1:])

            # Atualiza o email
            email = request.POST.get('email')
            if email:
                user.email = email

            # Atualiza o CPF
            cpf = request.POST.get('cpf')
            if cpf:
                profile.cpf = cpf

            # Atualiza a senha
            password = request.POST.get('password')
            if password:
                user.set_password(password)

            user.save()
            profile.save()

            return JsonResponse({'success': True, 'message': 'Perfil atualizado com sucesso!'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Erro ao atualizar perfil: {str(e)}'})
    return JsonResponse({'success': False, 'error': 'Método inválido.'})

def listar_cursos(request):
    cursos = Curso.objects.all()
    cliente_cursos = ClienteCursos.objects.filter(usuario=request.user) if request.user.is_authenticated else []
    cliente_cursos_ids = cliente_cursos.values_list('curso_id', flat=True)

    return render(request, 'cursos/listar_cursos.html', {
        'cursos': cursos,
        'cliente_cursos_ids': cliente_cursos_ids,
        'cliente_cursos': cliente_cursos,
    })

def comprar_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    if request.user.is_authenticated:
        ClienteCursos.objects.create(usuario=request.user, curso=curso, tipo_aquisicao='comprado')
        return redirect('listar_cursos')
    else:
        return redirect('login')

@login_required
def criar_pagamento(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)

    try:
        # Recupera os dados do usuário
        user = request.user
        profile = user.profile  # Relacionamento OneToOne com Profile

        # Garante que o CPF está preenchido
        if not profile.cpf:
            return JsonResponse({"success": False, "error": "CPF não cadastrado. Atualize seu perfil para continuar."})

        # Dados para a cobrança
        nome_cliente = user.get_full_name() or user.username
        email_cliente = user.email
        valor = curso.preco
        descricao = f"Compra do curso: {curso.nome}"

        # Cria cobrança PIX
        invoice_url, pix_qr_code = criar_cobranca_pix(nome_cliente, valor, email_cliente, descricao, profile.cpf)

        return JsonResponse({
            "success": True,
            "pixQrCode": pix_qr_code,
            "invoiceUrl": invoice_url,
        })
    except Exception as e:
        error_message = f"Erro ao criar cliente ou cobrança: {str(e)}"
        print(error_message)  # Exibe no console do servidor
        return JsonResponse({"success": False, "error": error_message})

@csrf_exempt
def asaas_webhook(request):
    if request.method == 'POST':
        try:
            # Log da requisição para depuração
            print("Headers:", request.headers)
            print("Body:", request.body)

            # Verifica se o corpo da requisição está vazio
            if not request.body:
                return JsonResponse({"success": False, "error": "Corpo da requisição está vazio."}, status=400)

            # Carrega o JSON do corpo da requisição
            data = json.loads(request.body)

            # Processa os dados
            payment_status = data.get('event')
            payment_id = data.get('payment', {}).get('id')
            customer_id = data.get('payment', {}).get('customer')
            curso_descricao = data.get('payment', {}).get('description')

            if payment_status == "PAYMENT_RECEIVED":
                print(f"Pagamento recebido: {payment_id}, cliente: {customer_id}, curso: {curso_descricao}")
                return JsonResponse({"success": True, "message": "Pagamento processado com sucesso."})
            else:
                return JsonResponse({"success": False, "error": "Evento desconhecido."})

        except json.JSONDecodeError:
            print("Erro: JSON inválido.")
            return JsonResponse({"success": False, "error": "Formato JSON inválido."}, status=400)
        except Exception as e:
            print("Erro no Webhook:", str(e))
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    else:
        return JsonResponse({"success": False, "error": "Método não permitido."}, status=405)
