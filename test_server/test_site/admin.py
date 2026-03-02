# test_site/admin.py
from django.contrib import admin
from .models import CustomUser, Course, Application

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'fio', 'phone', 'is_staff')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email', 'fio', 'phone')
    ordering = ('-id',)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'start_date', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('user__username', 'user__fio', 'course__name', 'feedback')
    list_editable = ('status',)
    list_per_page = 20
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Информация о заявке', {
            'fields': ('user', 'course', 'start_date', 'payment_method')
        }),
        ('Статус и отзыв', {
            'fields': ('status', 'feedback')
        }),
    )