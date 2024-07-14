from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.core.validators import RegexValidator

class Region(models.Model):
    RegCod = models.AutoField(db_column='RegCod', primary_key=True,  verbose_name="Código")
    RegNom = models.CharField(db_column='RegNom', max_length=20, verbose_name="Nombre")
    RegEstReg = models.CharField(db_column='RegEstReg', max_length=1, default='A', verbose_name="Estado de Registro")

    class Meta:
        db_table = 'Region'

    def __str__(self):
        return self.RegNom

class Municipio(models.Model):
    MunCod = models.AutoField(db_column='MunCod', primary_key=True, verbose_name="Código")
    MunNom = models.CharField(db_column='MunNom', max_length=20, verbose_name="Nombre")
    MunPreAnu = models.DecimalField(db_column='MunPreAnu', max_digits=8, decimal_places=2, default=0,verbose_name="Presupuesto Anual", null=False)
    MunNumViv = models.IntegerField(db_column='MunNumViv', default=0, verbose_name="Número de Viviendas")
    RegCod = models.ForeignKey(Region, on_delete=models.CASCADE, db_column='RegCod', verbose_name="Código de Región")
    MunEstReg = models.CharField(db_column='MunEstReg', max_length=1, default='A', verbose_name="Estado de Registro")

    class Meta:
        db_table = 'Municipio'

    def __str__(self):
        return self.MunNom

class ZonaUrbana(models.Model):
    ZonCod = models.AutoField(db_column='ZonCod', primary_key=True, verbose_name="Código")
    ZonNom = models.CharField(db_column='ZonNom', max_length=20, verbose_name="Nombre")
    MunCod = models.ForeignKey(Municipio, on_delete=models.CASCADE, db_column='MunCod', verbose_name="Código de Municipio")
    ZonEstReg = models.CharField(db_column='ZonEstReg', max_length=1, default='A', verbose_name="Estado de Registro")

    class Meta:
        db_table = 'Zona_Urbana'

    def __str__(self):
        return self.ZonNom

class TipoVivienda(models.Model):
    TipVivCod = models.AutoField(db_column='TipVivCod', primary_key=True, verbose_name="Código")
    TipVivDes = models.CharField(db_column='TipVivDes', max_length=15, verbose_name="Descripción")
    TipVivEstReg = models.CharField(db_column='TipVivEstReg', max_length=1, default='A', verbose_name="Estado de Registro")

    class Meta:
        db_table = 'Tipo_Vivienda'

    def __str__(self):
        return self.TipVivDes

class Vivienda(models.Model):
    VivCod = models.AutoField(db_column='VivCod', primary_key=True, verbose_name="Código")
    VivCal = models.CharField(db_column='VivCal', max_length=3, verbose_name="Calle")
    VivNum = models.IntegerField(db_column='VivNum', verbose_name="Número")
    VivCodPos = models.IntegerField(db_column='VivCodPos', verbose_name="Código Postal")
    VivOcu = models.CharField(db_column='VivOcu', max_length=1, default='N', choices=[('S', 'Sí'), ('N', 'No')], verbose_name="Ocupada")
    ZonCod = models.ForeignKey(ZonaUrbana, on_delete=models.CASCADE, db_column='ZonCod', verbose_name="Código de Zona")
    TipVivCod = models.ForeignKey(TipoVivienda, on_delete=models.CASCADE, db_column='TipVivCod', verbose_name="Código de Tipo de Vivienda")
    VivEstReg = models.CharField(db_column='VivEstReg', max_length=1, default='A', verbose_name="Estado de Registro")

    class Meta:
        db_table = 'Vivienda'
        unique_together = [['VivCal', 'VivNum', 'VivCodPos']]  # Define la combinación única de campos

    def __str__(self):
        return f"Vivienda {self.VivCod}"

    def clean(self):
        # Validar que todos los campos obligatorios sean ingresados
        if not self.VivCal or not self.VivNum or not self.VivCodPos or not self.VivOcu or not self.ZonCod or not self.TipVivCod:
            raise ValidationError("Todos los campos de Vivienda son obligatorios.")
            
    def save(self, *args, **kwargs):
        self.full_clean()  # Realizar la validación antes de guardar
        super().save(*args, **kwargs)

class Familia(models.Model):
    FamCod = models.AutoField(db_column ='FamCod',primary_key=True, verbose_name="Código")
    FamNom = models.CharField(db_column ='FamNom',max_length=15,verbose_name="Nombre")
    FamNumInt = models.IntegerField(db_column ='FamNumInt',default=0,verbose_name="Número de Integrantes")
    FamEstReg = models.CharField(db_column='FamEstReg', max_length=1, default='A', verbose_name="Estado de Registro")
    class Meta:
        db_table = 'Familia'

    def __str__(self):
        return self.FamNom

class TipoPersona(models.Model):
    TipPerCod = models.AutoField(db_column='TipPerCod',primary_key=True,verbose_name="Código")
    TipPerDes = models.CharField(db_column='TipPerDes',max_length=15,verbose_name="Descripción")
    TipPerEstReg = models.CharField(db_column='TipPerEstReg',max_length=1, default='A',verbose_name="Estado de Registro")

    class Meta:
        db_table = 'Tipo_Persona'

    def __str__(self):
        return self.TipPerDes

class Persona(models.Model):
    PerCod = models.AutoField(db_column='PerCod',primary_key=True,verbose_name="Código")
    PerNom = models.CharField(db_column='PerNom',max_length=15,verbose_name="Nombre")
    FamCod = models.ForeignKey(Familia, on_delete=models.CASCADE, db_column='FamCod',verbose_name="Código de Familia")
    TipPerCod = models.ForeignKey(TipoPersona, on_delete=models.CASCADE, db_column='TipPerCod',verbose_name="Tipo Persona Código")
    PerEstReg = models.CharField(db_column='PerEstReg',max_length=1, default='A',verbose_name="Estado de Registro")

    class Meta:
        db_table = 'Persona'

    def __str__(self):
        return self.PerNom

    def clean(self):
        # Validar que el nombre no sea nulo
        if not self.PerNom:
            raise ValidationError("El nombre de la persona no puede ser nulo.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Realizar la validación antes de guardar
        super().save(*args, **kwargs)

class Casa(models.Model):
    CasCod = models.AutoField(db_column='CasCod',primary_key=True,verbose_name="Código")
    CasEsc = models.CharField(db_column='CasEsc', max_length=2, default=' ',null=True, verbose_name="Escalera", blank=True, validators=[RegexValidator(r'^[0-9]*$', 'Ingrese solo números válidos.')])
    CasCodBlo = models.CharField(db_column='CasCodBlo',max_length=2, default=' ',null=True,verbose_name="Código de Bloque")
    CasPla = models.CharField(db_column='CasPla', max_length=2, default=' ', null=True,verbose_name="Planta", blank=True, validators=[RegexValidator(r'^[0-9]*$', 'Ingrese solo números válidos.')])
    CasNumPue = models.CharField(db_column='CasNumPue', max_length=2, default=' ', null=True, verbose_name="Número de Puerta", blank=True, validators=[RegexValidator(r'^[0-9]*$', 'Ingrese solo números válidos.')])
    CasMet = models.DecimalField(db_column='CasMet',max_digits=5, decimal_places=2,verbose_name="Metros", null=False)
    VivCod = models.ForeignKey(Vivienda, on_delete=models.CASCADE,db_column='VivCod',verbose_name="Código de Vivienda")
    FamCod = models.ForeignKey(Familia, on_delete=models.CASCADE, db_column='FamCod', verbose_name="Código de Familia")
    CasEstReg = models.CharField(db_column='CasEstReg',max_length=1, default='A',verbose_name="Estado de Registro")

    class Meta:
        db_table = 'Casa'

    def __str__(self):
        return f"Casa {self.CasCod}"

    def clean(self):
        # Validar que CasMet no sea nulo
        if not self.CasMet:
            raise ValidationError("El campo CasMet no puede ser nulo.")

        # Validar que solo una familia puede tener una casa
        existing_casa = Casa.objects.filter(FamCod=self.FamCod)
        if self.pk:
            existing_casa = existing_casa.exclude(pk=self.pk)  # Excluir la instancia actual al editar
        if existing_casa.exists():
            raise ValidationError("Esta familia ya tiene asignada una casa.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Llama a clean() antes de guardar para validar
        super().save(*args, **kwargs)

class PagoTributario(models.Model):
    ESTADOS = [
        ('en proceso', 'En Proceso'),
        ('pagada', 'Pagada'),
        ('debe', 'Debe')
    ]

    PagTriCod = models.AutoField(db_column='PagTriCod',primary_key=True,verbose_name="Pago Tributario Codigo")
    PagTriFec = models.DateField(db_column='PagTriFec', blank=True, null=True, verbose_name="Pago Tributario Fecha emitida")
    CasCod = models.ForeignKey(Casa, on_delete=models.CASCADE,db_column='CasCod',verbose_name="Código de Casa")
    PagTriCat = models.CharField(db_column='PagTriCat',max_length=1,verbose_name="Categoria")
    PagTriPag = models.DecimalField(db_column='PagTriPag',max_digits=8, decimal_places=2, default=0,verbose_name="Pago Total")
    PagTriEstReg = models.CharField(db_column='PagTriEstReg',max_length=15, choices=ESTADOS,verbose_name="Estado de Pago")

    class Meta:
        db_table = 'Pago_Tributario'

    def __str__(self):
        return f"Pago {self.PagTriCod}"

class Propietario(models.Model):
    ProCod = models.AutoField(db_column='ProCod',primary_key=True,verbose_name="Código")
    ProPagTri = models.DecimalField(db_column='ProPagTri',max_digits=8, decimal_places=2, null=True,verbose_name="Pago Tributario")
    ProMonIngFam = models.DecimalField(db_column='ProMonIngFam',max_digits=8, decimal_places=2, default=0,verbose_name="Monto Ingreso Familiar")
    PerCod = models.ForeignKey(Persona, on_delete=models.CASCADE,db_column='PerCod',verbose_name="Código de Persona")
    ProEstReg = models.CharField(db_column='ProEstReg',max_length=1, default='A',verbose_name="Estado de Registro")

    class Meta:
        db_table = 'Propietario'

    def __str__(self):
        return f"Propietario {self.ProCod}"

    def clean(self):
        # Validar que ProMonIngFam no sea nulo
        if not self.ProMonIngFam:
            raise ValidationError("El campo ProMonIngFam no puede ser nulo.")

        # Validar que la persona tiene el tipo "Propietario"
        if self.PerCod.TipPerCod.TipPerDes != "Propietario":
            raise ValidationError("La persona seleccionada no tiene el tipo de persona 'Propietario'.")

        # Validar que la persona no sea propietario de más de una familia
        if Propietario.objects.filter(PerCod=self.PerCod).exists() and self.pk is None:
            raise ValidationError("La persona seleccionada ya es propietario de otra familia.")

    def save(self, *args, **kwargs):
        # Calcular el pago tributario
        self.ProPagTri = self.ProMonIngFam * Decimal('0.1')  # Multiplicar por 0.1 como Decimal

        self.full_clean()  # Validar antes de guardar
        super().save(*args, **kwargs)
