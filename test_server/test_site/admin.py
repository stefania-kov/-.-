from django.contrib import admin
from .models import Application
from admin_interface.models import Theme
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group

# Скрываем Groups из админки
admin.site.unregister(Group)
# Удаление модели Theme из админки (admin-interface)
admin.site.unregister(Theme)



admin.site.register(Application)