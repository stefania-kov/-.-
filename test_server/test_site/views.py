from django.shortcuts import render, get_object_or_404, redirect
from .forms import RegisterForm, ApplicationForm
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Application, Course
from django.core.paginator import Paginator
from django.db.models import Q

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно!')
            return HttpResponseRedirect("/login/")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Неверный логин или пароль')
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('index')

@login_required
def applications(request):
    # Просмотр заявок пользователя
    user_applications = Application.objects.filter(user=request.user).order_by('-created_at')
    
    # Пагинация
    paginator = Paginator(user_applications, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'applications.html', {'applications': page_obj})

@login_required
def create_application(request):
    # Получаем все курсы из БД
    courses = Course.objects.all()
    
    # Если курсов нет, создаем
    if not courses:
        Course.objects.create(name='Основы алгоритмизации и программирования')
        Course.objects.create(name='Основы веб-дизайна')
        Course.objects.create(name='Основы проектирования баз данных')
        courses = Course.objects.all()
    
    if request.method == 'POST':
        course_id = request.POST.get('course')
        start_date = request.POST.get('start_date')
        payment_method = request.POST.get('payment_method')
        
        # Проверка что курс существует
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            messages.error(request, 'Выбранный курс не существует')
            return render(request, 'create_application.html', {'courses': courses})
        
        # Создаем заявку
        Application.objects.create(
            user=request.user,
            course_id=course_id,
            start_date=start_date,
            payment_method=payment_method,
            status='new'
        )
        messages.success(request, 'Заявка успешно создана!')
        return redirect('applications')
    
    return render(request, 'create_application.html', {'courses': courses})

@login_required
def add_feedback(request, app_id):
    application = get_object_or_404(Application, id=app_id, user=request.user)
    
    if application.status == 'completed' and request.method == 'POST':
        feedback = request.POST.get('feedback')
        application.feedback = feedback
        application.save()
        messages.success(request, 'Отзыв добавлен!')
    
    return redirect('applications')

def admin_panel(request):
    # Проверка на админа
    if request.user.username != 'Admin' or not request.user.is_authenticated:
        messages.error(request, 'Доступ запрещен')
        return redirect('index')
    
    applications = Application.objects.all().order_by('-created_at')
    
    # Фильтрация
    status_filter = request.GET.get('status', '')
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    # Поиск
    search = request.GET.get('search', '')
    if search:
        applications = applications.filter(
            Q(user__username__icontains=search) | 
            Q(course__name__icontains=search)
        )
    
    # Пагинация
    paginator = Paginator(applications, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.method == 'POST':
        app_id = request.POST.get('application_id')
        new_status = request.POST.get('status')
        application = get_object_or_404(Application, id=app_id)
        application.status = new_status
        application.save()
        messages.success(request, 'Статус обновлен!')
        return redirect('admin_panel')
    
    return render(request, 'admin_panel.html', {
        'applications': page_obj,
        'status_choices': Application.STATUS_CHOICES
    })

def robots (request):
    return render(request, 'robots.txt', content_type='text/plain')

def sitemap (request):
    return render(request, 'sitemap.xml', content_type='application/xml')