

from django.contrib import admin
from django.urls import path
from tasks import views 
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home, name='Home'),
    path('profile/', views.profile, name='perfil'),
    path('profiles/', views.update_profile, name='update_profile'),
    path('signup/', views.signup, name='signup'),
    path('registrar/', views.registrar, name='registrar'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks_completa/', views.tasks_completa, name='task_completa'),
    path("tasks/<int:task_id>/", views.task_detail, name='task_detail'),
    path("tasks/<int:task_id>/complete", views.complete, name='complete'),
    path("tasks/<int:task_id>/eliminar", views.Eliminar_tarea, name='Eliminar_tarea'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('create/', views.create_task, name='create'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="resetpwd.html"), name='password_reset'),
    path('reset_password_send/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="password-confirm.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


]
