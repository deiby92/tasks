from django.contrib import admin
from .models import tarea, datos, Profile

class TareaAdmin(admin.ModelAdmin):
    readonly_fields = ('creada', )

# Register your models here.
admin.site.register(tarea, TareaAdmin)
admin.site.register(datos)
admin.site.register(Profile)

