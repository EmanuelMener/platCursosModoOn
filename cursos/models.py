from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator

class Curso(models.Model):
    nome = models.CharField(max_length=255)
    horario = models.CharField(max_length=100, blank=True, null=True)
    local = models.CharField(max_length=100, blank=True, null=True)
    numero_alunos = models.IntegerField(default=0)
    codigo = models.CharField(max_length=50, blank=True, null=True)
    turma = models.CharField(max_length=50, blank=True, null=True)
    semestre = models.CharField(max_length=50, blank=True, null=True)
    capa = models.ImageField(upload_to='cursos/capas/', blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.nome

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notificação para {self.user.username} - {self.message}"

# Signal para criar notificação ao adicionar um novo curso
@receiver(post_save, sender=Curso)
def notify_new_course(sender, instance, created, **kwargs):
    if created:  # Somente para cursos recém-criados
        users = User.objects.all()
        for user in users:
            Notification.objects.create(
                user=user,
                message=f"Um novo curso foi adicionado: {instance.nome}",
                is_read=False
            )

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    cpf = models.CharField(
        max_length=14,
        blank=True,
        null=True,
        validators=[RegexValidator(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', 'CPF inválido. Use o formato XXX.XXX.XXX-XX.')]
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class ClienteCursos(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cursos")
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    tipo_aquisicao = models.CharField(max_length=20, choices=[("Vip ", "Vip"), ("Comprado", "Comprado")], default="Comprado")

    def __str__(self):
        return f"{self.usuario.username} - {self.curso.nome} ({self.tipo_aquisicao})"

@receiver(post_save, sender=ClienteCursos)
def notify_course_acquired(sender, instance, created, **kwargs):
    if created:  # Apenas quando um novo curso é associado ao usuário
        Notification.objects.create(
            user=instance.usuario,
            message=f"Você agora tem acesso ao curso: {instance.curso.nome}",
            is_read=False
        )

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    cpf = models.CharField(max_length=14, blank=True, null=True)  # Campo para CPF
    asaas_customer_id = models.CharField(max_length=50, blank=True, null=True)  # Novo campo

    def __str__(self):
        return f"{self.user.username}'s Profile"

