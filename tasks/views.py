from lib2to3.fixes.fix_input import context
from django.conf import settings
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import  render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ResetPasswordForm, TaskForm, update
from .models import tarea, Profile
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView


def registrar(request):
    tasks = User.objects.all(usuario=request.user) #completada__isnull=True filtar por tareas completadas 
    return render(request,'register.html', {'tasks':tasks})
def Home(request):
    return render(request,'Home.html')

def signup(request):

    if request.method == 'GET':
         return render(request,'signup.html', {
             'form':UserCreationForm
             })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
               # registrar usuarios
               user = User.objects.create_user(username=request.POST['username'], 
               password=request.POST['password1'], first_name=request.POST['first_name'], last_name=request.POST['last_name'],  email=request.POST['email'],                       )
               user.save()
               login(request, user)
               return redirect('tasks')
                        
            except:
                return render(request,'signup.html',{
                    'form':UserCreationForm,
                    "error":'usuario existe'
                })
        return render(request,'signup.html',{
                    'form':UserCreationForm,
                    "error":'Contraseña no coincide'
                })
    
# funcion de pagina de tareas 
@login_required
def tasks(request):
    tasks = tarea.objects.filter(usuario=request.user, completada__isnull=True) #completada__isnull=True filtar por tareas completadas 
    return render(request,'tasks.html', {'tasks':tasks})

# funcion de tareas para ver las tareas todas 
@login_required
def tasks_completa(request):
    tasks = tarea.objects.filter(usuario=request.user, completada__isnull=False).order_by('-completada') #completada__isnull=True filtar por tareas completadas 
    return render(request,'tasks.html', {'tasks':tasks})

#funcion cierre de sesion
@login_required
def signout(request):
    logout(request)
    return redirect('Home')

#funcion inicio de sesion 
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
        'form': AuthenticationForm
    })
    else:
       user =  authenticate(request, username=request.POST['username'], password=request.POST['password'])
    if user is None:
        return render(request, 'signin.html', {
            'form': AuthenticationForm,
             'error':'Usuario o contraseña incorrecta'
            })
    else:
        login(request, user)
        return redirect('perfil')

# Mostrar visualmente la creacion de tareas  
@login_required  
def create_task(request):
    if request.method == 'GET':
        return render(request, 'crea_tarea.html',{
            'form': TaskForm
        })
    else:
        try:
            form= TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.usuario = request.user
            new_task.save()
            return redirect('tasks')
        except:
            return render(request, 'crea_tarea.html',{
            'form': TaskForm,
            'error':'ingrese datos correctos' 

        })

# detalle de tareas 
@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(tarea, pk=task_id, usuario=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {
        'task':task,
        'form': form
         })
    else:
        try:
            task = get_object_or_404(tarea, pk=task_id, usuario=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
           return render(request, 'task_detail.html', {
           'task':task,
           'form': form,
           'error':"Error al actualizar"
            }) 
@login_required
def complete(request, task_id):
    task = get_object_or_404(tarea, pk=task_id, usuario=request.user)
    if request.method == 'POST':
        task.completada = timezone.now()
        task.save()
        return redirect('tasks')
@login_required
def Eliminar_tarea(request, task_id):
    task = get_object_or_404(tarea, pk=task_id, usuario=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

def profile(request):

    tasks = Profile.objects.all() #completada__isnull=True filtar por tareas completadas 
    
    return render(request,'perfil.html', {'tasks':tasks})


def update_profile(request):
    task = get_object_or_404(Profile, user=request.user)  # Obtener el perfil del usuario

    if request.method == 'POST':
        form = update(request.POST, instance=task)  # Suponiendo que 'UpdateForm' es el formulario
        if form.is_valid():  # Verificar si el formulario es válido
            form.save()  # Guardar los cambios en la base de datos
            return redirect('tasks')  # Redirigir a la vista de tareas
        else:
            error = "Error al actualizar"  # Mensaje de error si el formulario no es válido
    else:
        form = update(instance=task)  # Crear un formulario con los datos actuales del perfil
        error = None  # No hay error en el método GET

    return render(request, 'update_profile.html', {
        'task': task,
        'form': form,
        'error': error  # Pasar el mensaje de error a la plantilla
    })

class ResetPasswordView(FormView): # type: ignore
    form_class = ResetPasswordForm
    template_name = 'resetpwd.html'
   

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self):
        pass
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reseteo de Contraseña'
        return context

