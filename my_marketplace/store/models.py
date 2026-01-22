from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. Користувач
class User(AbstractUser):
    is_seller = models.BooleanField(default=False, verbose_name="Це продавець?")
    phone_number = models.CharField(max_length=15, blank=True, verbose_name="Телефон")

# 2. Категорія
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва категорії")
    slug = models.SlugField(unique=True, verbose_name="URL-ім'я")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

# 3. Товар
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Категорія")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', verbose_name="Продавець")
    name = models.CharField(max_length=200, verbose_name="Назва товару")
    description = models.TextField(verbose_name="Опис")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Фото")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

# 4. Замовлення (З АДРЕСОЮ)
class Order(models.Model):
    STATUS_CHOICES = (
        ('new', 'Нове'),
        ('paid', 'Оплачено'),
        ('shipped', 'Відправлено'),
        ('completed', 'Виконано'),
    )
    
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="Покупець")
    
    # Поля для доставки
    first_name = models.CharField(max_length=50, verbose_name="Ім'я", default="")
    last_name = models.CharField(max_length=50, verbose_name="Прізвище", default="")
    phone = models.CharField(max_length=20, verbose_name="Телефон", default="")
    address = models.TextField(verbose_name="Адреса доставки", default="")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Сума")

    def __str__(self):
        return f"Замовлення #{self.id}"
    
    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"

# 5. Деталі замовлення (ОСЬ ЦЬОГО НЕ ВИСТАЧАЛО)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Кількість")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна на момент покупки")

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"