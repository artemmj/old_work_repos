from django.db import models
from django.db.models.functions import DenseRank

from apps.helpers.models import CreatedModel, UUIDModel
from apps.project.models import Project
from apps.task.models import Task

PRODUCTS_FILE_LENGTH = 255


class Product(UUIDModel):
    title = models.CharField('Название', max_length=511, null=True, blank=True)
    vendor_code = models.CharField('Код товара', max_length=150, null=True, blank=True)
    barcode = models.CharField('Штрих-код', max_length=48)
    price = models.DecimalField('Цена', max_digits=9, decimal_places=2, default=0)
    remainder = models.DecimalField('Остаток', max_digits=11, decimal_places=3, default=0, null=True, blank=True)
    project = models.ForeignKey(Project, verbose_name='Проект', related_name='products', on_delete=models.CASCADE)
    am = models.CharField('Акцизная марка', max_length=150, null=True, blank=True)
    dm = models.CharField('Датаматрикс', max_length=255, null=True, blank=True)
    store_number = models.PositiveIntegerField('Номер магазина (для РеТрейдинг)', null=True, blank=True)
    size = models.CharField('Размер', max_length=31, null=True, blank=True)
    remainder_2 = models.DecimalField(
        'Остаток 2 (виртуальный)',
        max_digits=11,
        decimal_places=3,
        default=0,
        null=True,
        blank=True,
    )
    qr_code = models.CharField('QR-код', max_length=200, null=True, blank=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['title']),
            models.Index(fields=['barcode']),
        ]

    def __str__(self):
        return f'Product: {self.title}'


class ScannedProductQuerySet(models.QuerySet):

    def with_number_idx(self):
        return self.annotate(
            number=models.Window(
                expression=DenseRank(),
                order_by=[
                    models.F('id').desc(),
                ],
            ),
        )

    def with_displayed_dm(self):
        return self.annotate(
            displayed_dm=models.Case(
                models.When(
                    dm__isnull=False,
                    then=models.F('dm'),
                ),
                models.When(
                    product__dm__isnull=False,
                    then=models.F('product__dm'),
                ),
                default=models.F('dm'),
                output_field=models.CharField(),
            ),
        )


class ScannedProduct(UUIDModel, CreatedModel):
    product = models.ForeignKey(
        Product, verbose_name='Товар', related_name='scanned_products', on_delete=models.CASCADE,
    )
    task = models.ForeignKey(
        Task, verbose_name='Задание', related_name='scanned_products', on_delete=models.CASCADE,
    )
    amount = models.DecimalField('Колличество', max_digits=11, decimal_places=3, default=0)
    scanned_time = models.DateTimeField('Время сканирования товара', null=True, blank=True)
    added_by_product_code = models.BooleanField('Найден по коду товара', default=False)
    added_by_qr_code = models.BooleanField('Найден по QR-коду товара', default=False)
    is_weight = models.BooleanField('Весовой', default=False)
    dm = models.CharField('Датаматрикс', max_length=255, blank=True, null=True)

    objects = ScannedProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'Отсканированный товар'
        verbose_name_plural = 'Отсканированные товары'

    def __str__(self):
        return f'ScannedProduct: {self.id}'


class FileOfProjectProducts(UUIDModel, CreatedModel):
    project = models.OneToOneField(Project, models.CASCADE, related_name='file_of_products')
    products_file = models.CharField(max_length=PRODUCTS_FILE_LENGTH)

    class Meta:
        verbose_name = 'Сгенерированный .txt-файл с товарами'
        verbose_name_plural = 'Сгенерированные .txt-файлы с товарами'


class AdditionalProductTitleAttribute(UUIDModel):
    project = models.ForeignKey(
        Project,
        verbose_name='Проект',
        related_name='title_attrs',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    product = models.ForeignKey(
        Product,
        verbose_name='Продукт',
        related_name='title_attrs',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    content = models.CharField('Содержимое аттрибута', max_length=200)
    is_hidden = models.BooleanField('Скрытый или нет', default=False)

    class Meta:
        verbose_name = 'Дополнительный атрибут названия товара'
        verbose_name_plural = 'Дополнительные атрибуты названия товара'
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['is_hidden']),
        ]

    def __str__(self):
        return f'Additional title attr: {self.content}'
