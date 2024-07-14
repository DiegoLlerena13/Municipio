from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal, ROUND_HALF_UP
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.validators import MaxLengthValidator

class Region(models.Model):
    RegCod = models.AutoField(db_column='RegCod', primary_key=True,  verbose_name="Código")
    RegNom = models.CharField(db_column='RegNom', max_length=20, verbose_name="Nombre", unique=True, null=False)
    RegEstReg = models.CharField(db_column='RegEstReg', max_length=1, default='A', verbose_name="Estado de Registro")

    class Meta:
        db_table = 'Region'

    def __str__(self):
        return self.RegNom

class Municipio(models.Model):
    MunCod = models.AutoField(db_column='MunCod', primary_key=True, verbose_name="Código")
    MunNom = models.CharField(db_column='MunNom', max_length=20, verbose_name="Nombre", unique=True, null=False)
    MunPreAnu = models.DecimalField(db_column='MunPreAnu', max_digits=8, decimal_places=2, default=0,verbose_name="Presupuesto Anual", null=False)
    MunNumViv = models.IntegerField(db_column='MunNumViv', default=0, verbose_name="Número de Viviendas", null=True)
    RegCod = models.ForeignKey(Region, on_delete=models.CASCADE, db_column='RegCod', verbose_name="Código de Región")
    MunEstReg = models.CharField(db_column='MunEstReg', max_length=1, default='A', verbose_name="Estado de Registro")

    class Meta:
        db_table = 'Municipio'

    def __str__(self):
        return self.MunNom

class ZonaUrbana(models.Model):
    ZonCod = models.AutoField(db_column='ZonCod', primary_key=True, verbose_name="Código")
    ZonNom = models.CharField(db_column='ZonNom', max_length=20, verbose_name="Nombre", unique=True, null=False)
    MunCod = models.ForeignKey(Municipio, on_delete=models.CASCADE, db_column='MunCod', verbose_name="Código de Municipio")
    ZonEstReg = models.CharField(db_column='ZonEstReg', max_length=1, default='A', verbose_name="Estado de Registro")

    class Meta:
        db_table = 'Zona_Urbana'

    def __str__(self):
        return self.ZonNom

class TipoVivienda(models.Model):
    TipVivCod = models.AutoField(db_column='TipVivCod', primary_key=True, verbose_name="Código")
    TipVivDes = models.CharField(db_column='TipVivDes', max_length=15, verbose_name="Descripción", unique=True, null=False)
    TipVivEstReg = models.CharField(db_column='TipVivEstReg', max_length=1, default='A', verbose_name="Estado de Registro")

    class Meta:
        db_table = 'Tipo_Vivienda'

    def __str__(self):
        return self.TipVivDes

class Vivienda(models.Model):
    VivCod = models.AutoField(db_column='VivCod', primary_key=True, verbose_name="Código")
    VivCal = models.CharField(db_column='VivCal', max_length=3, verbose_name="Calle",validators=[MaxLengthValidator(3)])
    VivNum = models.CharField(db_column='VivNum', max_length=2, verbose_name="Número",validators=[MaxLengthValidator(2)])
    VivCodPos = models.CharField(db_column='VivCodPos', max_length=4, verbose_name="Código Postal",validators=[MaxLengthValidator(4)])
    VivOcu = models.CharField(db_column='VivOcu', max_length=1, default='N', choices=[('S', 'Sí'), ('N', 'No')], verbose_name="Ocupada")
    ZonCod = models.ForeignKey(ZonaUrbana, on_delete=models.CASCADE, db_column='ZonCod', verbose_name="Código de Zona")
    TipVivCod = models.ForeignKey(TipoVivienda, on_delete=models.CASCADE, db_column='TipVivCod', verbose_name="Código de Tipo de Vivienda")
    VivEstReg = models.CharField(db_column='VivEstReg', max_length=1, default='A', verbose_name="Estado de Registro")

    class Meta:
        db_table = 'Vivienda'
        unique_together = [['VivCal', 'VivNum']]  # Define la combinación única de campos

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
    TipPerDes = models.CharField(db_column='TipPerDes',max_length=15,verbose_name="Descripción", unique=True)
    TipPerEstReg = models.CharField(db_column='TipPerEstReg',max_length=1, default='A',verbose_name="Estado de Registro")

    class Meta:
        db_table = 'Tipo_Persona'

    def __str__(self):
        return self.TipPerDes

class Persona(models.Model):
    PerCod = models.AutoField(db_column='PerCod',primary_key=True,verbose_name="Código")
    PerNom = models.CharField(db_column='PerNom',max_length=20,verbose_name="Nombres")
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
        
        tipo_propietario = TipoPersona.objects.get(TipPerDes='Propietario')
        if self.TipPerCod == tipo_propietario:
            existing_propietario = Persona.objects.filter(FamCod=self.FamCod, TipPerCod=tipo_propietario)
            if self.pk:
                existing_propietario = existing_propietario.exclude(pk=self.pk)  # Excluir la instancia actual al editar
            if existing_propietario.exists():
                raise ValidationError("Esta familia ya tiene un propietario asignado.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Realizar la validación antes de guardar
        super().save(*args, **kwargs)

class Casa(models.Model):
    CasCod = models.AutoField(db_column='CasCod',primary_key=True,verbose_name="Código")
    CasEsc = models.CharField(db_column='CasEsc', max_length=2, default='  ', null=True, verbose_name="Escalera", blank=True, validators=[MaxLengthValidator(2),RegexValidator(r'^[0-9]*$', 'Ingrese solo números válidos.')])
    CasCodBlo = models.CharField(db_column='CasCodBlo', max_length=2, default=' ',blank=True,validators=[MaxLengthValidator(2)], null=True, verbose_name="Código de Bloque")
    CasPla = models.CharField(db_column='CasPla', max_length=2, default='  ', null=True, verbose_name="Planta", blank=True, validators=[MaxLengthValidator(2),RegexValidator(r'^[0-9]*$', 'Ingrese solo números válidos.')])
    CasNumPue = models.CharField(db_column='CasNumPue', max_length=2, default='  ', null=True, verbose_name="Número de Puerta", blank=True, validators=[MaxLengthValidator(2),RegexValidator(r'^[0-9]*$', 'Ingrese solo números válidos.')])
    CasMet = models.DecimalField(db_column='CasMet', max_digits=7, decimal_places=2, verbose_name="Metros", null=False)
    VivCod = models.ForeignKey(Vivienda, on_delete=models.CASCADE, db_column='VivCod', verbose_name="Código de Vivienda")
    FamCod = models.ForeignKey(Familia, on_delete=models.CASCADE, db_column='FamCod', verbose_name="Código de Familia")
    CasEstReg = models.CharField(db_column='CasEstReg', max_length=1, default='A', verbose_name="Estado de Registro")

    class Meta:
        db_table = 'Casa'
        unique_together = [['CasEsc', 'CasCodBlo', 'CasPla', 'CasNumPue']]  # Define la combinación única de campos

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
        
         # Validar que solo una familia puede tener una casa si la vivienda es de tipo "Particular"
        if self.VivCod.TipVivCod.TipVivDes == "Particular":
            existing_casa = Casa.objects.filter(VivCod=self.VivCod)
            if self.pk:
                existing_casa = existing_casa.exclude(pk=self.pk)  # Excluir la instancia actual al editar
            if existing_casa.exists():
                raise ValidationError("Ya existe una casa asignada a esta vivienda particular.")
            if self.CasEsc or self.CasCodBlo or self.CasPla or self.CasNumPue:
                raise ValidationError("Los campos CasEsc, CasCodBlo, CasPla y CasNumPue deben estar vacíos si la vivienda no es de tipo BloqueCasa.")

        # Validar campos específicos si la vivienda es del tipo "BloqueCasa"
        if self.VivCod.TipVivCod.TipVivDes == "BloqueCasa":
            if not self.CasEsc or not self.CasCodBlo or not self.CasPla or not self.CasNumPue:
                raise ValidationError("Los campos CasEsc, CasCodBlo, CasPla y CasNumPue son obligatorios si la vivienda es de tipo 'BloqueCasa'.")
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Llama a clean() antes de guardar para validar
        super().save(*args, **kwargs)

class PagoTributario(models.Model):
    ESTADOS = [
        ('en proceso', 'En Proceso'),
        ('pagada', 'Pagada'),
        ('debe', 'Debe')
    ]

    PagTriCod = models.AutoField(db_column='PagTriCod', primary_key=True, verbose_name="Pago Tributario Codigo")
    PagTriFec = models.DateField(db_column='PagTriFec', default=timezone.now, verbose_name="Pago Tributario Fecha emitida")
    CasCod = models.ForeignKey(Casa, on_delete=models.CASCADE, db_column='CasCod', verbose_name="Código de Casa")
    PagTriIngFam = models.DecimalField(db_column='PagTriIngFam', max_digits=6, decimal_places=2, null=False, default=0, verbose_name="Ingreso Familiar")
    PagTriCat = models.CharField(db_column='PagTriCat', max_length=1, null=True, default=' ', verbose_name="Categoria")
    PagTriPag = models.DecimalField(db_column='PagTriPag', max_digits=8, decimal_places=2, default=0, verbose_name="Pago Total")
    PagTriEstReg = models.CharField(db_column='PagTriEstReg', max_length=15, choices=ESTADOS, default="debe", verbose_name="Estado de Pago")

    class Meta:
        db_table = 'Pago_Tributario'
        unique_together = [['CasCod']] 

    def __str__(self):
        return f"Pago {self.PagTriCod}"
    
    def clean(self):
        # Validar que no haya duplicados de casa
        if PagoTributario.objects.filter(CasCod=self.CasCod).exists() and self.pk is None:
            raise ValidationError("Esta casa ya tiene un pago tributario asignado.")

    def save(self, *args, **kwargs):
        propietario = Propietario.objects.filter(PerCod__FamCod=self.CasCod.FamCod).first()
        if propietario:
            self.PagTriIngFam = propietario.ProMonIngFam
            # Asignar la categoría basada en el ingreso familiar
            if self.PagTriIngFam < 1000:
                self.PagTriCat = 'A'
            elif 1000 <= self.PagTriIngFam < 2500:
                self.PagTriCat = 'B'
            else:
                self.PagTriCat = 'C'
                
            if self.PagTriCat == 'A':
                self.PagTriPag = Decimal(self.PagTriIngFam) * Decimal('0.10')
            elif self.PagTriCat == 'B':
                self.PagTriPag = Decimal(self.PagTriIngFam) * Decimal('0.15')
            elif self.PagTriCat == 'C':
                self.PagTriPag = Decimal(self.PagTriIngFam) * Decimal('0.20')
            self.PagTriPag = self.PagTriPag.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        else:
            raise ValidationError("No se encontró un propietario para esta casa.")
        
        self.full_clean()  # Realizar la validación antes de guardar
        super().save(*args, **kwargs)
    
class Propietario(models.Model):
    ProCod = models.AutoField(db_column='ProCod', primary_key=True, verbose_name="Código")
    ProMonIngFam = models.DecimalField(db_column='ProMonIngFam', max_digits=10, decimal_places=2, default=0, verbose_name="Monto Ingreso Familiar")
    PerCod = models.ForeignKey(Persona, on_delete=models.CASCADE, db_column='PerCod', verbose_name="Código de Persona")
    ProEstReg = models.CharField(db_column='ProEstReg', max_length=1, default='A', verbose_name="Estado de Registro")

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
            raise ValidationError("La persona seleccionada ya es propietario una familia.")

    def save(self, *args, **kwargs):

        self.full_clean()  # Validar antes de guardar
        super().save(*args, **kwargs)
