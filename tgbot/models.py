from __future__ import annotations
from typing import Union, Optional, Tuple
from django.db import models
from django.db.models import QuerySet
from telegram import Update
from telegram.ext import CallbackContext
from dtb.settings import DEBUG
from tgbot.handlers.utils.info import extract_user_data_from_update
from utils.models import nb, GetOrNoneManager,CreateUpdateTracker


class User(CreateUpdateTracker):
    user_id = models.PositiveBigIntegerField(primary_key=True)
    username = models.CharField(max_length=32, **nb)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, **nb)
    language_code = models.CharField(max_length=8, help_text="Foydalanuvchining qurilmadagi tili.", default='uz ')
    deep_link = models.CharField(max_length=64, **nb)
    action = models.CharField(verbose_name='Holati', max_length=10, **nb)
    action_item = models.SmallIntegerField(verbose_name='Holat qiymati', **nb, default=None)
    locations = models.CharField(max_length=64, default=None, **nb)

    is_blocked_bot = models.BooleanField(default=False)

    is_admin = models.BooleanField(default=False)

    objects = GetOrNoneManager()  

    def __str__(self):
        return f'@{self.username}' if self.username is not None else f'{self.user_id}'

    @classmethod
    def get_user_and_created(cls, update: Update, context: CallbackContext) -> Tuple[User, bool]:
        """ python-telegram-bot's Update, Context --> User instance """
        data = extract_user_data_from_update(update)
        u, created = cls.objects.update_or_create(user_id=data["user_id"], defaults=data)

        if created:
            # Save deep_link to User model
            if context is not None and context.args is not None and len(context.args) > 0:
                payload = context.args[0]
                if str(payload).strip() != str(data["user_id"]).strip():  # you can't invite yourself
                    u.deep_link = payload
                    u.save()

        return u, created

    @classmethod
    def get_user(cls, update: Update, context: CallbackContext) -> User:
        u, _ = cls.get_user_and_created(update, context)
        return u

    @classmethod
    def get_user_by_username_or_user_id(cls, username_or_user_id: Union[str, int]) -> Optional[User]:
        """ Search user in DB, return User or None if not found """
        username = str(username_or_user_id).replace("@", "").strip().lower()
        if username.isdigit():  # user_id
            return cls.objects.filter(user_id=int(username)).first()
        return cls.objects.filter(username__iexact=username).first()

    @property
    def invited_users(self) -> QuerySet[User]:
        return User.objects.filter(deep_link=str(self.user_id), created_at__gt=self.created_at)

    @property
    def tg_str(self) -> str:
        if self.username:
            return f'@{self.username}'
        return f"{self.first_name} {self.last_name}" if self.last_name else f"{self.first_name}"


class Menu(models.Model):
    title = models.CharField(verbose_name='Catigoris name', max_length=255, unique=True)
    catigoris_position = models.PositiveSmallIntegerField(verbose_name='position for catigoris')
    images = models.ImageField(upload_to = 'menu_img/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menus"


class Product(models.Model):
    category = models.ForeignKey(Menu, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='tovarning ismi', max_length=255)
    image = models.ImageField(upload_to = 'product_img/')
    price = models.PositiveIntegerField(verbose_name='narx')
    description = models.TextField()
    position = models.PositiveSmallIntegerField(verbose_name='tovarning pozitsiyasi')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, verbose_name='telefon nomer', default='')
    date = models.DateTimeField(auto_now_add=True, blank=True)
    PAYMANTS = (
        ('Naxt', 'Naxt'),
        ('Click', 'Click'),
        ('PayMe', 'PayMe'),
        ('Terminal', 'Terminal'),
    )
    payment = models.CharField(verbose_name="To'lov turlari", choices=PAYMANTS, max_length=10, default='Naxt')
    STATES = (
        ('new', 'new'),
        ('pending', 'pending'),
        ('preparing', 'preparing'),
        ('delivering', 'delivering'),
        ('accepted', 'accepted'),
        ('declined', 'declined'),
        ('archivad', 'archivad'),
        ('cancellation', 'cancellation'),
        
    )
    states = models.CharField(verbose_name='buyurtmaning holati', choices=STATES, max_length=12)
    all_price = models.PositiveBigIntegerField(verbose_name="to'plam narx", default=0)

    def __str__(self):
       return self.user_id.username

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

class Cart(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    add_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts" 

    def __str__(self):
       return f'User name:"{self.order_id.user_id.username}"   Product: {self.add_product.name}'


class Branch(models.Model):
    name = models.CharField(verbose_name='Branch name', max_length=64)
    position_latitude = models.FloatField()
    position_longitude = models.FloatField()

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = "Branch"
        verbose_name_plural = "Branches" 