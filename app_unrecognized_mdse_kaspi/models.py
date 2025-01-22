import datetime

from django.db import models

from django.utils import timezone


class Product(models.Model):
    sku = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Артикул",
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Название товара",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="""
            Указывает на дату, когда система впервые обнаружила 
            данный товар в списке `нераспознанные kaspi`.
        """,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
        help_text="""
            Указывает на дату, когда система изменяла/проверяла информацию о товаре.
        """,
    )
    in_file = models.BooleanField(
        default=True,
        verbose_name="Нераспознанные KASPI",
        help_text="""
            Если этот флаг ИСТИНА (зеленая галочка) - значит товар в Нераспознанные на KASPI.<br>
            Иначе (красный крестик) - товар больше не числится в Нераспознанные на KASPI.
        """,
    )
    # Доп. поля, если нужно

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.sku} – {self.name}"

    @property
    def total_active_time(self) -> datetime.timedelta:
        """
        Считает сумму всех законченных (и текущего активного) периодов.
        """
        total = datetime.timedelta()
        for period in self.active_periods.all():
            if period.ended_at:
                total += period.ended_at - period.started_at
                self.in_file = False
            else:
                # Период еще активен, значит считаем до 'сейчас'
                total += timezone.now() - period.started_at
                self.in_file = True
        self.save()
        return total


class ProductActivePeriod(models.Model):
    """
    Модель, которая хранит периоды, когда товар находится «в списке» (в файле).
    """

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="active_periods"
    )
    started_at = models.DateTimeField(
        verbose_name="Начало периода",
        help_text="""
            Указывает на периоды, когда товар числиться в списке Нераспознанные на KASPI.
        """,
    )
    ended_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Конец периода",
        help_text="""
            Когда товар обработан и больше не числиться в списке Нераспознанные на KASPI
            здесь будет храниться значение (когда система запросила список Нераспознанных и не нашла товар в нем).
        """,
    )

    class Meta:
        verbose_name = "Период в списке Нераспознанные на KASPI"
        verbose_name_plural = "Периоды в списке Нераспознанные на KASPI"

    def __str__(self):
        return (
            f"Период активности для {self.product.sku}"
            f" c {self.started_at} по {self.ended_at or '...'}"
        )
