from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Address(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    locality = models.CharField(max_length=150, verbose_name="Ближайшее местоположение")
    city = models.CharField(max_length=150, verbose_name="Город")
    state = models.CharField(max_length=150, verbose_name="Улица")

    class Meta:
        verbose_name_plural = 'Адреса'

    def __str__(self):
        return self.locality


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name="Имя категории")
    slug = models.SlugField(max_length=55, verbose_name="Web имя категории")
    description = models.TextField(blank=True, verbose_name="Описание категории")
    category_image = models.ImageField(upload_to='category', blank=True, null=True, verbose_name="Изображение категории")
    is_active = models.BooleanField(verbose_name="Активность")
    is_featured = models.BooleanField(verbose_name="Избранное")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        verbose_name_plural = 'Категории'
        ordering = ('-created_at',)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название продукта")
    slug = models.SlugField(max_length=160, verbose_name="Web Название продукта")
    sku = models.CharField(max_length=255, unique=True, verbose_name="Уникальный идентификатор продукта(ID)")
    short_description = models.TextField(verbose_name="Краткое описание")
    detail_description = models.TextField(blank=True, null=True, verbose_name="Подробное описание")
    product_image = models.ImageField(upload_to='product', blank=True, null=True, verbose_name="Изображение продукта")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена товара")
    category = models.ForeignKey(Category, verbose_name="Категория продукта", on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name="Активен")
    is_featured = models.BooleanField(verbose_name="Избранное")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        verbose_name_plural = 'Товары'
        ordering = ('-created_at',)

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        verbose_name_plural = 'Товары в заказе'

    def __str__(self):
        return str(self.user)

    # Creating Model Property to calculate Quantity x Price
    @property
    def total_price(self):
        return self.quantity * self.product.price


STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled')
)


class Order(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    address = models.ForeignKey(Address, verbose_name="Адрес доставки", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Продукт", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    ordered_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=50,
        default="Pending",
        verbose_name="Статус"
    )

    class Meta:
        verbose_name_plural = 'Заказы'
