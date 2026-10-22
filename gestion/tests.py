from django.test import TestCase

from .models import Curso, Estudiante


class CursoTests(TestCase):
    """Prueba 1: creacion de un curso y calculo de cupos."""

    def test_creacion_curso_y_cupos_disponibles(self):
        curso = Curso.objects.create(
            codigo="SIS101", nombre="Fundamentos de Software", creditos=4, cupo_maximo=25
        )

        self.assertEqual(Curso.objects.count(), 1)
        self.assertEqual(str(curso), "SIS101 - Fundamentos de Software")
        self.assertEqual(curso.cupos_disponibles(), 25)


class EstudianteTests(TestCase):
    """Prueba 2: matricula de un estudiante en un curso."""

    def test_estudiante_se_matricula_en_curso(self):
        curso = Curso.objects.create(
            codigo="SIS202", nombre="DevOps Aplicado", creditos=3, cupo_maximo=30
        )
        estudiante = Estudiante.objects.create(
            cedula="0102030405",
            nombres="Ana Maria",
            apellidos="Chafla",
            email="ana.chafla@universidad.edu",
        )
        estudiante.cursos.add(curso)

        self.assertEqual(estudiante.nombre_completo(), "Ana Maria Chafla")
        self.assertIn(curso, estudiante.cursos.all())
        self.assertEqual(curso.cupos_disponibles(), 29)
