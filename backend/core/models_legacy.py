# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Actividad(models.Model):
    id_actividad = models.AutoField(primary_key=True)
    id_luminaria = models.ForeignKey('Luminaria', models.DO_NOTHING, db_column='id_luminaria', blank=True, null=True)
    id_municipio = models.ForeignKey('Municipio', models.DO_NOTHING, db_column='id_municipio')
    id_barrio = models.ForeignKey('Barrio', models.DO_NOTHING, db_column='id_barrio', blank=True, null=True)
    barrio = models.CharField(max_length=80, blank=True, null=True)
    id_tipo_actividad = models.ForeignKey('TipoActividad', models.DO_NOTHING, db_column='id_tipo_actividad', db_comment='Tipo de Actividad Ejecutada')
    id_tercero = models.ForeignKey('Tercero', models.DO_NOTHING, db_column='id_tercero', blank=True, null=True)
    id_tipo_reporte = models.ForeignKey('TipoReporte', models.DO_NOTHING, db_column='id_tipo_reporte', blank=True, null=True, db_comment='Se llena con el reportado en la PQR')
    id_estado_actividad = models.ForeignKey('TipoActividad', models.DO_NOTHING, db_column='id_estado_actividad', related_name='actividad_id_estado_actividad_set')
    direccion = models.CharField(max_length=80)
    fch_actividad = models.DateTimeField()
    fch_reporte = models.DateTimeField(blank=True, null=True, db_comment='se llena con la fecha de la PQR')
    observacion = models.TextField(blank=True, null=True)
    latitud = models.DecimalField(max_digits=16, decimal_places=13)
    longitud = models.DecimalField(max_digits=16, decimal_places=13)
    seq = models.IntegerField(blank=True, null=True)
    id_pqr = models.ForeignKey('Pqr', models.DO_NOTHING, db_column='id_pqr', blank=True, null=True)
    id_tercero_registra = models.ForeignKey('Tercero', models.DO_NOTHING, db_column='id_tercero_registra', related_name='actividad_id_tercero_registra_set', blank=True, null=True)
    fch_registro = models.DateTimeField(blank=True, null=True)
    id_vehiculo = models.ForeignKey('Vehiculo', models.DO_NOTHING, db_column='id_vehiculo', blank=True, null=True)
    id_tipo_luminaria = models.ForeignKey('TipoLuminaria', models.DO_NOTHING, db_column='id_tipo_luminaria', blank=True, null=True)
    ot_anterior = models.CharField(max_length=50, blank=True, null=True)
    fch_ejecucion_actividad = models.DateField(blank=True, null=True)
    hora_ejecucion_actividad = models.TimeField(blank=True, null=True)
    fch_programacion = models.DateField(blank=True, null=True)
    fch_retroalimentacion = models.DateTimeField(blank=True, null=True)
    id_luminaria_retirada_modernizacion = models.IntegerField(blank=True, null=True)
    id_usuario_retroalimenta = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'actividad'


class ArchivoPqr(models.Model):
    id_archivo_pqr = models.AutoField(primary_key=True)
    id_pqr = models.ForeignKey('Pqr', models.DO_NOTHING, db_column='id_pqr')
    tipo = models.CharField(max_length=45)
    tamano = models.IntegerField()
    extension = models.CharField(max_length=45)
    nombre_archivo = models.CharField(max_length=45)
    archivo = models.TextField()
    id_tercero_registra = models.ForeignKey('Tercero', models.DO_NOTHING, db_column='id_tercero_registra')
    fch_registro = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'archivo_pqr'


class Articulo(models.Model):
    id_articulo = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=150)
    clase = models.CharField(max_length=1, db_comment='S:SERVICIO M:MATERIAL')

    class Meta:
        managed = False
        db_table = 'articulo'


class ArticuloActividad(models.Model):
    id_actividad = models.OneToOneField(Actividad, models.DO_NOTHING, db_column='id_actividad', primary_key=True)  # The composite primary key (id_actividad, id_articulo) found, that is not supported. The first column is selected.
    id_articulo = models.ForeignKey(Articulo, models.DO_NOTHING, db_column='id_articulo')
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'articulo_actividad'
        unique_together = (('id_actividad', 'id_articulo'),)


class Barrio(models.Model):
    id_barrio = models.AutoField(primary_key=True)
    id_municipio = models.ForeignKey('Municipio', models.DO_NOTHING, db_column='id_municipio')
    descripcion = models.CharField(max_length=80)

    class Meta:
        managed = False
        db_table = 'barrio'
        db_table_comment = 'Barrios y Corregimiento de los Municipio'


class ClaseIluminacion(models.Model):
    id_clase_iluminacion = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'clase_iluminacion'


class ComentarioPqr(models.Model):
    id_comentario_pqr = models.AutoField(primary_key=True)
    id_pqr = models.ForeignKey('Pqr', models.DO_NOTHING, db_column='id_pqr')
    id_tercero = models.ForeignKey('Tercero', models.DO_NOTHING, db_column='id_tercero')
    comentario = models.TextField()
    fch_registro = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'comentario_pqr'


class Configuracion(models.Model):
    id_configuracion = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(max_length=100, blank=True, null=True)
    ruta_logo = models.CharField(max_length=100, blank=True, null=True)
    tema = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    nit = models.CharField(max_length=50, blank=True, null=True)
    representante_legal = models.CharField(max_length=100, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'configuracion'


class Departamento(models.Model):
    id_departamento = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'departamento'


class EstadoActividad(models.Model):
    id_estado_actividad = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'estado_actividad'


class EstadoLuminaria(models.Model):
    id_estado_luminaria = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'estado_luminaria'


class EstadoPqr(models.Model):
    id_estado_pqr = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=45)
    permitir_edicion = models.CharField(max_length=1)
    permitir_eliminar = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'estado_pqr'


class Luminaria(models.Model):
    id_luminaria = models.AutoField(primary_key=True)
    poste_no = models.CharField(max_length=45)
    luminaria_no = models.CharField(max_length=45, blank=True, null=True)
    id_tipo_luminaria = models.ForeignKey('TipoLuminaria', models.DO_NOTHING, db_column='id_tipo_luminaria', blank=True, null=True)
    id_municipio = models.ForeignKey('Municipio', models.DO_NOTHING, db_column='id_municipio')
    direccion = models.CharField(max_length=45)
    id_barrio = models.ForeignKey(Barrio, models.DO_NOTHING, db_column='id_barrio')
    latitud = models.DecimalField(max_digits=16, decimal_places=13)
    longitud = models.DecimalField(max_digits=16, decimal_places=13)
    id_tercero = models.ForeignKey('Tercero', models.DO_NOTHING, db_column='id_tercero', blank=True, null=True, db_comment='Técnico Instalador')
    referencia = models.CharField(max_length=45, blank=True, null=True)
    propiedad_poste = models.CharField(max_length=50, blank=True, null=True)
    id_tipo_poste = models.IntegerField(blank=True, null=True)
    id_norma_tipo_poste = models.IntegerField(blank=True, null=True)
    id_tipo_brazo = models.IntegerField(blank=True, null=True)
    id_marca_luminaria = models.IntegerField(blank=True, null=True)
    zona = models.CharField(max_length=50, blank=True, null=True)
    nodo = models.CharField(max_length=50, blank=True, null=True)
    transformador_no = models.CharField(max_length=50, blank=True, null=True)
    potencia_transformador = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    id_propiedad_transformador = models.IntegerField(blank=True, null=True)
    potencia = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    fch_instalacion = models.DateField(blank=True, null=True)
    fch_registro = models.DateTimeField()
    id_tercero_registra = models.IntegerField(db_comment='Usuario del sistema quien realiza el registro de la luminaria')
    id_estado_luminaria = models.ForeignKey(EstadoLuminaria, models.DO_NOTHING, db_column='id_estado_luminaria')
    id_tercero_proveedor = models.IntegerField(blank=True, null=True, db_comment='Proveedor de la luminaria')
    id_periodo_mantenimiento = models.IntegerField(blank=True, null=True)
    fch_actualizacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'luminaria'


class MarcaLuminaria(models.Model):
    id_marca_luminaria = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'marca_luminaria'


class MedioRecepcionPqr(models.Model):
    id_medio_recepcion_pqr = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'medio_recepcion_pqr'


class Menu(models.Model):
    id_menu = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    ruta_pagina = models.CharField(max_length=80, blank=True, null=True)
    ejecutable = models.CharField(max_length=1)
    id_menu_padre = models.IntegerField(blank=True, null=True)
    descripcion = models.CharField(max_length=45)
    orden = models.IntegerField()
    icono = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'menu'


class MenuTercero(models.Model):
    id_menu = models.IntegerField(primary_key=True)  # The composite primary key (id_menu, id_tercero) found, that is not supported. The first column is selected.
    id_tercero = models.IntegerField()
    crear = models.CharField(max_length=1)
    actualizar = models.CharField(max_length=1)
    eliminar = models.CharField(max_length=1)
    imprimir = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'menu_tercero'
        unique_together = (('id_menu', 'id_tercero'),)


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


class NormaPoste(models.Model):
    id_norma_poste = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)
    altura = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'norma_poste'


class NormaTipoPoste(models.Model):
    id_norma_tipo_poste = models.AutoField(primary_key=True)
    id_tipo_poste = models.ForeignKey('TipoPoste', models.DO_NOTHING, db_column='id_tipo_poste')
    descripcion = models.CharField(max_length=100)
    estado = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'norma_tipo_poste'


class PeriodoMantenimiento(models.Model):
    id_periodo_mantenimiento = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)
    dias = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'periodo_mantenimiento'


class Pqr(models.Model):
    id_pqr = models.AutoField(primary_key=True)
    id_municipio = models.ForeignKey(Municipio, models.DO_NOTHING, db_column='id_municipio')
    id_tipo_pqr = models.ForeignKey('TipoPqr', models.DO_NOTHING, db_column='id_tipo_pqr')
    id_tipo_reporte = models.ForeignKey('TipoReporte', models.DO_NOTHING, db_column='id_tipo_reporte')
    id_medio_recepcion_pqr = models.ForeignKey(MedioRecepcionPqr, models.DO_NOTHING, db_column='id_medio_recepcion_pqr')
    id_usuario_servicio = models.ForeignKey('UsuarioServicio', models.DO_NOTHING, db_column='id_usuario_servicio', blank=True, null=True)
    id_luminaria = models.ForeignKey(Luminaria, models.DO_NOTHING, db_column='id_luminaria', blank=True, null=True)
    comentario = models.TextField()
    id_tercero_registra = models.ForeignKey('Tercero', models.DO_NOTHING, db_column='id_tercero_registra')
    fch_registro = models.DateTimeField()
    fch_pqr = models.DateField()
    id_estado_pqr = models.ForeignKey(EstadoPqr, models.DO_NOTHING, db_column='id_estado_pqr')
    fch_cierre = models.DateTimeField(blank=True, null=True)
    id_tercero_cierra = models.ForeignKey('Tercero', models.DO_NOTHING, db_column='id_tercero_cierra', related_name='pqr_id_tercero_cierra_set', blank=True, null=True)
    id_barrio_reporte = models.IntegerField(blank=True, null=True)
    direccion_reporte = models.CharField(max_length=80, blank=True, null=True)
    nombre_usuario_servicio = models.CharField(max_length=80, blank=True, null=True)
    direccion_usuario_servicio = models.CharField(max_length=80, blank=True, null=True)
    telefono_usuario_servicio = models.CharField(max_length=45, blank=True, null=True)
    apoyo_no = models.CharField(max_length=50, blank=True, null=True)
    hora_pqr = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pqr'


class PropiedadTransformador(models.Model):
    id_propiedad_transformador = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'propiedad_transformador'


class Tercero(models.Model):
    id_tercero = models.AutoField(primary_key=True)
    id_tipo_identificacion = models.ForeignKey('TipoIdentificacion', models.DO_NOTHING, db_column='id_tipo_identificacion')
    identificacion = models.CharField(max_length=45)
    nombre = models.CharField(max_length=45, blank=True, null=True)
    apellido = models.CharField(max_length=45, blank=True, null=True)
    direccion = models.CharField(max_length=45)
    email = models.CharField(max_length=45, blank=True, null=True)
    telefono = models.CharField(max_length=45, blank=True, null=True)
    id_municipio = models.ForeignKey(Municipio, models.DO_NOTHING, db_column='id_municipio')
    razon_social = models.CharField(max_length=45, blank=True, null=True)
    es_cliente = models.CharField(max_length=1)
    es_proveedor = models.CharField(max_length=1)
    es_empleado = models.CharField(max_length=1)
    es_usuario = models.CharField(max_length=1)
    clave = models.CharField(max_length=45, blank=True, null=True)
    usuario = models.CharField(unique=True, max_length=45, blank=True, null=True)
    id_tercero_registra = models.IntegerField(blank=True, null=True)
    fch_registro = models.DateTimeField()
    ejecuta_labor_tecnica = models.CharField(max_length=1)
    super_usuario = models.CharField(max_length=1)
    tipo_foto = models.CharField(max_length=45, blank=True, null=True)
    tamano_foto = models.IntegerField(blank=True, null=True)
    extension_foto = models.CharField(max_length=45, blank=True, null=True)
    nombre_foto = models.CharField(max_length=45, blank=True, null=True)
    foto = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'tercero'


class TipoActividad(models.Model):
    id_tipo_actividad = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=45)
    instalacion = models.CharField(max_length=1)
    preventivo = models.CharField(max_length=1, blank=True, null=True)
    correctivo = models.CharField(max_length=1, blank=True, null=True)
    reubicacion = models.CharField(max_length=1, blank=True, null=True)
    desmonte = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipo_actividad'


class TipoBrazo(models.Model):
    id_tipo_brazo = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tipo_brazo'


class TipoIdentificacion(models.Model):
    id_tipo_identificacion = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=45)
    abreviatura = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = 'tipo_identificacion'


class TipoLuminaria(models.Model):
    id_tipo_luminaria = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=45)
    potencia = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipo_luminaria'


class TipoPoste(models.Model):
    id_tipo_poste = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tipo_poste'


class TipoPqr(models.Model):
    id_tipo_pqr = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=45)
    dias_vencimiento = models.IntegerField()
    estado = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'tipo_pqr'


class TipoReporte(models.Model):
    id_tipo_reporte = models.AutoField(primary_key=True)
    id_tipo_pqr = models.ForeignKey(TipoPqr, models.DO_NOTHING, db_column='id_tipo_pqr', blank=True, null=True)
    descripcion = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'tipo_reporte'


class TmpCorrectivoAgosto(models.Model):
    dias_apagados = models.CharField(db_column='DIAS_APAGADOS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fecha_reclamo = models.DateField(db_column='FECHA_RECLAMO', blank=True, null=True)  # Field name made lowercase.
    fecha_revision = models.DateField(db_column='FECHA_REVISION', blank=True, null=True)  # Field name made lowercase.
    municipio = models.CharField(db_column='MUNICIPIO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    barrio = models.CharField(db_column='BARRIO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='DIRECCION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    observacion = models.CharField(db_column='OBSERVACION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    descripcion_solicitud = models.CharField(db_column='DESCRIPCION_SOLICITUD', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tipo_luminaria = models.CharField(db_column='TIPO_LUMINARIA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    codigo_luminaria = models.CharField(db_column='CODIGO_LUMINARIA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    numero_poste = models.CharField(db_column='NUMERO_POSTE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    coordenadas = models.CharField(db_column='COORDENADAS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tecnico = models.CharField(db_column='TECNICO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    potencia = models.CharField(db_column='POTENCIA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cambio_arrancador_de_70 = models.CharField(db_column='CAMBIO ARRANCADOR DE 70', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_arrancador_de_100_400 = models.CharField(db_column='CAMBIO ARRANCADOR DE 100 400', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_balasto70 = models.CharField(db_column='CAMBIO DE BALASTO70', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_balasto_150 = models.CharField(db_column='CAMBIO DE BALASTO 150', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_balasto_250 = models.CharField(db_column='CAMBIO DE BALASTO 250', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_balasto_400 = models.CharField(db_column='CAMBIO DE BALASTO 400', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_balasto_1000 = models.CharField(db_column='CAMBIO DE BALASTO 1000', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    reconexion_a_la_red = models.CharField(db_column='RECONEXION A LA RED', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    reparacion_de_conexiones_internas = models.CharField(db_column='REPARACION DE CONEXIONES INTERNAS', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_fotocelda_de_220 = models.CharField(db_column='CAMBIO DE FOTOCELDA DE 220', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    base_de_foto_celda = models.CharField(db_column='BASE DE FOTO CELDA', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_condensador_de_10 = models.CharField(db_column='CAMBIO DE CONDENSADOR DE 10', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_condensador_de_20 = models.CharField(db_column='CAMBIO DE CONDENSADOR DE 20', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_condensador_de_24 = models.CharField(db_column='CAMBIO DE CONDENSADOR DE 24', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_condensador_de_30 = models.CharField(db_column='CAMBIO DE CONDENSADOR DE 30', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_condensador_de_35 = models.CharField(db_column='CAMBIO DE CONDENSADOR DE 35', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_condensador_de_45 = models.CharField(db_column='CAMBIO DE CONDENSADOR DE 45', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_brazo = models.CharField(db_column='CAMBIO DE BRAZO', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    instalacion_de_nueva_luminaria = models.CharField(db_column='INSTALACION DE NUEVA LUMINARIA', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    tendido_de_red = models.CharField(db_column='TENDIDO DE RED', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    leds_de_45w = models.CharField(db_column='LEDs DE 45W', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    leds_de_170w = models.CharField(db_column='LEDs DE 170W', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    reflectores_de_150 = models.CharField(db_column='REFLECTORES DE 150', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    reflectores_de_250 = models.CharField(db_column='REFLECTORES DE 250', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    reflectores_de_400 = models.CharField(db_column='REFLECTORES DE 400', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    soporte_rosca_e_27 = models.CharField(db_column='SOPORTE ROSCA E 27', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    soporte_rosca_e_40 = models.CharField(db_column='SOPORTE ROSCA E 40', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    conectores_de_regletas = models.CharField(db_column='CONECTORES DE REGLETAS', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    conectores_de_kz = models.CharField(db_column='CONECTORES DE KZ', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    conectores_2_a_2 = models.CharField(db_column='CONECTORES 2 A 2', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    alambre_n_14 = models.CharField(db_column='ALAMBRE N 14', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cable_n_4 = models.CharField(db_column='CABLE N 4', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cable_n_6 = models.CharField(db_column='CABLE N 6', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cable_3_14 = models.CharField(db_column='CABLE 3 14', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    id_municipio = models.IntegerField(blank=True, null=True)
    id_barrio = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tmp_correctivo_agosto'


class TmpCorrectivoJulio(models.Model):
    dias_apagados = models.CharField(db_column='DIAS_APAGADOS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fecha_reclamo = models.DateField(db_column='FECHA_RECLAMO', blank=True, null=True)  # Field name made lowercase.
    fecha_revision = models.DateField(db_column='FECHA_REVISION', blank=True, null=True)  # Field name made lowercase.
    municipio = models.CharField(db_column='MUNICIPIO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    barrio = models.CharField(db_column='BARRIO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='DIRECCION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    observacion = models.CharField(db_column='OBSERVACION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    descripcion_solicitud = models.CharField(db_column='DESCRIPCION_SOLICITUD', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tipo_luminaria = models.CharField(db_column='TIPO_LUMINARIA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    codigo_luminaria = models.CharField(db_column='CODIGO_LUMINARIA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    numero_poste = models.CharField(db_column='NUMERO_POSTE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    coordenadas = models.CharField(db_column='COORDENADAS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tecnico = models.CharField(db_column='TECNICO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    potencia = models.CharField(db_column='POTENCIA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cambio_arrancador_de_70 = models.CharField(db_column='CAMBIO ARRANCADOR DE 70', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_arrancador_de_100_400 = models.CharField(db_column='CAMBIO ARRANCADOR DE 100 400', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_balasto70 = models.CharField(db_column='CAMBIO DE BALASTO70', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_balasto_150 = models.CharField(db_column='CAMBIO DE BALASTO 150', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_balasto_250 = models.CharField(db_column='CAMBIO DE BALASTO 250', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_balasto_400 = models.CharField(db_column='CAMBIO DE BALASTO 400', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_balasto_1000 = models.CharField(db_column='CAMBIO DE BALASTO 1000', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    reconexion_a_la_red = models.CharField(db_column='RECONEXION A LA RED', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    reparacion_de_conexiones_internas = models.CharField(db_column='REPARACION DE CONEXIONES INTERNAS', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_fotocelda_de_220 = models.CharField(db_column='CAMBIO DE FOTOCELDA DE 220', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    base_de_foto_celda = models.CharField(db_column='BASE DE FOTO CELDA', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_condensador_de_10 = models.CharField(db_column='CAMBIO DE CONDENSADOR DE 10', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_condensador_de_20 = models.CharField(db_column='CAMBIO DE CONDENSADOR DE 20', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_condensador_de_24 = models.CharField(db_column='CAMBIO DE CONDENSADOR DE 24', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_condensador_de_30 = models.CharField(db_column='CAMBIO DE CONDENSADOR DE 30', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_condensador_de_35 = models.CharField(db_column='CAMBIO DE CONDENSADOR DE 35', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_condensador_de_45 = models.CharField(db_column='CAMBIO DE CONDENSADOR DE 45', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_brazo = models.CharField(db_column='CAMBIO_BRAZO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    instalacion_de_nueva_luminaria = models.CharField(db_column='INSTALACION DE NUEVA LUMINARIA', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    tendido_de_red = models.CharField(db_column='TENDIDO DE RED', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    leds_de_45w = models.CharField(db_column='LEDs DE 45W', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    leds_de_170w = models.CharField(db_column='LEDs DE 170W', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    reflectores_de_150 = models.CharField(db_column='REFLECTORES DE 150', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    reflectores_de_250 = models.CharField(db_column='REFLECTORES DE 250', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    reflectores_de_400 = models.CharField(db_column='REFLECTORES DE 400', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    soporte_rosca_e_27 = models.CharField(db_column='SOPORTE ROSCA E 27', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    soporte_rosca_e_40 = models.CharField(db_column='SOPORTE ROSCA E 40', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    conectores_de_regletas = models.CharField(db_column='CONECTORES DE REGLETAS', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    conectores_de_kz = models.CharField(db_column='CONECTORES DE KZ', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    conectores_2_2 = models.CharField(db_column='CONECTORES_2 _2', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    alambre_n_14 = models.CharField(db_column='ALAMBRE N_14', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cable_n_4 = models.CharField(db_column='CABLE N_4', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cable_n_6 = models.CharField(db_column='CABLE N_6', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cable_3_14 = models.CharField(db_column='CABLE 3*14', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    id_municipio = models.IntegerField(blank=True, null=True)
    id_barrio = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tmp_correctivo_julio'


class TmpCorrectivoJulio2(models.Model):
    dias_apagados = models.CharField(db_column='DIAS_APAGADOS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fecha_reclamo = models.DateField(db_column='FECHA_RECLAMO', blank=True, null=True)  # Field name made lowercase.
    fecha_revision = models.DateField(db_column='FECHA_REVISION', blank=True, null=True)  # Field name made lowercase.
    municipio = models.CharField(db_column='MUNICIPIO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    barrio = models.CharField(db_column='BARRIO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='DIRECCION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    observacion = models.CharField(db_column='OBSERVACION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    descripcion_solicitud = models.CharField(db_column='DESCRIPCION_SOLICITUD', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tipo_luminaria = models.CharField(db_column='TIPO_LUMINARIA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    codigo_luminaria = models.CharField(db_column='CODIGO_LUMINARIA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    numero_poste = models.CharField(db_column='NUMERO_POSTE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    coordenadas = models.CharField(db_column='COORDENADAS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tecnico = models.CharField(db_column='TECNICO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    potencia = models.CharField(db_column='POTENCIA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cambio_arrancador_de_70 = models.CharField(db_column='CAMBIO ARRANCADOR DE 70', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_arrancador_de_100_400 = models.CharField(db_column='CAMBIO ARRANCADOR DE 100 400', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_balasto70 = models.CharField(db_column='CAMBIO DE BALASTO70', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_balasto_150 = models.CharField(db_column='CAMBIO DE BALASTO 150', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_balasto_250 = models.CharField(db_column='CAMBIO DE BALASTO 250', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_balasto_400 = models.CharField(db_column='CAMBIO DE BALASTO 400', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_balasto_1000 = models.CharField(db_column='CAMBIO DE BALASTO 1000', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    reconexion_a_la_red = models.CharField(db_column='RECONEXION A LA RED', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    reparacion_de_conexiones_internas = models.CharField(db_column='REPARACION DE CONEXIONES INTERNAS', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_fotocelda_de_220 = models.CharField(db_column='CAMBIO DE FOTOCELDA DE 220', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    base_de_foto_celda = models.CharField(db_column='BASE DE FOTO CELDA', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_condensador_de_10 = models.CharField(db_column='CAMBIO DE CONDENSADOR DE 10', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_condensador_de_20 = models.CharField(db_column='CAMBIO DE CONDENSADOR DE 20', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_condensador_de_24 = models.CharField(db_column='CAMBIO DE CONDENSADOR DE 24', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_condensador_de_30 = models.CharField(db_column='CAMBIO DE CONDENSADOR DE 30', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_condensador_de_35 = models.CharField(db_column='CAMBIO DE CONDENSADOR DE 35', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_condensador_de_45 = models.CharField(db_column='CAMBIO DE CONDENSADOR DE 45', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_brazo = models.CharField(db_column='CAMBIO_BRAZO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    instalacion_de_nueva_luminaria = models.CharField(db_column='INSTALACION DE NUEVA LUMINARIA', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    tendido_de_red = models.CharField(db_column='TENDIDO DE RED', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    leds_de_45w = models.CharField(db_column='LEDs DE 45W', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    leds_de_170w = models.CharField(db_column='LEDs DE 170W', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    reflectores_de_150 = models.CharField(db_column='REFLECTORES DE 150', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    reflectores_de_250 = models.CharField(db_column='REFLECTORES DE 250', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    reflectores_de_400 = models.CharField(db_column='REFLECTORES DE 400', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    soporte_rosca_e_27 = models.CharField(db_column='SOPORTE ROSCA E 27', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    soporte_rosca_e_40 = models.CharField(db_column='SOPORTE ROSCA E 40', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    conectores_de_regletas = models.CharField(db_column='CONECTORES DE REGLETAS', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    conectores_de_kz = models.CharField(db_column='CONECTORES DE KZ', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    conectores_2_2 = models.CharField(db_column='CONECTORES_2 _2', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    alambre_n_14 = models.CharField(db_column='ALAMBRE N_14', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cable_n_4 = models.CharField(db_column='CABLE N_4', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cable_n_6 = models.CharField(db_column='CABLE N_6', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cable_3_14 = models.CharField(db_column='CABLE 3*14', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    id_municipio = models.IntegerField(blank=True, null=True)
    id_barrio = models.IntegerField(blank=True, null=True)
    seq = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'tmp_correctivo_julio_2'


class TmpCorrectivoJunio(models.Model):
    fecha_reclamo = models.CharField(db_column='FECHA_RECLAMO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fecha_revision = models.CharField(db_column='FECHA_REVISION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    municipio = models.CharField(db_column='MUNICIPIO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    barrio = models.CharField(db_column='BARRIO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='DIRECCION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    descripcionde_solicitud = models.CharField(db_column='DESCRIPCIONDE_SOLICITUD', max_length=255, blank=True, null=True)  # Field name made lowercase.
    codigo_luminaria = models.CharField(db_column='CODIGO_LUMINARIA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    numero_poste = models.CharField(db_column='NUMERO_POSTE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    coordenadas = models.CharField(db_column='COORDENADAS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='TIPO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tecnico = models.CharField(db_column='TECNICO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    potencia = models.CharField(db_column='POTENCIA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cambio_arrancador_de_70 = models.CharField(db_column='CAMBIO_ARRANCADOR_DE_70', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cambio_arrancador_de_100_400 = models.CharField(db_column='CAMBIO_ARRANCADOR_DE_100_400', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cambio_arrancador_de_480 = models.CharField(db_column='CAMBIO_ARRANCADOR_DE_480', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cambio_de_balasto_70 = models.CharField(db_column='CAMBIO_DE_BALASTO_70', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cambio_de_balasto_150 = models.CharField(db_column='CAMBIO_DE_BALASTO_150', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cambio_de_balasto_250 = models.CharField(db_column='CAMBIO_DE_BALASTO_250', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cambio_de_balasto_400 = models.CharField(db_column='CAMBIO_DE_BALASTO_400', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cambio_de_balasto_de_1000 = models.CharField(db_column='CAMBIO_DE_BALASTO_DE_1000', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cambio_de_balasto_115_480 = models.CharField(db_column='CAMBIO_DE_BALASTO_115_480', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cambio_de_balasto_250_480 = models.CharField(db_column='CAMBIO DE BALASTO 250 480', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    reconexio_a_la_red = models.CharField(db_column='RECONEXIO#A LA RED', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    reparacio_de_conexiones_internas = models.CharField(db_column='REPARACIO#DE CONEXIONES INTERNAS', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_fotocelda_de_220 = models.CharField(db_column='CAMBIO DE FOTOCELDA DE 220', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_fotocelda_de_480 = models.CharField(db_column='CAMBIO DE FOTOCELDA DE 480', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    base_de_foto_celda = models.CharField(db_column='BASE DE FOTO CELDA', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    tendido_de_red = models.CharField(db_column='TENDIDO DE RED', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_condensador_de_10 = models.CharField(db_column='CAMBIO DE CONDENSADOR DE 10', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_condensador_de_20 = models.CharField(db_column='CAMBIO DE CONDENSADOR DE 20', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_condensador_de_30 = models.CharField(db_column='CAMBIO DE CONDENSADOR DE 30', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_condensador_de_35 = models.CharField(db_column='CAMBIO DE CONDENSADOR DE 35', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_condensador_de_45 = models.CharField(db_column='CAMBIO DE CONDENSADOR DE 45', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_condensador_de_1000 = models.CharField(db_column='CAMBIO DE CONDENSADOR DE 1000', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_brazo_corto = models.CharField(db_column='CAMBIO DE BRAZO CORTO', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_brazo_largo = models.CharField(db_column='CAMBIO DE BRAZO LARGO', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    instalacio_de_nueva_luminaria_de_45 = models.CharField(db_column='INSTALACIO#DE NUEVA LUMINARIA DE 45', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    instalacio_de_nueva_luminaria_de_150 = models.CharField(db_column='INSTALACIO#DE NUEVA LUMINARIA DE 150', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    instalacio_de_nueva_luminaria_250 = models.CharField(db_column='INSTALACIO#DE NUEVA LUMINARIA 250', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    leds_de_45w = models.CharField(db_column='LEDs DE 45W', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    leds_de_80w = models.CharField(db_column='LEDs DE 80W', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    reflectores_de_150 = models.CharField(db_column='REFLECTORES DE 150', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    reflectores_de_250 = models.CharField(db_column='REFLECTORES DE 250', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    reflectores_de_400 = models.CharField(db_column='REFLECTORES DE 400', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    soporte_rosca_e_27 = models.CharField(db_column='SOPORTE ROSCA E 27', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    soporte_rosca_e_40 = models.CharField(db_column='SOPORTE ROSCA E 40', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    conectores_de_regletas = models.CharField(db_column='CONECTORES DE REGLETAS', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    conectores_kz = models.CharField(db_column='CONECTORES_KZ', max_length=255, blank=True, null=True)  # Field name made lowercase.
    conectores_2_a_2 = models.CharField(db_column='CONECTORES_2_A_2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    alambre_n_4 = models.CharField(db_column='ALAMBRE_N_4', max_length=255, blank=True, null=True)  # Field name made lowercase.
    alambre_n_8 = models.CharField(db_column='ALAMBRE_N_8', max_length=255, blank=True, null=True)  # Field name made lowercase.
    alambre_n_10 = models.CharField(db_column='ALAMBRE_N_10', max_length=255, blank=True, null=True)  # Field name made lowercase.
    alambre_n_12 = models.CharField(db_column='ALAMBRE_N_12', max_length=255, blank=True, null=True)  # Field name made lowercase.
    alambre_n_14 = models.CharField(db_column='ALAMBRE_N_14', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cable_n_2 = models.CharField(db_column='CABLE_N_2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cable_n_4 = models.CharField(db_column='CABLE_N_4', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cable_n_6 = models.CharField(db_column='CABLE_N_6', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cable_2x14 = models.CharField(db_column='CABLE_2X14', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cable_3x14 = models.CharField(db_column='CABLE_3X14', max_length=255, blank=True, null=True)  # Field name made lowercase.
    id_municipio = models.IntegerField(blank=True, null=True)
    id_barrio = models.IntegerField(blank=True, null=True)
    seq = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tmp_correctivo_junio'


class TmpCorrectivoJunio2(models.Model):
    fecha_reclamo = models.CharField(db_column='FECHA_RECLAMO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fecha_revision = models.CharField(db_column='FECHA_REVISION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    municipio = models.CharField(db_column='MUNICIPIO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    barrio = models.CharField(db_column='BARRIO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='DIRECCION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    descripcionde_solicitud = models.CharField(db_column='DESCRIPCIONDE_SOLICITUD', max_length=255, blank=True, null=True)  # Field name made lowercase.
    codigo_luminaria = models.CharField(db_column='CODIGO_LUMINARIA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    numero_poste = models.CharField(db_column='NUMERO_POSTE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    coordenadas = models.CharField(db_column='COORDENADAS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='TIPO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tecnico = models.CharField(db_column='TECNICO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    potencia = models.CharField(db_column='POTENCIA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cambio_arrancador_de_70 = models.CharField(db_column='CAMBIO_ARRANCADOR_DE_70', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cambio_arrancador_de_100_400 = models.CharField(db_column='CAMBIO_ARRANCADOR_DE_100_400', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cambio_arrancador_de_480 = models.CharField(db_column='CAMBIO_ARRANCADOR_DE_480', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cambio_de_balasto_70 = models.CharField(db_column='CAMBIO_DE_BALASTO_70', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cambio_de_balasto_150 = models.CharField(db_column='CAMBIO_DE_BALASTO_150', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cambio_de_balasto_250 = models.CharField(db_column='CAMBIO_DE_BALASTO_250', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cambio_de_balasto_400 = models.CharField(db_column='CAMBIO_DE_BALASTO_400', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cambio_de_balasto_de_1000 = models.CharField(db_column='CAMBIO_DE_BALASTO_DE_1000', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cambio_de_balasto_115_480 = models.CharField(db_column='CAMBIO_DE_BALASTO_115_480', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cambio_de_balasto_250_480 = models.CharField(db_column='CAMBIO DE BALASTO 250 480', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    reconexio_a_la_red = models.CharField(db_column='RECONEXIO#A LA RED', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    reparacio_de_conexiones_internas = models.CharField(db_column='REPARACIO#DE CONEXIONES INTERNAS', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_fotocelda_de_220 = models.CharField(db_column='CAMBIO DE FOTOCELDA DE 220', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_fotocelda_de_480 = models.CharField(db_column='CAMBIO DE FOTOCELDA DE 480', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    base_de_foto_celda = models.CharField(db_column='BASE DE FOTO CELDA', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    tendido_de_red = models.CharField(db_column='TENDIDO DE RED', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_condensador_de_10 = models.CharField(db_column='CAMBIO DE CONDENSADOR DE 10', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_condensador_de_20 = models.CharField(db_column='CAMBIO DE CONDENSADOR DE 20', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_condensador_de_30 = models.CharField(db_column='CAMBIO DE CONDENSADOR DE 30', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_condensador_de_35 = models.CharField(db_column='CAMBIO DE CONDENSADOR DE 35', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_condensador_de_45 = models.CharField(db_column='CAMBIO DE CONDENSADOR DE 45', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_condensador_de_1000 = models.CharField(db_column='CAMBIO DE CONDENSADOR DE 1000', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_brazo_corto = models.CharField(db_column='CAMBIO DE BRAZO CORTO', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cambio_de_brazo_largo = models.CharField(db_column='CAMBIO DE BRAZO LARGO', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    instalacio_de_nueva_luminaria_de_45 = models.CharField(db_column='INSTALACIO#DE NUEVA LUMINARIA DE 45', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    instalacio_de_nueva_luminaria_de_150 = models.CharField(db_column='INSTALACIO#DE NUEVA LUMINARIA DE 150', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    instalacio_de_nueva_luminaria_250 = models.CharField(db_column='INSTALACIO#DE NUEVA LUMINARIA 250', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    leds_de_45w = models.CharField(db_column='LEDs DE 45W', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    leds_de_80w = models.CharField(db_column='LEDs DE 80W', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    reflectores_de_150 = models.CharField(db_column='REFLECTORES DE 150', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    reflectores_de_250 = models.CharField(db_column='REFLECTORES DE 250', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    reflectores_de_400 = models.CharField(db_column='REFLECTORES DE 400', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    soporte_rosca_e_27 = models.CharField(db_column='SOPORTE ROSCA E 27', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    soporte_rosca_e_40 = models.CharField(db_column='SOPORTE ROSCA E 40', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    conectores_de_regletas = models.CharField(db_column='CONECTORES DE REGLETAS', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    conectores_kz = models.CharField(db_column='CONECTORES_KZ', max_length=255, blank=True, null=True)  # Field name made lowercase.
    conectores_2_a_2 = models.CharField(db_column='CONECTORES_2_A_2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    alambre_n_4 = models.CharField(db_column='ALAMBRE_N_4', max_length=255, blank=True, null=True)  # Field name made lowercase.
    alambre_n_8 = models.CharField(db_column='ALAMBRE_N_8', max_length=255, blank=True, null=True)  # Field name made lowercase.
    alambre_n_10 = models.CharField(db_column='ALAMBRE_N_10', max_length=255, blank=True, null=True)  # Field name made lowercase.
    alambre_n_12 = models.CharField(db_column='ALAMBRE_N_12', max_length=255, blank=True, null=True)  # Field name made lowercase.
    alambre_n_14 = models.CharField(db_column='ALAMBRE_N_14', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cable_n_2 = models.CharField(db_column='CABLE_N_2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cable_n_4 = models.CharField(db_column='CABLE_N_4', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cable_n_6 = models.CharField(db_column='CABLE_N_6', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cable_2x14 = models.CharField(db_column='CABLE_2X14', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cable_3x14 = models.CharField(db_column='CABLE_3X14', max_length=255, blank=True, null=True)  # Field name made lowercase.
    id_municipio = models.IntegerField(blank=True, null=True)
    id_barrio = models.IntegerField(blank=True, null=True)
    seq = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'tmp_correctivo_junio_2'


class TmpInventarioCandelaria(models.Model):
    fecha = models.CharField(db_column='FECHA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    numero_poste = models.CharField(db_column='NUMERO_POSTE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    codigo_luminaria = models.CharField(db_column='CODIGO_LUMINARIA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    municipio = models.CharField(db_column='MUNICIPIO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    barrio = models.CharField(db_column='BARRIO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='DIRECCION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    coordenadas = models.CharField(db_column='COORDENADAS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    id_municipio = models.IntegerField(blank=True, null=True)
    id_barrio = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tmp_inventario_candelaria'


class TmpInventarioManati(models.Model):
    fecha = models.CharField(db_column='FECHA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    numero_poste = models.CharField(db_column='NUMERO_POSTE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    codigo_luminaria = models.CharField(db_column='CODIGO_LUMINARIA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    municipio = models.CharField(db_column='MUNICIPIO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    barrio = models.CharField(db_column='BARRIO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='DIRECCION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    coordenadas = models.CharField(db_column='COORDENADAS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    id_municipio = models.IntegerField(blank=True, null=True)
    id_barrio = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tmp_inventario_manati'


class TmpInventarioPoloNuevo(models.Model):
    fecha = models.CharField(db_column='FECHA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    numero_poste = models.CharField(db_column='NUMERO_POSTE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    codigo_luminaria = models.CharField(db_column='CODIGO_LUMINARIA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    municipio = models.CharField(db_column='MUNICIPIO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    barrio = models.CharField(db_column='BARRIO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='DIRECCION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    coordenadas = models.CharField(db_column='COORDENADAS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    id_municipio = models.IntegerField(blank=True, null=True)
    id_barrio = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tmp_inventario_polo_nuevo'


class TmpInventarioSantaLucia(models.Model):
    fecha = models.CharField(db_column='FECHA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    numero_poste = models.CharField(db_column='NUMERO_POSTE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    codigo_luminaria = models.CharField(db_column='CODIGO_LUMINARIA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    municipio = models.CharField(db_column='MUNICIPIO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    barrio = models.CharField(db_column='BARRIO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='DIRECCION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    coordenadas = models.CharField(db_column='COORDENADAS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    id_municipio = models.IntegerField(blank=True, null=True)
    id_barrio = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tmp_inventario_santa_lucia'


class TmpInventarioSuan(models.Model):
    fecha = models.CharField(db_column='FECHA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    numero_poste = models.CharField(db_column='NUMERO_POSTE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    codigo_luminaria = models.CharField(db_column='CODIGO_LUMINARIA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    municipio = models.CharField(db_column='MUNICIPIO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    barrio = models.CharField(db_column='BARRIO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='DIRECCION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    coordenadas = models.CharField(db_column='COORDENADAS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    id_municipio = models.IntegerField(blank=True, null=True)
    id_barrio = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tmp_inventario_suan'


class TmpInventarioUsiacuri(models.Model):
    fecha = models.CharField(db_column='FECHA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    numero_poste = models.CharField(db_column='NUMERO_POSTE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    codigo_luminaria = models.CharField(db_column='CODIGO_LUMINARIA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    municipio = models.CharField(db_column='MUNICIPIO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    barrio = models.CharField(db_column='BARRIO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='DIRECCION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    coordenadas = models.CharField(db_column='COORDENADAS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    id_municipio = models.IntegerField(blank=True, null=True)
    id_barrio = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tmp_inventario_usiacuri'


class TmpMateriales(models.Model):
    descripcion = models.CharField(max_length=80, blank=True, null=True)
    cantidad = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tmp_materiales'


class TmpModernizacionAgosto(models.Model):
    fecha_ejecucion = models.DateField(db_column='FECHA_EJECUCION', blank=True, null=True)  # Field name made lowercase.
    numero_poste = models.CharField(db_column='NUMERO_POSTE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    codigo_luminaria = models.CharField(db_column='CODIGO_LUMINARIA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    municipio = models.CharField(db_column='MUNICIPIO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    barrio = models.CharField(db_column='BARRIO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='DIRECCION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    coordenadas = models.CharField(db_column='COORDENADAS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tecnico = models.CharField(db_column='TECNICO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    evento = models.CharField(db_column='EVENTO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    descripcion_luminaria = models.CharField(db_column='DESCRIPCION LUMINARIA', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    id_municipio = models.IntegerField(blank=True, null=True)
    id_barrio = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tmp_modernizacion_agosto'


class TmpModernizacionJulio(models.Model):
    fecha = models.DateField(db_column='FECHA', blank=True, null=True)  # Field name made lowercase.
    numero_poste = models.CharField(db_column='NUMERO_POSTE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    codigo_luminaria = models.CharField(db_column='CODIGO_LUMINARIA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    municipio = models.CharField(db_column='MUNICIPIO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    barrio = models.CharField(db_column='BARRIO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='DIRECCION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    coordenadas = models.CharField(db_column='COORDENADAS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    descripcion_luminaria = models.CharField(db_column='DESCRIPCION_LUMINARIA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    evento = models.CharField(db_column='EVENTO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    id_municipio = models.IntegerField(blank=True, null=True)
    id_barrio = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tmp_modernizacion_julio'


class TmpModernizacionJunio(models.Model):
    fecha = models.DateField(db_column='FECHA', blank=True, null=True)  # Field name made lowercase.
    numero_poste = models.CharField(db_column='NUMERO_POSTE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    codigo_luminaria = models.CharField(db_column='CODIGO_LUMINARIA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    municipio = models.CharField(db_column='MUNICIPIO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    barrio = models.CharField(db_column='BARRIO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='DIRECCION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    coordenadas = models.CharField(db_column='COORDENADAS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    descripcion_luminaria = models.CharField(db_column='DESCRIPCION_LUMINARIA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    evento = models.CharField(db_column='EVENTO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    id_municipio = models.IntegerField(blank=True, null=True)
    id_barrio = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tmp_modernizacion_junio'


class TmpPreventivosAgosto(models.Model):
    fecha_revision = models.DateField(db_column='FECHA_REVISION', blank=True, null=True)  # Field name made lowercase.
    municipio = models.CharField(db_column='MUNICIPIO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    barrio = models.CharField(db_column='BARRIO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='DIRECCION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    codigo_luminaria = models.CharField(db_column='CODIGO_LUMINARIA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    numero_poste = models.CharField(db_column='NUMERO_POSTE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    coordenadas = models.CharField(db_column='COORDENADAS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tipo_luminaria = models.CharField(db_column='TIPO_LUMINARIA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tecnico = models.CharField(db_column='TECNICO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    descripcion_mantenimiento = models.CharField(db_column='DESCRIPCION_MANTENIMIENTO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    id_municipio = models.IntegerField(blank=True, null=True)
    id_barrio = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tmp_preventivos_agosto'


class TmpPreventivosJulio(models.Model):
    fecha_revision = models.DateField(db_column='FECHA_REVISION', blank=True, null=True)  # Field name made lowercase.
    municipio = models.CharField(db_column='MUNICIPIO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    barrio = models.CharField(db_column='BARRIO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='DIRECCION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    codigo_luminaria = models.CharField(db_column='CODIGO_LUMINARIA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    numero_poste = models.CharField(db_column='NUMERO_POSTE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    coordenadas = models.CharField(db_column='COORDENADAS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tipo_luminaria = models.CharField(db_column='TIPO_LUMINARIA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tecnico = models.CharField(db_column='TECNICO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    descripcion_mantenimiento = models.CharField(db_column='DESCRIPCION_MANTENIMIENTO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    id_municipio = models.IntegerField(blank=True, null=True)
    id_barrio = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tmp_preventivos_julio'


class TmpPreventivosJunio(models.Model):
    fecha_revision = models.DateField(db_column='FECHA_REVISION', blank=True, null=True)  # Field name made lowercase.
    municipio = models.CharField(db_column='MUNICIPIO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    barrio = models.CharField(db_column='BARRIO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='DIRECCION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    codigo_luminaria = models.CharField(db_column='CODIGO_LUMINARIA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    numero_poste = models.CharField(db_column='NUMERO_POSTE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    coordenadas = models.CharField(db_column='COORDENADAS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tipo_luminaria = models.CharField(db_column='TIPO_LUMINARIA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tecnico = models.CharField(db_column='TECNICO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    descripcion_mantenimiento = models.CharField(db_column='DESCRIPCION_MANTENIMIENTO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    id_municipio = models.IntegerField(blank=True, null=True)
    id_barrio = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tmp_preventivos_junio'


class UnidadMedida(models.Model):
    id_unidad_medida = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)
    abreviatura = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'unidad_medida'


class UsuarioServicio(models.Model):
    id_usuario_servicio = models.AutoField(primary_key=True)
    id_tipo_identificacion = models.ForeignKey(TipoIdentificacion, models.DO_NOTHING, db_column='id_tipo_identificacion')
    identificacion = models.IntegerField(unique=True)
    digito_verificacion = models.IntegerField()
    nombre = models.CharField(max_length=80)
    id_municipio = models.ForeignKey(Municipio, models.DO_NOTHING, db_column='id_municipio')
    direccion = models.CharField(max_length=80)
    telefono = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=45, blank=True, null=True)
    id_tercero_registra = models.IntegerField(blank=True, null=True)
    fch_registro = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario_servicio'


class Vehiculo(models.Model):
    id_vehiculo = models.AutoField(primary_key=True)
    placa = models.CharField(max_length=20, blank=True, null=True)
    descripcion = models.CharField(max_length=45)
    estado = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'vehiculo'
