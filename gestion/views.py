from django.http import JsonResponse

from .models import Curso, Estudiante


def inicio(request):
    """Vista simple que confirma que el despliegue funciona."""
    return JsonResponse(
        {
            "proyecto": "Sistema de Gestion Universitaria",
            "estudiantes_registrados": Estudiante.objects.count(),
            "cursos_registrados": Curso.objects.count(),
        }
    )


def health(request):
    """Endpoint de health check usado por Docker y el pipeline."""
    return JsonResponse({"status": "ok"})
