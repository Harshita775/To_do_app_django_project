from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import *

# from django.http import HttpResponse

# Create your views here.

def homePage(request):
    return render(request, 'tasks/home.html')

def loginPage(request):

    if request.user.is_authenticated:
        return redirect('ulist')
    
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exists')
            return render(request, 'tasks/login_register.html')  # Return immediately
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('ulist')
        else:
            messages.error(request, 'Username or Password does not exist')
          
    context = {'page':page}
    return render(request, 'tasks/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    # page = 'register'

    if request.user.is_authenticated:
        return redirect('ulist')
    
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('ulist')
        else:
            messages.error(request, 'An error occured during registration')

    return render(request, 'tasks/login_register.html', {'form':form})

@login_required(login_url='login')
def userList(request):
    tasks = Task.objects.filter(user = request.user)

    number = Task.objects.filter(complete=False, user=request.user).count()

    search_input = request.GET.get('search-bar') or ''
    if search_input:
        tasks = Task.objects.filter(title__startswith = search_input,  user=request.user)

    context = {'tasks':tasks, 'number':number, 'search_input':search_input}
    return render(request, 'tasks/list.html', context)


@login_required(login_url='login')
def createTask(request):
    form = TaskForm()

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
        return redirect('ulist')
    
    context = {'form':form}
    return render(request, 'tasks/create_task.html', context)

@login_required(login_url='login')
def viewTask(request, pk):
    task = Task.objects.get(id=pk)
    context = {'task':task}
    return render(request, 'tasks/view_task.html', context)


@login_required(login_url='login')
def updateTask(request, pk):
    task = Task.objects.get(id=pk)

    form = TaskForm(instance=task)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('ulist')

    context = {'form':form}

    return render(request, 'tasks/update_task.html', context)


@login_required(login_url='login')
def deleteTask(request, pk):
    item = Task.objects.get(id=pk)

    if request.method  == "POST":
        item.delete()
        return redirect('ulist')
    
    context = {'item':item}
    return render(request, 'tasks/delete.html', context)