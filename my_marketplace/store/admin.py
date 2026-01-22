from django.contrib import admin
from .models import User, Category, Product, Order

# Реєструємо наші таблиці, щоб їх бачив адмін
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)