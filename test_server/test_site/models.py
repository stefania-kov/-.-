from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, verbose_name='Телефон')
    fio = models.CharField('ФИО', max_length=150)

    def __str__(self):
        return self.username

# ДОБАВЬТЕ ЭТУ МОДЕЛЬ
class Course(models.Model):
    name = models.CharField('Название курса', max_length=200)
    
    def __str__(self):
        return self.name

class Application(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'Идет обучение'),
        ('completed', 'Обучение завершено'),
    ]
    
    PAYMENT_CHOICES = [
        ('cash', 'Наличными'),
        ('transfer', 'Перевод по номеру телефона'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')  # ТЕПЕРЬ ЭТО РАБОТАЕТ
    start_date = models.DateField('Желаемая дата начала')
    payment_method = models.CharField('Способ оплаты', max_length=20, choices=PAYMENT_CHOICES)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    feedback = models.TextField('Отзыв', blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.course.name}"