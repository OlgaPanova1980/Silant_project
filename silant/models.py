from django.db import models
from django.contrib.auth.models import User


class BaseDirectory(models.Model):
    directory_name = models.CharField(max_length=255, verbose_name="Название сущности (справочника)", null=True, blank=True)
    name = models.CharField(max_length=255, verbose_name="Имя")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class VehicleModel(BaseDirectory):
    directory_name = models.CharField(max_length=255, verbose_name="Название сущности (справочника)", default="Модель техники")
    class Meta:
        verbose_name = "Модель техники"
        verbose_name_plural = "Модели техники"

class EngineModel(BaseDirectory):
    directory_name = models.CharField(max_length=255, verbose_name="Название сущности (справочника)", default="Модель двигателя")
    class Meta:
        verbose_name = "Модель двигателя"
        verbose_name_plural = "Модели двигателя"

class TransmissionModel(BaseDirectory):
    directory_name = models.CharField(max_length=255, verbose_name="Название сущности (справочника)", default="Модель трансмиссии")
    class Meta:
        verbose_name = "Модель трансмиссии"
        verbose_name_plural = "Модели трансмиссии"

class DriveAxleModel(BaseDirectory):
    directory_name = models.CharField(max_length=255, verbose_name="Название сущности (справочника)", default="Модель ведущего моста")
    class Meta:
        verbose_name = "Модель ведущего моста"
        verbose_name_plural = "Модели ведущих мостов"

class SteeringAxleModel(BaseDirectory):
    directory_name = models.CharField(max_length=255, verbose_name="Название сущности (справочника)", default="Модель управляемого моста")
    class Meta:
        verbose_name = "Модель управляемого моста"
        verbose_name_plural = "Модели управляемых мостов"

class MaintenanceType(BaseDirectory):
    directory_name = models.CharField(max_length=255, verbose_name="Название сущности (справочника)", default="Вид ТО")
    class Meta:
        verbose_name = "Вид ТО"
        verbose_name_plural = "Виды ТО"

class FailureNode(BaseDirectory):
    directory_name = models.CharField(max_length=255, verbose_name="Название сущности (справочника)", default="Узел отказа")
    class Meta:
        verbose_name = "Узел отказа"
        verbose_name_plural = "Узлы отказа"

class RecoveryMethod(BaseDirectory):
    directory_name = models.CharField(max_length=255, verbose_name="Название сущности (справочника)", default="Способ восстановления")
    class Meta:
        verbose_name = "Способ восстановления"
        verbose_name_plural = "Способы восстановления"

class MaintenanceOrganization(BaseDirectory):
    directory_name = models.CharField(max_length=255, verbose_name="Название сущности (справочника)", default="Организация, проводившая ТО")
    class Meta:
        verbose_name = "Организация, проводившая ТО"
        verbose_name_plural = "Организации, проводившие ТО"



class ServiceCompany(BaseDirectory):
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        limit_choices_to={'is_staff': False},
        related_name='service_profile',
        verbose_name="Пользователь (Аккаунт организации)"
    )

    class Meta:
        verbose_name = "Сервисная компания"
        verbose_name_plural = "Сервисные компании"
 
    def __str__(self):
        if self.user:
            return self.user.get_full_name() or self.user.username
        return self.name or f"Сервисная компания №{self.pk}"


class Machine(models.Model):
    vin = models.CharField(max_length=50, unique=True, verbose_name="Заводской № машины")
    vehicle_model = models.ForeignKey(VehicleModel, on_delete=models.PROTECT, verbose_name="Модель техники")
    engine_model = models.ForeignKey(EngineModel, on_delete=models.PROTECT, verbose_name="Модель двигателя")
    engine_num = models.CharField(max_length=50, verbose_name="Заводской № двигателя")
    transmission_model = models.ForeignKey(TransmissionModel, on_delete=models.PROTECT, verbose_name="Модель трансмиссии")
    transmission_num = models.CharField(max_length=50, verbose_name="Заводской № трансмиссии")
    drive_axle_model = models.ForeignKey(DriveAxleModel, on_delete=models.PROTECT, verbose_name="Модель ведущего моста")
    drive_axle_num = models.CharField(max_length=50, verbose_name="Заводской № ведущего моста")
    steering_axle_model = models.ForeignKey(SteeringAxleModel, on_delete=models.PROTECT, verbose_name="Модель управляемого моста")
    steering_axle_num = models.CharField(max_length=50, verbose_name="Заводской № управляемого моста")
    
    delivery_contract = models.CharField(max_length=100, verbose_name="Договор поставки №, дата")
    shipping_date = models.DateField(verbose_name="Дата отгрузки с завода")
    consignee = models.CharField(max_length=255, verbose_name="Грузополучатель (конечный потребитель)")
    delivery_address = models.CharField(max_length=500, verbose_name="Адрес поставки (эксплуатации)")
    equipment = models.TextField(blank=True, verbose_name="Комплектация (доп. опции)")
    
    client = models.ForeignKey(User, on_delete=models.PROTECT, related_name='machines', verbose_name="Клиент")
    service_company = models.ForeignKey(ServiceCompany, on_delete=models.PROTECT, related_name='maintained_machines', verbose_name="Сервисная компания")

    class Meta:
        verbose_name = "Машина"
        verbose_name_plural = "Машины"
        ordering = ['-shipping_date']

    def __str__(self):
        return f"{self.vehicle_model.name} (Зав. №{self.vin})"


class Maintenance(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='maintenances', verbose_name="Машина")
    maintenance_type = models.ForeignKey(MaintenanceType, on_delete=models.PROTECT, verbose_name="Вид ТО")
    maintenance_date = models.DateField(verbose_name="Дата проведения ТО")
    operating_hours = models.IntegerField(verbose_name="Наработка, м/час")
    order_number = models.CharField(max_length=100, verbose_name="№ заказ-наряда")
    order_date = models.DateField(verbose_name="Дата заказ-наряда")
    maintenance_org = models.ForeignKey(MaintenanceOrganization, on_delete=models.PROTECT, verbose_name="Организация, проводившая ТО", null=True, blank=True)
    service_company = models.ForeignKey(ServiceCompany, on_delete=models.PROTECT, verbose_name="Сервисная компания", null=True, blank=True)

    class Meta:
        verbose_name = "Техническое обслуживание"
        verbose_name_plural = "Технические обслуживания"
        ordering = ['-maintenance_date']

    def save(self, *args, **kwargs):
        if not self.service_company_id and self.machine_id:
            self.service_company = self.machine.service_company
        super().save(*args, **kwargs)

    def __str__(self):
        return f"ТО {self.maintenance_type.name} для {self.machine.vin} от {self.maintenance_date}"


class Complaint(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='complaints', verbose_name="Машина")
    failure_date = models.DateField(verbose_name="Дата отказа")
    operating_hours = models.IntegerField(verbose_name="Наработка, м/час")
    failure_node = models.ForeignKey(FailureNode, on_delete=models.PROTECT, verbose_name="Узел отказа")
    failure_description = models.TextField(verbose_name="Описание отказа")
    recovery_method = models.ForeignKey(RecoveryMethod, on_delete=models.PROTECT, verbose_name="Способ восстановления")
    parts_used = models.TextField(blank=True, null=True, verbose_name="Используемые запасные части")
    recovery_date = models.DateField(verbose_name="Дата восстановления")
    downtime = models.IntegerField(editable=False, verbose_name="Время простоя (дней)")
    service_company = models.ForeignKey(ServiceCompany, on_delete=models.PROTECT, verbose_name="Сервисная компания", null=True, blank=True)

    class Meta:
        verbose_name = "Рекламация"
        verbose_name_plural = "Рекламации"
        ordering = ['-failure_date']

    def save(self, *args, **kwargs):
        if self.recovery_date and self.failure_date:
            self.downtime = (self.recovery_date - self.failure_date).days
        if not self.service_company_id and self.machine_id:
            self.service_company = self.machine.service_company
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Рекламация по машине {self.machine.vin} от {self.failure_date}"

