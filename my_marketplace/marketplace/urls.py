from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from store.views import * # Імпортуємо всі функції

urlpatterns = [
    # --- Адмінка ---
    path('admin/', admin.site.urls),

    # --- Головні сторінки ---
    path('', home, name='home'),
    path('cart/', cart_view, name='cart'),

    # --- Товари та Кошик ---
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),

    # --- Оформлення замовлення ---
    path('checkout/', checkout, name='checkout'),

    # --- Вхід / Реєстрація / Вихід ---
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]

# Налаштування для картинок
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)