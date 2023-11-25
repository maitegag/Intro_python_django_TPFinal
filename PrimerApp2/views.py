import json
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Alumno, Curso, BandaHoraria
import csv
from pathlib import Path
#from PrimerProyecto2.settings import lista_alumnos_actualizada

# Funcion que lee un archivo .csv y carga les alumnes desde el mismo

def index(request):
    return render(request, 'form.html')

def cargar_alumnos(request):
    if request.method == "POST" and request.POST.get("csv_fn"):
        #csv_file = request.FILES["base_datos_alumnos"]  F:\base_datos_alumnos.csv
        if request.POST["csv_fn"].endswith(".csv"):
            try:
                csv_fn = request.POST["csv_fn"].strip()
                csv_fn = csv_fn.replace("\\\\", "\\")
                #return JsonResponse(f"archivo {csv_fn}", status=200, safe=False)
                with open (csv_fn, "r", newline="", encoding="latin-1") as f:
                    csv_data =  csv.reader(f)
                    next(csv_data)       # skips headers
                    # Iterate through the CSV data and create or update Alumno objects
                    ya_existentes = set()  # create a set to check duplicates

                    for row in csv_data:
                        (nombre, apellido, dni, telefono, correo_electronico,
                            curso_id, curso_descripcion, curso_nota,
                            banda_nombre, banda_inicio, banda_fin) = row[0].split(";")
                        if dni not in ya_existentes:
                            ya_existentes.add(dni)
                        else:
                            pass
                        
                        banda = BandaHoraria(nombre=banda_nombre, horario_inicio = banda_inicio,
                                      horario_fin=banda_fin)
                        banda.save()
                        curso = Curso(nombre=curso_id, descripcion = curso_descripcion,
                                      banda_horaria=banda, nota=curso_nota)
                        curso.save()
                        alumno = Alumno(
                            nombre=nombre, apellido=apellido, dni=dni, telefono=telefono,
                            correo_electronico=correo_electronico, curso=curso
                        )
                        alumno.save()
#                        lista_alumnos_actualizada.append(alumno)

                return JsonResponse(
                    {"message": "Alumnos cargados correctamente."}, status=200)
            
            except Exception as e:
                return JsonResponse({"todo mal": str(e)}, status=400)
        else:
            return JsonResponse(
                {"error": "El archivo debe ser un archivo CSV valido."}, status=400
            )
    else:
        return JsonResponse(
            {"error": f"Debe proporcionar un archivo CSV para cargar."}, status=400
        )

# Función que lista les alumnes cargado


def listar_alumnos(request):  # Función para listar alumnos
    # Serializa los datos de les alumnes en una lista de diccionarios
    serialized_alumnos = []
    for alumno in Alumno.objects.all():
        #a = alumno.objects.get(pk=1)
        serialized_alumnos.append(
            {
                "nombre": alumno.nombre,
                "apellido": alumno.apellido,
                "dni": alumno.dni,
                "telefono": alumno.telefono,
                "correo_electronico": alumno.correo_electronico,
                "curso_id": alumno.curso.nombre,
                "curso_descripcion": alumno.curso.descripcion,
                "curso_nota": alumno.curso.nota,
                "banda_nombre" : alumno.curso.banda_horaria.nombre,
                "banda_inicio" : alumno.curso.banda_horaria.horario_inicio,
                "banda_fin" : alumno.curso.banda_horaria.horario_fin,
                
            }
        )
    return JsonResponse({"alumnos": f"{serialized_alumnos}"}, status=200)


# Función que retorna la informción de un alumne en formato .csv
def form_alumno(request):
    return render(request, 'form_alumno.html')

def obtener_alumno(request):
    if request.method == "POST" and request.POST.get("input_dni"):
        input_dni_str = request.POST.get("input_dni")
        try:
            input_dni = int(input_dni_str)
        except ValueError:
            return JsonResponse({"error": f"DNI invalido: {input_dni_str}."}, status=400)
    else:
        return JsonResponse({"error": "No ha ingresado un DNI."}, status=400)
    
    alumno = get_object_or_404(Alumno, dni=input_dni)

    # Serializa los datos de les alumnes en un diccionario
    serialized_alumno = {
        "nombre": alumno.nombre,
        "apellido": alumno.apellido,
        "dni": alumno.dni,
        "telefono": alumno.telefono,
        "correo_electronico": alumno.correo_electronico,
        "curso": alumno.curso.nombre if alumno.curso else None,
        "banda_horaria": alumno.curso.banda_horaria.nombre if alumno.curso else None,
    }

    #alumno_buscado = csv.writer(serialized_alumno)

    return JsonResponse({"alumno": serialized_alumno})


# FALTA: g, h, i, j

# Función que permite modificar la informacion de un alumne
def modificar_alumno(request, dni):
    alumno = get_object_or_404(Alumno, dni=dni)

    if request.method == "PUT":
        try:
            data = json.loads(request.body.decode("utf-8"))

            # Actualiza los campos del alumno con los datos proporcionados
            alumno.nombre = data.get("nombre", alumno.nombre)
            alumno.apellido = data.get("apellido", alumno.apellido)
            alumno.telefono = data.get("telefono", alumno.telefono)
            alumno.correo_electronico = data.get(
                "correo_electronico", alumno.correo_electronico
            )
            alumno.curso = data.get("curso", alumno.curso)

            alumno.save()  # guarda el registro actualizado en la base de datos

            return JsonResponse(
                {"message": "Alumno modificado correctamente"}, status=200
            )

        except json.JSONDecodeError as e:
            return JsonResponse(
                {"error": "Error en el formato JSON de la solicitud"}, status=400
            )

    else:
        return JsonResponse(
            {
                "error": "Método no permitido. Utiliza el método PUT para modificar al alumno"
            },
            status=405,
        )

    # Función que permita eliminar une alumne existente


def eliminar_alumno(request, dni):
    alumno = get_object_or_404(Alumno, dni=dni)

    if request.method == "DELETE":
        alumno.delete()

        return JsonResponse({"message": "Alumno eliminado correctamente"}, status=200)

    else:
        return JsonResponse(
            {
                "error": "Método no permitido. Utiliza el método DELETE para eliminar al alumno"
            },
            status=405,
        )


# Función que asigne el curso a un alumne


def asignar_curso(request, dni, id_curso):
    alumno = get_object_or_404(Alumno, dni=dni)
    curso = get_object_or_404(Curso, id=id_curso)

    if request.method == "POST":
        alumno.curso = curso
        alumno.save()

        return JsonResponse(
            {"message": f"Curso asignado correctamente al alumno con DNI {dni}"},
            status=200,
        )

    else:
        JsonResponse(
            {
                "error": "Método no permitido. Utiliza el método POST para asignar el curso"
            },
            status=405,
        )


# Función para consultar alumnes por curso


def alumnos_por_curso(request, id_curso):
    #alumnos = Alumno.objects.filter(curso_id=id_curso)

    serialized_alumnos = []
    

    return JsonResponse({"alumnos": serialized_alumnos})