from django.db import models
from django.contrib.auth.models import User

# Creacion de tablas.

class tarea(models.Model):
    Titulo = models.CharField(max_length=100)
    descripcion  = models.TextField(blank=True)
    creada = models.DateTimeField (auto_now_add=True)
    completada = models.DateTimeField(null=True, blank=True)
    importante = models.BooleanField(default=False) 
    usuario = models.ForeignKey(User, on_delete= models.CASCADE)

    def __str__(self):
        return self.Titulo + '- by - ' + self.usuario.username
    
class datos(models.Model):
    email= models.EmailField(max_length=100)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Usuario')
    direccion = models.CharField(max_length=150, null=True, blank=True)
    telefono = models.CharField(max_length=50, null=True, blank=True)
    
    class Meta:
        verbose_name = 'perfil'
        verbose_name_plural = 'perfiles'
        ordering = ['-id']

    def __str__(self):
        return self.user.username