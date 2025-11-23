from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Curso
from .forms import CursoForm

@login_required
def lista_cursos(request):
    """Lista todos los cursos"""
    cursos = Curso.objects.all()
    
    # Filtros
    nivel = request.GET.get('nivel')
    estado = request.GET.get('estado')
    
    if nivel:
        cursos = cursos.filter(nivel=nivel)
    if estado:
        cursos = cursos.filter(estado=estado)
    
    context = {
        'cursos': cursos,
        'titulo': 'Lista de Cursos'
    }
    return render(request, 'cursos/lista_cursos.html', context)

@login_required
def detalle_curso(request, curso_id):
    """Muestra los detalles de un curso específico"""
    curso = get_object_or_404(Curso, id=curso_id)
    context = {
        'curso': curso,
        'titulo': f'Detalle - {curso.nombre}'
    }
    return render(request, 'cursos/detalle_curso.html', context)

@login_required
def nuevo_curso(request):
    """Crea un nuevo curso"""
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            curso = form.save(commit=False)
            curso.creado_por = request.user
            curso.save()
            messages.success(request, f'Curso "{curso.nombre}" creado exitosamente!')
            return redirect('cursos:lista_cursos')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = CursoForm()
    
    context = {
        'form': form,
        'titulo': 'Nuevo Curso',
        'accion': 'Crear'
    }
    return render(request, 'cursos/form_curso.html', context)

@login_required
def editar_curso(request, curso_id):
    """Edita un curso existente"""
    curso = get_object_or_404(Curso, id=curso_id)
    
    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            curso_editado = form.save()
            messages.success(request, f'Curso "{curso_editado.nombre}" actualizado exitosamente!')
            return redirect('cursos:detalle_curso', curso_id=curso.id)
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = CursoForm(instance=curso)
    
    context = {
        'form': form,
        'curso': curso,
        'titulo': f'Editar - {curso.nombre}',
        'accion': 'Actualizar'
    }
    return render(request, 'cursos/form_curso.html', context)

@login_required
def eliminar_curso(request, curso_id):
    """Elimina un curso"""
    curso = get_object_or_404(Curso, id=curso_id)
    
    if request.method == 'POST':
        nombre_curso = curso.nombre
        curso.delete()
        messages.success(request, f'Curso "{nombre_curso}" eliminado exitosamente!')
        return redirect('cursos:lista_cursos')
    
    context = {
        'curso': curso,
        'titulo': 'Eliminar Curso'
    }
    return render(request, 'cursos/eliminar_curso.html', context)

@login_required
def alumnos_curso(request, curso_id):
    """Muestra los alumnos inscritos en un curso"""
    curso = get_object_or_404(Curso, id=curso_id)
    # Esto lo completaremos cuando tengamos el modelo de matrículas
    context = {
        'curso': curso,
        'titulo': f'Alumnos de {curso.nombre}'
    }
    return render(request, 'cursos/alumnos_curso.html', context)