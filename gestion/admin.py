from django.contrib import admin

from .models import Curso, Estudiante


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "creditos", "cupo_maximo", "activo")
    search_fields = ("codigo", "nombre")


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ("cedula", "nombres", "apellidos", "email")
    search_fields = ("cedula", "nombres", "apellidos", "email")
    filter_horizontal = ("cursos",)
