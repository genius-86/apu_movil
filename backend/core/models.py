from django.db import models

class TipoIdentificacion(models.Model):
    id_tipo_identificacion = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=45)
    abreviatura = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = 'tipo_identificacion'
        verbose_name = 'Tipo de Identificación'
        verbose_name_plural = 'Tipos de Identificación'

    def __str__(self):
        return self.descripcion

class Departamento(models.Model):
    id_departamento = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'departamento'

    def __str__(self):
        return self.descripcion

class Municipio(models.Model):
    id_municipio = models.AutoField(primary_key=True)
    id_departamento = models.ForeignKey(Departamento, models.DO_NOTHING, db_column='id_departamento')
    descripcion = models.CharField(max_length=45)
    tiene_contrato = models.CharField(max_length=1)
    latitud = models.DecimalField(max_digits=16, decimal_places=13, blank=True, null=True)
    longitud = models.DecimalField(max_digits=16, decimal_places=13, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'municipio'

    def __str__(self):
        return self.descripcion

class Barrio(models.Model):
    id_barrio = models.AutoField(primary_key=True)
    id_municipio = models.ForeignKey(Municipio, models.DO_NOTHING, db_column='id_municipio')
    descripcion = models.CharField(max_length=80)

    class Meta:
        managed = False
        db_table = 'barrio'
        verbose_name = 'Barrio'
        verbose_name_plural = 'Barrios'

    def __str__(self):
        return self.descripcion

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class TerceroManager(BaseUserManager):
    def create_user(self, usuario, password=None, **extra_fields):
        if not usuario:
            raise ValueError('El usuario es obligatorio')
        user = self.model(usuario=usuario, **extra_fields)
        # Note: legacy system likely doesn't use set_password for MD5 the same way
        # But for new users we might want standard hashing. 
        # For legacy compatibility, we rely on custom password hasher or checking mechanism.
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, usuario, password=None, **extra_fields):
        extra_fields.setdefault('super_usuario', 'S') # Assuming 'S' or '1'
        return self.create_user(usuario, password, **extra_fields)

class Tercero(AbstractBaseUser):
    id_tercero = models.AutoField(primary_key=True)
    id_tipo_identificacion = models.ForeignKey(TipoIdentificacion, models.DO_NOTHING, db_column='id_tipo_identificacion', blank=True, null=True)
    identificacion = models.CharField(max_length=45, blank=True, null=True)
    nombre = models.CharField(max_length=45, blank=True, null=True)
    apellido = models.CharField(max_length=45, blank=True, null=True)
    direccion = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=45, blank=True, null=True)
    telefono = models.CharField(max_length=45, blank=True, null=True)
    id_municipio = models.ForeignKey(Municipio, models.DO_NOTHING, db_column='id_municipio', blank=True, null=True)
    razon_social = models.CharField(max_length=45, blank=True, null=True)
    
    # Flags/Roles
    es_cliente = models.CharField(max_length=1, default='N')
    es_proveedor = models.CharField(max_length=1, default='N')
    es_empleado = models.CharField(max_length=1, default='N')
    es_usuario = models.CharField(max_length=1, default='N')
    
    # Auth
    # Map 'password' field of AbstractBaseUser to 'clave' column
    password = models.CharField(max_length=45, db_column='clave', blank=True, null=True)
    usuario = models.CharField(unique=True, max_length=45, blank=True, null=True)
    last_login = None # Legacy table likely doesn't have last_login, or we need to add it/ignore it.
    # If we inherit AbstractBaseUser, it expects last_login. 
    # If legacy DB can't change, we must ignore it or map to a dummy.
    # Set managed='False' means we can't add columns.
    # We can try to use a non-field for last_login or just accept it's missing (will error on save).
    # For reading, it's fine. For login, update_last_login updates it.
    # We should disable update_last_login signal if column missing.
    
    # Meta data
    id_tercero_registra = models.IntegerField(blank=True, null=True)
    fch_registro = models.DateTimeField(auto_now_add=True)
    ejecuta_labor_tecnica = models.CharField(max_length=1, default='N')
    super_usuario = models.CharField(max_length=1, default='N')
    estado = models.CharField(max_length=1, default='A')

    objects = TerceroManager()

    USERNAME_FIELD = 'usuario'
    REQUIRED_FIELDS = []
    
    # Disable last_login if not in legacy DB
    last_login = None

    class Meta:
        managed = False
        db_table = 'tercero'

    def __str__(self):
        return f"{self.nombre} {self.apellido}" if self.nombre else self.razon_social or self.usuario

    @property
    def is_staff(self):
        # 'S' indicates superuser/staff in legacy system
        return self.super_usuario == 'S'

    @property
    def is_superuser(self):
        return self.super_usuario == 'S'

    @property
    def is_active(self):
        return self.estado == 'A'

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

class TipoLuminaria(models.Model):
    id_tipo_luminaria = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=45)
    potencia = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipo_luminaria'

    def __str__(self):
        return self.descripcion

class EstadoLuminaria(models.Model):
    id_estado_luminaria = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'estado_luminaria'

    def __str__(self):
        return self.descripcion

class Luminaria(models.Model):
    id_luminaria = models.AutoField(primary_key=True)
    poste_no = models.CharField(max_length=45)
    luminaria_no = models.CharField(max_length=45, blank=True, null=True)
    id_tipo_luminaria = models.ForeignKey(TipoLuminaria, models.DO_NOTHING, db_column='id_tipo_luminaria', blank=True, null=True)
    id_municipio = models.ForeignKey(Municipio, models.DO_NOTHING, db_column='id_municipio')
    direccion = models.CharField(max_length=45)
    id_barrio = models.ForeignKey(Barrio, models.DO_NOTHING, db_column='id_barrio')
    latitud = models.DecimalField(max_digits=16, decimal_places=13)
    longitud = models.DecimalField(max_digits=16, decimal_places=13)
    id_tercero = models.ForeignKey(Tercero, models.DO_NOTHING, db_column='id_tercero', blank=True, null=True, db_comment='Técnico Instalador')
    referencia = models.CharField(max_length=45, blank=True, null=True)
    id_estado_luminaria = models.ForeignKey(EstadoLuminaria, models.DO_NOTHING, db_column='id_estado_luminaria')
    fch_registro = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'luminaria'

    def __str__(self):
        return f"Lum {self.luminaria_no} (Poste {self.poste_no})"

class TipoActividad(models.Model):
    id_tipo_actividad = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=45)
    instalacion = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'tipo_actividad'

    def __str__(self):
        return self.descripcion

class Articulo(models.Model):
    id_articulo = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=150)
    clase = models.CharField(max_length=1, db_comment='S:SERVICIO M:MATERIAL')

    class Meta:
        managed = False
        db_table = 'articulo'

    def __str__(self):
        return self.descripcion

class EstadoActividad(models.Model):
    id_estado_actividad = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'estado_actividad'

    def __str__(self):
        return self.descripcion

class UnidadMedida(models.Model):
    id_unitario = models.AutoField(primary_key=True, db_column='id_unidad_medida')
    descripcion = models.CharField(max_length=50)
    abreviatura = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'unidad_medida'

    def __str__(self):
        return self.descripcion

class Vehiculo(models.Model):
    id_vehiculo = models.AutoField(primary_key=True)
    placa = models.CharField(max_length=20, blank=True, null=True)
    descripcion = models.CharField(max_length=45)
    estado = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'vehiculo'

    def __str__(self):
        return f"{self.placa} - {self.descripcion}"

class Actividad(models.Model):
    id_actividad = models.AutoField(primary_key=True)
    id_luminaria = models.ForeignKey(Luminaria, models.DO_NOTHING, db_column='id_luminaria', blank=True, null=True)
    id_municipio = models.ForeignKey(Municipio, models.DO_NOTHING, db_column='id_municipio')
    id_barrio = models.ForeignKey(Barrio, models.DO_NOTHING, db_column='id_barrio', blank=True, null=True)
    barrio = models.CharField(max_length=80, blank=True, null=True)
    id_tipo_actividad = models.ForeignKey(TipoActividad, models.DO_NOTHING, db_column='id_tipo_actividad')
    id_tercero = models.ForeignKey(Tercero, models.DO_NOTHING, db_column='id_tercero', blank=True, null=True)
    id_estado_actividad = models.ForeignKey(EstadoActividad, models.DO_NOTHING, db_column='id_estado_actividad', related_name='actividades')
    id_vehiculo = models.ForeignKey(Vehiculo, models.DO_NOTHING, db_column='id_vehiculo', blank=True, null=True)
    id_tipo_reporte = models.ForeignKey('TipoReporte', models.DO_NOTHING, db_column='id_tipo_reporte', blank=True, null=True)
    
    direccion = models.CharField(max_length=80)
    fch_actividad = models.DateTimeField()
    fch_reporte = models.DateTimeField(blank=True, null=True)
    fch_ejecucion_actividad = models.DateField(blank=True, null=True)
    hora_ejecucion_actividad = models.TimeField(blank=True, null=True)
    
    observacion = models.TextField(blank=True, null=True)
    latitud = models.DecimalField(max_digits=16, decimal_places=13, default=0)
    longitud = models.DecimalField(max_digits=16, decimal_places=13, default=0)
    seq = models.IntegerField(blank=True, null=True)
    
    # Relation to PQR
    id_pqr = models.ForeignKey('Pqr', models.DO_NOTHING, db_column='id_pqr', blank=True, null=True)
    id_tercero_registra = models.ForeignKey(Tercero, models.DO_NOTHING, db_column='id_tercero_registra', related_name='actividades_registradas', blank=True, null=True)
    fch_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'actividad'

    def __str__(self):
        return f"Actividad {self.id_actividad} - {self.direccion}"

class ActividadMobile(models.Model):
    """Auxiliary table for new mobile features to avoid legacy schema changes"""
    id_actividad = models.OneToOneField(Actividad, on_delete=models.CASCADE, primary_key=True, related_name='mobile_data')
    fch_inicio = models.DateTimeField(blank=True, null=True)
    latitud_inicio = models.DecimalField(max_digits=16, decimal_places=13, blank=True, null=True)
    longitud_inicio = models.DecimalField(max_digits=16, decimal_places=13, blank=True, null=True)
    
    class Meta:
        db_table = 'actividad_mobile'

class ActividadMaterial(models.Model):
    id_actividad_material = models.AutoField(primary_key=True)
    id_actividad = models.ForeignKey(Actividad, models.CASCADE, related_name='materiales')
    id_articulo = models.ForeignKey(Articulo, models.DO_NOTHING)
    id_unidad_medida = models.ForeignKey(UnidadMedida, models.DO_NOTHING, db_column='id_unidad_medida', blank=True, null=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    serial = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=[('INSTALADO', 'Instalado'), ('DESMONTADO', 'Desmontado')])

    class Meta:
        db_table = 'actividad_material' # New table for enriched data

class ActividadFoto(models.Model):
    id_actividad_foto = models.AutoField(primary_key=True)
    id_actividad = models.ForeignKey(Actividad, models.CASCADE, related_name='fotos')
    foto = models.ImageField(upload_to='actividades/fotos/')
    tipo = models.CharField(max_length=10, choices=[('ANTES', 'Antes'), ('DESPUES', 'Después')])
    fch_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'actividad_foto'

class ActividadFirma(models.Model):
    id_actividad_firma = models.AutoField(primary_key=True)
    id_actividad = models.OneToOneField(Actividad, models.CASCADE, related_name='firma')
    nombre_firmante = models.CharField(max_length=100)
    firma_base64 = models.TextField() # Signature as base64 string
    fch_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'actividad_firma'

class TipoPqr(models.Model):
    id_tipo_pqr = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=45)
    dias_vencimiento = models.IntegerField()
    estado = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'tipo_pqr'

    def __str__(self):
        return self.descripcion

class TipoReporte(models.Model):
    id_tipo_reporte = models.AutoField(primary_key=True)
    id_tipo_pqr = models.ForeignKey(TipoPqr, models.DO_NOTHING, db_column='id_tipo_pqr', blank=True, null=True)
    descripcion = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'tipo_reporte'

    def __str__(self):
        return self.descripcion

class MedioRecepcionPqr(models.Model):
    id_medio_recepcion_pqr = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'medio_recepcion_pqr'

    def __str__(self):
        return self.descripcion

class EstadoPqr(models.Model):
    id_estado_pqr = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=45)
    permitir_edicion = models.CharField(max_length=1)
    permitir_eliminar = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'estado_pqr'

    def __str__(self):
        return self.descripcion

class Pqr(models.Model):
    id_pqr = models.AutoField(primary_key=True)
    id_municipio = models.ForeignKey(Municipio, models.DO_NOTHING, db_column='id_municipio')
    id_tipo_pqr = models.ForeignKey(TipoPqr, models.DO_NOTHING, db_column='id_tipo_pqr')
    id_tipo_reporte = models.ForeignKey(TipoReporte, models.DO_NOTHING, db_column='id_tipo_reporte')
    id_medio_recepcion_pqr = models.ForeignKey(MedioRecepcionPqr, models.DO_NOTHING, db_column='id_medio_recepcion_pqr')
    # id_usuario_servicio omitted for now or strictly map if needed
    id_luminaria = models.ForeignKey(Luminaria, models.DO_NOTHING, db_column='id_luminaria', blank=True, null=True)
    comentario = models.TextField()
    id_tercero_registra = models.ForeignKey(Tercero, models.DO_NOTHING, db_column='id_tercero_registra')
    fch_registro = models.DateTimeField()
    fch_pqr = models.DateField()
    id_estado_pqr = models.ForeignKey(EstadoPqr, models.DO_NOTHING, db_column='id_estado_pqr')
    fch_cierre = models.DateTimeField(blank=True, null=True)
    id_tercero_cierra = models.ForeignKey(Tercero, models.DO_NOTHING, db_column='id_tercero_cierra', related_name='pqr_cierra_set', blank=True, null=True)
    
    # Report info
    direccion_reporte = models.CharField(max_length=80, blank=True, null=True)
    nombre_usuario_servicio = models.CharField(max_length=80, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'pqr'

    def __str__(self):
        return f"PQR {self.id_pqr} - {self.id_tipo_pqr}"
