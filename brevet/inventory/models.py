from pathlib import Path

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver

from brevet_database.models import Randonneur, Event, Result

class AbstractModel(models.Model):
    created =   models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    ordered =   models.DateTimeField(null=True, blank=True, verbose_name='Заказано')
    received =  models.DateTimeField(null=True, blank=True, verbose_name='Получено')
    removed =   models.DateTimeField(null=True, blank=True, verbose_name='Передано')    
    price =     models.IntegerField(default=0, verbose_name='Цена')
    comment =   models.TextField(blank=True, verbose_name='Комментарий')
    active =    models.BooleanField(default=True, verbose_name='Активность')

    def get_admin_url_change(self):
        return f"/admin/{self._meta.app_label}/{self._meta.object_name.lower()}/{self.pk}/change/"

    def get_admin_url_add(self):
        return f"/admin/{self._meta.app_label}/{self._meta.object_name.lower()}/add/"

    def get_admin_url_delete(self):
        return f"/admin/{self._meta.app_label}/{self._meta.object_name.lower()}/{self.pk}/delete/"

    class Meta:
        abstract = True

class Medal(AbstractModel):
    randonneur =    models.ForeignKey(Randonneur, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Рандоннёр')
    event =         models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Бревет')
    payment =       models.BooleanField(default=False, verbose_name='Оплата')

    class Meta:
        verbose_name = "Медаль"
        verbose_name_plural = "Медали"
        ordering = ['-active', '-removed', '-event__date']

    def __str__(self):
        distance = self.event.route.distance
        created = self.created.strftime("%d.%m.%Y")
        randonneur = f"{self.randonneur.russian_surname} {self.randonneur.russian_name}" if self.randonneur else "(ничья)"
        removed = "(Вручена)" if self.removed else ""
        paid = "(Не оплачена)" if not self.payment else ''
        ordered = "(Не заказана)" if not self.ordered else ''
        received = "(Не получена)" if not self.received else ''

        return f"{ordered}{paid}{received}{removed} Медаль {distance} - {randonneur} - {created}"


@receiver(models.signals.post_save, sender=Event)
def add_medals(sender, instance:Event, created, **kwargs):
    if instance.finished:
        results = Result.objects.filter(event=instance, medal=True)
        price = Price.objects.filter(item='Medal').first() or 0
        for result in results:
            existing = Medal.objects.filter(
                randonneur=result.randonneur,
                event=instance,
                ).first()
            if not existing:
                medal = Medal()
                medal.randonneur = result.randonneur
                medal.event = result.event
                medal.price = int(price)
                medal.save()

class Price(models.Model):
    item = models.CharField(
        unique=True, 
        max_length=64,
        verbose_name="Предмет",
        choices=[
            ("Medal", "Медаль"),
            ("Registration", "Регистрация"),
            ("CardN", "Последние 4 цифры карты ОРВМ")
        ])

    price = models.IntegerField(verbose_name="Цена")

    def __int__(self):
        return self.price
    
    def __str__(self):
        return f"{self.item} - {self.price}"

    class Meta:
        verbose_name = "Цена"
        verbose_name_plural = "Цены"