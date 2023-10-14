from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator


# Create your models here.
class Empresa(models.Model):
    nome = models.CharField(max_length=60)
    CNPJ = models.CharField(max_length=14)
    endereco = models.CharField(max_length=200)
    fone = models.PositiveBigIntegerField(validators=[MaxValueValidator(99999999999)])
    inscricao = models.CharField(max_length=200)
    razao_social = models.CharField(max_length=200)
    registro = models.CharField(max_length=200)
    
    def __str__(self):
        return self.nome

class UserProfile(models.Model):
    user = models.OneToOneField(
        User, 
        verbose_name=_("user"), 
        on_delete=models.CASCADE
    )
    empresa = models.ForeignKey(Empresa, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

class Person(models.Model):
    nome = models.CharField(max_length=200)
    funcao = models.CharField(max_length=200)
    