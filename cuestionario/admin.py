from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    Dimension, Departamento, NivelJerarquico, Cargo, Trabajador, 
    Competencia, TextosEvaluacion, Autoevaluacion, 
    EvaluacionJefatura, ResultadoConsolidado
)

# --- Configuración Estética ---
admin.site.site_header = "Administración Sistema Mohala"
admin.site.index_title = "Panel de Control Evaluación 2026"

admin.site.unregister(User)

@admin.register(User)
class MyUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'get_rut', 'first_name', 'get_paterno', 'get_materno', 'is_staff')
    
    @admin.display(description='RUT')
    def get_rut(self, obj):
        return obj.trabajador.rut if hasattr(obj, 'trabajador') else "---"

    @admin.display(description='A. Paterno')
    def get_paterno(self, obj):
        return obj.trabajador.apellido_paterno if hasattr(obj, 'trabajador') else "---"

    @admin.display(description='A. Materno')
    def get_materno(self, obj):
        return obj.trabajador.apellido_materno if hasattr(obj, 'trabajador') else "---"

@admin.register(Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):
    list_display = ('id_trabajador', 'nombre', 'apellido_paterno', 'apellido_materno', 'rut', 'email', 'nivel_jerarquico', 'cargo', 'departamento', 'id_jefe_directo')
    list_filter = ('nivel_jerarquico', 'departamento', 'cargo')
    search_fields = ('nombre', 'apellido_paterno', 'rut', 'email')
    ordering = ('apellido_paterno', 'nombre')

@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('nombre_cargo', 'nivel_jerarquico')
    list_filter = ('nivel_jerarquico',)

@admin.register(Competencia)
class CompetenciaAdmin(admin.ModelAdmin):
    list_display = ('nombre_competencia', 'dimension')
    list_filter = ('dimension',)

@admin.register(TextosEvaluacion)
class TextosEvaluacionAdmin(admin.ModelAdmin):
    list_display = ('codigo_excel', 'competencia', 'nivel_jerarquico', 'get_texto_corto')
    list_filter = ('nivel_jerarquico', 'competencia__dimension', 'competencia')
    search_fields = ('codigo_excel', 'texto')
    ordering = ('id_textos_evaluacion',)

    @admin.display(description='Pregunta')
    def get_texto_corto(self, obj):
        return (obj.texto[:60] + '...') if len(obj.texto) > 60 else obj.texto

@admin.register(Autoevaluacion)
class AutoevaluacionAdmin(admin.ModelAdmin):
    list_display = ('trabajador', 'get_nivel_jerarquico', 'codigo_excel', 'get_competencia', 'puntaje', 'estado_finalizacion', 'fecha_evaluacion')
    list_filter = ('estado_finalizacion', 'fecha_evaluacion', 'nivel_jerarquico')
    search_fields = ('trabajador__nombre', 'trabajador__apellido_paterno', 'codigo_excel__codigo_excel')
    ordering = ('codigo_excel__id_textos_evaluacion',)

    @admin.display(description='Nivel Jerárquico', ordering='nivel_jerarquico')
    def get_nivel_jerarquico(self, obj):
        return obj.nivel_jerarquico

    @admin.display(description='Competencia')
    def get_competencia(self, obj):
        return obj.codigo_excel.competencia if obj.codigo_excel else "-"
    
@admin.register(EvaluacionJefatura)
class EvaluacionJefaturaAdmin(admin.ModelAdmin):
    list_display = ('evaluador', 'trabajador_evaluado', 'get_nivel_jerarquico', 'codigo_excel', 'get_competencia', 'puntaje', 'estado_finalizacion')
    list_filter = ('estado_finalizacion', 'evaluador', 'trabajador_evaluado')
    search_fields = ('trabajador__nombre', 'trabajador__apellido_paterno', 'codigo_excel__codigo_excel')
    ordering = ('codigo_excel__id_textos_evaluacion',)

    @admin.display(description='Nivel Jerárquico', ordering='nivel_jerarquico')
    def get_nivel_jerarquico(self, obj):
        return obj.nivel_jerarquico

    @admin.display(description='Competencia')
    def get_competencia(self, obj):
        return obj.codigo_excel.competencia if obj.codigo_excel else "-"

@admin.register(ResultadoConsolidado)
class ResultadoConsolidadoAdmin(admin.ModelAdmin):
    list_display = ('trabajador', 'get_nivel_jerarquico', 'codigo_excel', 'get_competencia', 'puntaje_autoev', 'puntaje_jefe', 'diferencia', 'periodo')
    list_filter = ('periodo', 'trabajador')
    readonly_fields = ('diferencia',)
    ordering = ('codigo_excel__id_textos_evaluacion',)

    @admin.display(description='Nivel Jerárquico', ordering='nivel_jerarquico')
    def get_nivel_jerarquico(self, obj):
        return obj.nivel_jerarquico

    @admin.display(description='Competencia')
    def get_competencia(self, obj):
        return obj.codigo_excel.competencia if obj.codigo_excel else "-"

# Registros simples
admin.site.register(Dimension)
admin.site.register(Departamento)
admin.site.register(NivelJerarquico)