from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cargarAlumnos", views.cargar_alumnos, name="cargar_alumnos"),
    path("listarAlumnos", views.listar_alumnos, name="listar_alumnos"),
    path("alumno", views.form_alumno, name="form_alumno"),
    path("obtenerAlumno", views.obtener_alumno, name="obtener_alumno"),
    path("modificarAlumno", views.modificar_alumno, name="modificar_alumno"),
    path("eliminarAlumno", views.eliminar_alumno, name="eliminar_alumno"),
    path("asignarCurso",views.asignar_curso, name="asignar_curso"),
    path("alumnosPorCurso", views.alumnos_por_curso, name="alumnos_por_curso"),
]
