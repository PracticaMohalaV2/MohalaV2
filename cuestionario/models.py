from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save 
from django.dispatch import receiver 

# =========================
# Tabla Escala
# =========================
class Escala(models.Model):
    id_escala = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'ESCALA'

    def __str__(self):
        return f"{self.id_escala} - {self.descripcion}"

# =========================
# Tabla Dimension
# =========================
class Dimension(models.Model):
    id_dimension = models.AutoField(primary_key=True)
    nombre_dimension = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'DIMENSION'

    def __str__(self):
        return self.nombre_dimension

# =========================
# Tabla Departamento
# =========================
class Departamento(models.Model):
    id_departamento = models.AutoField(primary_key=True)
    nombre_departamento = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'DEPARTAMENTO'

    def __str__(self):
        return self.nombre_departamento

# =========================
# Tabla Nivel Jerarquico
# =========================
class NivelJerarquico(models.Model):
    id_nivel_jerarquico = models.AutoField(primary_key=True)
    nombre_nivel_jerarquico = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'NIVEL_JERARQUICO'

    def __str__(self):
        return self.nombre_nivel_jerarquico

# =========================
# Tabla Cargo
# =========================
class Cargo(models.Model):
    id_cargo = models.AutoField(primary_key=True)
    nombre_cargo = models.CharField(max_length=50)
    nivel_jerarquico = models.ForeignKey(
        'NivelJerarquico', 
        on_delete=models.DO_NOTHING, 
        db_column='nivel_jerarquico_id_nivel_jerarquico'
    )

    class Meta:
        managed = False
        db_table = 'CARGO'

    def __str__(self):
        return self.nombre_cargo

# =========================
# Tabla Trabajador
# =========================
class Trabajador(models.Model):
    id_trabajador = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=20, unique=True)
    id_jefe_directo = models.ForeignKey(
        'self', 
        on_delete=models.DO_NOTHING, 
        db_column='id_jefe_directo', 
        null=True, 
        blank=True, 
        related_name='subordinados'
    )
    nombre = models.CharField(max_length=40)
    apellido_paterno = models.CharField(max_length=40)
    apellido_materno = models.CharField(max_length=40)
    email = models.CharField(max_length=80)
    genero = models.CharField(max_length=10)
    nivel_jerarquico = models.ForeignKey(
        'NivelJerarquico', 
        on_delete=models.DO_NOTHING, 
        db_column='nivel_jerarquico_id_nivel_jerarquico'
    )
    cargo = models.ForeignKey(
        'Cargo', 
        on_delete=models.DO_NOTHING, 
        db_column='cargo_id_cargo'
    )
    departamento = models.ForeignKey(
        'Departamento', 
        on_delete=models.DO_NOTHING, 
        db_column='departamento_id_departamento'
    )

    user = models.OneToOneField(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        db_column='user_id' 
    )

    class Meta:
        managed = False
        db_table = 'TRABAJADOR'

    @property
    def es_jefe(self):
        return self.subordinados.exists()

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} | {self.rut}"

# =========================
# Tabla Competencia
# =========================
class Competencia(models.Model):
    id_competencia = models.AutoField(primary_key=True)
    nombre_competencia = models.CharField(max_length=50)
    dimension = models.ForeignKey(
        'Dimension', 
        on_delete=models.DO_NOTHING, 
        db_column='dimension_id_dimension'
    )

    class Meta:
        managed = False
        db_table = 'COMPETENCIA'

    def __str__(self):
        return self.nombre_competencia

# =========================
# Tabla Textos Evaluacion
# =========================
class TextosEvaluacion(models.Model):
    id_textos_evaluacion = models.AutoField(primary_key=True)
    codigo_excel = models.CharField(max_length=10, unique=True)
    texto = models.TextField()
    dimension = models.ForeignKey(
        'Dimension', 
        on_delete=models.DO_NOTHING, 
        db_column='dimension_id_dimension'
    )
    competencia = models.ForeignKey(
        'Competencia', 
        on_delete=models.DO_NOTHING, 
        db_column='competencia_id_competencia'
    )
    nivel_jerarquico = models.ForeignKey(
        'NivelJerarquico', 
        on_delete=models.DO_NOTHING, 
        db_column='nivel_jerarquico_id_nivel_jerarquico'
    )

    class Meta:
        managed = False
        db_table = 'TEXTOS_EVALUACION'

    def __str__(self):
        return f"[{self.codigo_excel}]"

# =========================
# Tabla Autoevaluacion
# =========================
class Autoevaluacion(models.Model):
    id_autoevaluacion = models.AutoField(primary_key=True)
    puntaje = models.IntegerField()  
    escala = models.ForeignKey(
        'Escala', 
        on_delete=models.DO_NOTHING, 
        db_column='escala_id_escala'
    )
    fecha_evaluacion = models.DateField()
    momento_evaluacion = models.DateTimeField(auto_now_add=True)
    estado_finalizacion = models.BooleanField(default=False)
    comentario = models.TextField(null=True, blank=True)
    trabajador = models.ForeignKey(
        'Trabajador', 
        on_delete=models.DO_NOTHING, 
        db_column='trabajador_id_trabajador'
    )
    codigo_excel = models.ForeignKey(
        'TextosEvaluacion', 
        on_delete=models.DO_NOTHING, 
        to_field='codigo_excel', 
        db_column='codigo_excel'
    )
    nivel_jerarquico = models.ForeignKey(
        'NivelJerarquico', 
        on_delete=models.DO_NOTHING, 
        db_column='nivel_jerarquico_id_nivel_jerarquico'
    )

    class Meta:
        managed = False
        db_table = 'AUTOEVALUACION'
        unique_together = (('trabajador', 'codigo_excel'),)

# =========================
# Tabla Evaluacion Jefatura
# =========================
class EvaluacionJefatura(models.Model):
    id_evaluacion_jefatura = models.AutoField(primary_key=True)
    puntaje = models.IntegerField() 
    escala = models.ForeignKey(
        'Escala', 
        on_delete=models.DO_NOTHING, 
        db_column='escala_id_escala'
    )
    evaluador = models.ForeignKey(
        'Trabajador', 
        on_delete=models.DO_NOTHING, 
        db_column='evaluador_id_trabajador', 
        related_name='jefe_evaluador'
    )
    fecha_evaluacion = models.DateField()
    momento_evaluacion = models.DateTimeField(auto_now_add=True)
    estado_finalizacion = models.BooleanField(default=False)
    comentario = models.TextField(null=True, blank=True)
    trabajador_evaluado = models.ForeignKey(
        'Trabajador', 
        on_delete=models.DO_NOTHING, 
        db_column='trabajador_id_trabajador', 
        related_name='subordinado_evaluado'
    )
    codigo_excel = models.ForeignKey(
        'TextosEvaluacion', 
        on_delete=models.DO_NOTHING, 
        to_field='codigo_excel', 
        db_column='codigo_excel'
    )
    nivel_jerarquico = models.ForeignKey(
        'NivelJerarquico', 
        on_delete=models.DO_NOTHING, 
        db_column='nivel_jerarquico_id_nivel_jerarquico'
    )

    class Meta:
        managed = False
        db_table = 'EVALUACION_JEFATURA'
        unique_together = (('evaluador', 'trabajador_evaluado', 'codigo_excel'),)

# =========================
# Tabla Resultado Consolidado
# =========================
class ResultadoConsolidado(models.Model):
    id_resultado = models.AutoField(primary_key=True)
    puntaje_autoev = models.IntegerField() 
    puntaje_jefe = models.IntegerField()   
    diferencia = models.IntegerField()    

    trabajador = models.ForeignKey(
        'Trabajador', 
        on_delete=models.DO_NOTHING, 
        db_column='trabajador_id_trabajador'
    )
    dimension = models.ForeignKey(
        'Dimension', 
        on_delete=models.DO_NOTHING, 
        db_column='dimension_id_dimension'
    )
    competencia = models.ForeignKey(
        'Competencia', 
        on_delete=models.DO_NOTHING, 
        db_column='competencia_id_competencia'
    )
    codigo_excel = models.ForeignKey(
        'TextosEvaluacion', 
        on_delete=models.DO_NOTHING, 
        to_field='codigo_excel', 
        db_column='codigo_excel'
    )
    nivel_jerarquico = models.ForeignKey(
        'NivelJerarquico', 
        on_delete=models.DO_NOTHING, 
        db_column='nivel_jerarquico_id_nivel_jerarquico'
    )
    
    periodo = models.IntegerField()
    fecha_consolidacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'RESULTADO_CONSOLIDADO'
        unique_together = (('trabajador', 'codigo_excel', 'periodo'),)

# =========================
# Tabla Descripcion Respuesta
# =========================
class DescripcionRespuesta(models.Model):
    id_descripcion_respuesta = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    codigo_excel = models.ForeignKey(
        'TextosEvaluacion', 
        on_delete=models.DO_NOTHING, 
        to_field='codigo_excel', 
        db_column='codigo_excel'
    )
    escala = models.ForeignKey(
        'Escala', 
        on_delete=models.DO_NOTHING, 
        db_column='escala_id_escala'
    )
    dimension = models.ForeignKey(
        'Dimension', 
        on_delete=models.DO_NOTHING, 
        db_column='dimension_id_dimension'
    )
    competencia = models.ForeignKey(
        'Competencia', 
        on_delete=models.DO_NOTHING, 
        db_column='competencia_id_competencia'
    )
    nivel_jerarquico = models.ForeignKey(
        'NivelJerarquico', 
        on_delete=models.DO_NOTHING, 
        db_column='nivel_jerarquico_id_nivel_jerarquico'
    )

    class Meta:
        managed = False
        db_table = 'DESCRIPCION_RESPUESTA'
        unique_together = (('codigo_excel', 'nivel_jerarquico', 'escala'),)

# ==========================================================
# SIGNALS: Automatización de creación de usuarios para Login
# ==========================================================
@receiver(post_save, sender=Trabajador)
def crear_usuario_automatico(sender, instance, created, **kwargs):
    if created and not instance.user:
        nuevo_user = User.objects.create_user(
            username=instance.email,
            email=instance.email,
            password='Mohala2026'
        )
        instance.user = nuevo_user
        instance.save()

# ==========================================================
# Reporte Global
# ==========================================================
class ReporteGlobal(models.Model):
    id_reporte_global = models.AutoField(primary_key=True)
    contenido_pdf = models.BinaryField()
    timestamp = models.DateTimeField(auto_now_add=True)
    total_trabajadores = models.IntegerField(default=0)
    periodo = models.IntegerField(default=2026)

    class Meta:
        db_table = 'REPORTE_GLOBAL'

    def __str__(self):
        return f"Reporte Global {self.id_reporte_global} - Periodo {self.periodo}"


# ==========================================================
# Gemini
# ==========================================================
class PromptGemini(models.Model):
    id_prompt = models.AutoField(primary_key=True)
    prompt_texto = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    respuesta_gemini = models.TextField(null=True, blank=True)
    pdf_generado = models.BooleanField(default=False)
    archivo_pdf = models.BinaryField(null=True, blank=True)
    
    reporte_global = models.ForeignKey(
        ReporteGlobal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='REPORTE_GLOBAL_ID'
    )

    class Meta:
        db_table = 'PROMPT_GEMINI'
        ordering = ['-timestamp']

    def __str__(self):
        return f"Prompt {self.id_prompt} - {self.timestamp.strftime('%d/%m/%Y')}"
    
# ==========================================================
# Biblioteca
# ==========================================================
class Biblioteca(models.Model):
    id_biblioteca = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    archivo = models.BinaryField(editable=True)
    estado_carga = models.BooleanField(default=False)
    fecha_carga = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'BIBLIOTECA'

    def __str__(self):
        return self.nombre