from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class Flat(models.Model):
    created_at = models.DateTimeField(
        'Когда создано объявление',
        default=timezone.now,
        db_index=True)

    new_building = models.BooleanField("Новостройка", null=True, db_index=True)
    description = models.TextField('Текст объявления', blank=True)
    price = models.IntegerField('Цена квартиры', db_index=True)

    town = models.CharField(
        'Город, где находится квартира',
        max_length=50,
        db_index=True)
    town_district = models.CharField(
        'Район города, где находится квартира',
        max_length=50,
        blank=True,
        help_text='Чертаново Южное')
    address = models.TextField(
        'Адрес квартиры',
        help_text='ул. Подольских курсантов д.5 кв.4')
    floor = models.CharField(
        'Этаж',
        max_length=3,
        help_text='Первый этаж, последний этаж, пятый этаж')

    rooms_number = models.IntegerField(
        'Количество комнат в квартире',
        db_index=True)
    living_area = models.IntegerField(
        'количество жилых кв.метров',
        null=True,
        blank=True,
        db_index=True)

    has_balcony = models.NullBooleanField('Наличие балкона', db_index=True)
    active = models.BooleanField('Активно-ли объявление', db_index=True)
    likes = models.ManyToManyField(User, related_name="like_by_users",
                                   verbose_name="Кто лайкнул", blank=True)
    construction_year = models.IntegerField(
        'Год постройки здания',
        null=True,
        blank=True,
        db_index=True)

    def __str__(self):
        return f'{self.town}, {self.address} ({self.price}р.)'


class Complaint(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,
                               null=True, verbose_name="Кто жаловался",
                               related_name="complaints")
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE,
                             blank=True, null=True,
                             verbose_name="Квартира на которую жаловались",
                             related_name="complaints")

    text = models.TextField('Текст жалобы', blank=True)

    def __str__(self):
        return self.text


class Owner(models.Model):
    name = models.CharField("ФИО", max_length=30)
    phonenumber = models.CharField('Номер владельца', max_length=20)
    pure_phonenumber = PhoneNumberField('Нормализованный номер телефона',
                                        region="RU", blank=True)
    apartments = models.ManyToManyField(Flat, related_name="owners",
                                        blank=True,
                                        verbose_name="Квартира в собственности"
                                        )

    def __str__(self):
        return self.name
