from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название компании")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    email = models.EmailField(blank=True, verbose_name="Email")
    website = models.URLField(blank=True, verbose_name="Сайт")
    address = models.TextField(blank=True, verbose_name="Адрес")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='companies')
    
    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name

class Contact(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='contacts', verbose_name="Компания")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    email = models.EmailField(blank=True, verbose_name="Email")
    position = models.CharField(max_length=100, blank=True, verbose_name="Должность")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Pipeline(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название воронки")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Воронка продаж"
        verbose_name_plural = "Воронки продаж"
    
    def __str__(self):
        return self.name

class Stage(models.Model):
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, related_name='stages')
    name = models.CharField(max_length=100, verbose_name="Название этапа")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    
    class Meta:
        verbose_name = "Этап воронки"
        verbose_name_plural = "Этапы воронки"
        ordering = ['order']
    
    def __str__(self):
        return f"{self.pipeline.name} - {self.name}"

class Deal(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
    ]
    
    title = models.CharField(max_length=255, verbose_name="Название сделки")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='deals')
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True, related_name='deals')
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Сумма")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name="Приоритет")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_deals')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_deals')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Сделка"
        verbose_name_plural = "Сделки"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('call', 'Звонок'),
        ('meeting', 'Встреча'),
        ('email', 'Email'),
        ('task', 'Задача'),
        ('note', 'Заметка'),
    ]
    
    type = models.CharField(max_length=10, choices=ACTIVITY_TYPES, verbose_name="Тип активности")
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    description = models.TextField(blank=True, verbose_name="Описание")
    due_date = models.DateTimeField(null=True, blank=True, verbose_name="Срок выполнения")
    completed = models.BooleanField(default=False, verbose_name="Выполнено")
    completed_at = models.DateTimeField(null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='activities')
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True, related_name='activities')
    deal = models.ForeignKey(Deal, on_delete=models.SET_NULL, null=True, blank=True, related_name='activities')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='activities')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Активность"
        verbose_name_plural = "Активности"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_type_display()}: {self.title}"
    
    def save(self, *args, **kwargs):
        if self.completed and not self.completed_at:
            self.completed_at = timezone.now()
        elif not self.completed:
            self.completed_at = None
        super().save(*args, **kwargs)
