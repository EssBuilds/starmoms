from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Task, Child
from .forms import TaskForm, ChildForm, RegisterForm

def home(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user)
        children = Child.objects.filter(user=request.user)
        return render(request, 'todo/home.html', {'tasks': tasks, 'children': children})
    return render(request, 'todo/login.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('todo:home')
    else:
        form = RegisterForm()
    return render(request, 'todo/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Successfully logged in!")
            return redirect('todo:home')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'todo/login.html')

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect('todo:login')

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, "Task added!")
            return redirect('todo:home')
    return redirect('todo:home')

@login_required
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    task.delete()
    messages.success(request, "Task deleted!")
    return redirect('todo:home')
