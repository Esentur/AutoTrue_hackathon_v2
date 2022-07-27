from django.contrib.auth import get_user_model
from django.db import models

from django.db import models

User = get_user_model()


class Type(models.Model):
    type_title = models.TextField(max_length=100)
    slug = models.SlugField(primary_key=True,
                            max_length=100,
                            unique=True,
                            blank=True)
    type_parent = models.ForeignKey('self',
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank=True,
                                    related_name='type_childen')

    def save(self, *args, **kwargs):
        self.slug = self.type_title.lower()
        super(Type, self).save(*args, **kwargs)

    def __str__(self):
        if self.type_parent:
            return f'{self.type_parent} >> {self.slug}'
        else:
            return self.slug

    class Meta:
        verbose_name = 'Тип транспорта'
        verbose_name_plural = 'Типы транспорта'




class Vehicle(models.Model):
    FUEL_TYPE = (
        ('PETROL', 'бензин'),
        ('DIESEL', 'дизель'),
        ('ELECTRIC', 'электричество'),
        ('GAS', 'газ')
    )
    DRIVE_TYPE = (
        ('rear-wheel', 'задний привод'),
        ('front-wheel', 'передний привод'),
        ('all-wheel', 'полный привод')
    )
    TRANSMISSION_TYPE = (
        ('manual', 'механическая'),
        ('automatic', 'автоматическая'),
        ('variable', 'вариативная/бесступенчатая')
    )
    STEERING_TYPE = (
        ('left', 'левый'),
        ('right', 'правый'),
        ('other', 'другое')
    )
    seller = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='vehicles')
    title = models.CharField(verbose_name='Наименование транспортного средства', max_length=50)
    price = models.DecimalField(verbose_name='Цена', max_digits=15, decimal_places=2)
    year = models.PositiveIntegerField(verbose_name='Год выпуска')
    mileage = models.PositiveIntegerField(verbose_name='Пробег')
    type = models.ForeignKey(Type,
                             on_delete=models.CASCADE,
                             related_name='vehicles',
                             verbose_name='Тип кузова')
    volume = models.DecimalField(verbose_name='объем двигателя', max_digits=3, decimal_places=1)
    fuel = models.CharField(verbose_name='Вид топлива', max_length=10, choices=FUEL_TYPE)
    power = models.PositiveIntegerField(verbose_name='Мощность')
    drive = models.CharField(verbose_name='Привод', max_length=20, choices=DRIVE_TYPE)
    transmission = models.CharField(verbose_name='КПП', max_length=20, choices=TRANSMISSION_TYPE)
    steering = models.CharField(verbose_name='Руль', max_length=20, choices=STEERING_TYPE)

    def __str__(self):
        return f'Модель: {self.title} '

    class Meta:
        ordering = ['title']
        db_table = 'vehicle'
        verbose_name = 'Транспортное средство'
        verbose_name_plural = 'Транстпортные средства'


class Image(models.Model):
    image = models.ImageField(verbose_name='изображение', upload_to='vehicles')
    vehicle = models.ForeignKey(Vehicle,
                                on_delete=models.CASCADE,
                                related_name='images',
                                verbose_name='транспорт')

    def __str__(self):
        return self.vehicle

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
