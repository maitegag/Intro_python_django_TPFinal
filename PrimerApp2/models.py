from django.db import models

# Create your models here.

# Item 1.c)
class BandaHoraria(models.Model):
    nombre = models.CharField(max_length=250)
    horario_inicio = models.IntegerField()
    horario_fin = models.IntegerField()


# Item 1.b)
class Curso(models.Model):
    nombre = models.CharField(max_length=250)
    descripcion = models.CharField(max_length=250)
    banda_horaria = models.ForeignKey(BandaHoraria, on_delete=models.CASCADE)
    nota = models.IntegerField()


# Item 1.a)
class Alumno(models.Model):
    nombre = models.CharField(max_length=250)
    apellido = models.CharField(max_length=250)
    dni = models.IntegerField(primary_key=True)
    telefono = models.CharField(max_length=15)
    correo_electronico = models.EmailField()
    curso = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True)