from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Alumno
from .forms import AlumnoForm

@login_required
def lista_alumnos(request):
    """Lista todos los alumnos con filtros y búsqueda"""
    alumnos = Alumno.objects.all()
    
    # Búsqueda
    query = request.GET.get('q')
    if query:
        alumnos = alumnos.filter(
            Q(nombres__icontains=query) |
            Q(apellidos__icontains=query) |
            Q(dni__icontains=query) |
            Q(codigo_alumno__icontains=query) |
            Q(email__icontains=query)
        )
    
    # Filtros
    estado = request.GET.get('estado')
    genero = request.GET.get('genero')
    
    if estado:
        alumnos = alumnos.filter(estado=estado)
    if genero:
        alumnos = alumnos.filter(genero=genero)
    
    # Ordenamiento
    orden = request.GET.get('orden', 'apellidos')
    alumnos = alumnos.order_by(orden)
    
    context = {
        'alumnos': alumnos,
        'titulo': 'Lista de Alumnos',
        'total_alumnos': alumnos.count(),
        'alumnos_activos': alumnos.filter(estado='A').count(),
    }
    return render(request, 'alumnos/lista_alumnos.html', context)

@login_required
def detalle_alumno(request, alumno_id):
    """Muestra los detalles de un alumno específico"""
    alumno = get_object_or_404(Alumno, id=alumno_id)
    context = {
        'alumno': alumno,
        'titulo': f'Detalle - {alumno.nombre_completo()}'
    }
    return render(request, 'alumnos/detalle_alumno.html', context)

@login_required
def nuevo_alumno(request):
    """Crea un nuevo alumno"""
    if request.method == 'POST':
        form = AlumnoForm(request.POST, request.FILES)
        if form.is_valid():
            alumno = form.save(commit=False)
            alumno.creado_por = request.user
            alumno.save()
            messages.success(request, f'Alumno "{alumno.nombre_completo()}" creado exitosamente!')
            return redirect('alumnos:lista_alumnos')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = AlumnoForm()
    
    context = {
        'form': form,
        'titulo': 'Nuevo Alumno',
        'accion': 'Crear'
    }
    return render(request, 'alumnos/form_alumno.html', context)

@login_required
def editar_alumno(request, alumno_id):
    """Edita un alumno existente"""
    alumno = get_object_or_404(Alumno, id=alumno_id)
    
    if request.method == 'POST':
        form = AlumnoForm(request.POST, request.FILES, instance=alumno)
        if form.is_valid():
            alumno_editado = form.save()
            messages.success(request, f'Alumno "{alumno_editado.nombre_completo()}" actualizado exitosamente!')
            return redirect('alumnos:detalle_alumno', alumno_id=alumno.id)
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = AlumnoForm(instance=alumno)
    
    context = {
        'form': form,
        'alumno': alumno,
        'titulo': f'Editar - {alumno.nombre_completo()}',
        'accion': 'Actualizar'
    }
    return render(request, 'alumnos/form_alumno.html', context)

@login_required
def eliminar_alumno(request, alumno_id):
    """Elimina un alumno"""
    alumno = get_object_or_404(Alumno, id=alumno_id)
    
    if request.method == 'POST':
        nombre_alumno = alumno.nombre_completo()
        alumno.delete()
        messages.success(request, f'Alumno "{nombre_alumno}" eliminado exitosamente!')
        return redirect('alumnos:lista_alumnos')
    
    context = {
        'alumno': alumno,
        'titulo': 'Eliminar Alumno'
    }
    return render(request, 'alumnos/eliminar_alumno.html', context)

@login_required
def buscar_alumnos(request):
    """Búsqueda avanzada de alumnos"""
    alumnos = Alumno.objects.all()
    query = request.GET.get('q')
    
    if query:
        alumnos = alumnos.filter(
            Q(nombres__icontains=query) |
            Q(apellidos__icontains=query) |
            Q(dni__icontains=query) |
            Q(codigo_alumno__icontains=query)
        )
    
    context = {
        'alumnos': alumnos,
        'query': query,
        'titulo': 'Búsqueda de Alumnos'
    }
    return render(request, 'alumnos/buscar_alumnos.html', context)