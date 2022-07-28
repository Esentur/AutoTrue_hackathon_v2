from django.contrib.auth import get_user_model
from django.db import models
from apps.vehicle.models import Vehicle

User = get_user_model()


class Purchase(models.Model):
    vehicle = models.ForeignKey(Vehicle,
                                on_delete=models.CASCADE,
                                related_name='purchases',
                                verbose_name='Покупаемый транспорт')
    buyer = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='purchases',
                              verbose_name='Покупатель')
    cost = models.DecimalField(max_digits=50,
                               decimal_places=2,
                               default=0,
                               blank=True,
                               verbose_name='Итоговая стоимость')

    created_at = models.DateTimeField(verbose_name='Дата заказа', auto_now_add=True)

    is_confirmed = models.BooleanField(verbose_name='Подтвержден ли', default=False)

    def __str__(self):
        return f'{self.vehicle}. Покупатель: {self.buyer}. Итговая стоимость: {self.cost}. Дата заказа: {self.created_at}'

    def save(self, *args, **kwargs):
        self.cost = self.vehicle.price
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Закупка'
        verbose_name_plural = 'Закупки'
