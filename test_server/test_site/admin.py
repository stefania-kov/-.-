from django.contrib import admin
from .models import Application
from admin_interface.models import Theme


# Удаление модели Theme из админки (admin-interface)
admin.site.unregister(Theme)



admin.site.register(Application)