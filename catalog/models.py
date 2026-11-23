from django.db import models
from django.conf import settings

# МОДЕЛЬ КАТЕГОРИИ
class Category(models.Model):
    name = models.CharField("Название категории", max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

# МОДЕЛЬ ХАРАКТЕРИСТИК
class Characteristic(models.Model):
    name = models.CharField("Характеристика", max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Характеристика"
        verbose_name_plural = "Характеристики"

    def __str__(self):
        return self.name


# МОДЕЛЬ ТОВАРА
class Product(models.Model):
    class Status(models.TextChoices):
        IN_STOCK = "in_stock", "В наличии"
        OUT_OF_STOCK = "out_of_stock", "Нет в наличии"
        ARCHIVED = "archived", "Снят с продажи"

    title = models.CharField("Название товара", max_length=100)
    description = models.TextField("Описание", blank=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    status = models.CharField("Статус", max_length=20, choices=Status.choices, default=Status.IN_STOCK,)
    category = models.ForeignKey( Category, on_delete=models.CASCADE, related_name="products", verbose_name="Категория",)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="products", verbose_name="Автор",)
    characteristics = models.ManyToManyField(Characteristic, blank=True, related_name="products", verbose_name="Характеристики",)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата изменения", auto_now=True)

    class Meta:
        ordering = ["-created_at", "-id"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.title
