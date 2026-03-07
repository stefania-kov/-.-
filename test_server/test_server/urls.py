"""
URL configuration for test_server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""
URL configuration for test_server project.
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings  # Добавьте этот импорт
from django.conf.urls.static import static  # Добавьте этот импорт
from django.views.static import serve  # Добавьте этот импорт
from test_site import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('applications/', views.applications, name='applications'),
    path('add_feedback/<int:app_id>/', views.add_feedback, name='add_feedback'),
    path('logout/', views.logout_user, name='logout'),
    path('create_application/', views.create_application, name='create_application'),
    path('robots.txt/', views.robots, name='robots'),
    path('sitemap.xml/', views.sitemap, name='sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Добавляем заголовки кэширования для медиа
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
            'show_indexes': False,
        }),
    ]