from django.db import models


class Curso(models.Model):
    """Curso o materia ofertada por la universidad."""

    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=120)
    creditos = models.PositiveSmallIntegerField(default=3)
    cupo_maximo = models.PositiveSmallIntegerField(default=30)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["codigo"]
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    def cupos_disponibles(self):
        return self.cupo_maximo - self.estudiantes.count()


class Estudiante(models.Model):
    """Estudiante matriculado en la universidad."""

    cedula = models.CharField(max_length=10, unique=True)
    nombres = models.CharField(max_length=80)
    apellidos = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    fecha_ingreso = models.DateField(auto_now_add=True)
    cursos = models.ManyToManyField(Curso, related_name="estudiantes", blank=True)

    class Meta:
        ordering = ["apellidos", "nombres"]
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"

    def __str__(self):
        return f"{self.apellidos} {self.nombres} ({self.cedula})"

    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"
