from django.shortcuts import render, HttpResponse, redirect
from django.template import context
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def registration(request):
    return render(request, 'register.html') 

def register(request):
    if request.method == 'POST':
        print(request.POST)
        errors = User.objects.RegistrationValidator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            newuser = User.objects.create(Fname=request.POST['Fname'], Lname=request.POST['Lname'], email=request.POST['email'], password=pw_hash)
            request.session['user'] = newuser.id
            print(newuser)
            print(pw_hash)
            return redirect('/dashboard')

def login(request):
    if request.method == 'POST':
        print(request.POST)
        print(User.id)
        errors = User.objects.LoginValidator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        request.session['user'] = User.objects.get(email=request.POST['logemail']).id
    
    return redirect('/dashboard')

def dashboard(request):
    CurrentUser = User.objects.get(id=request.session['user'])
    context = {
        'Thisuser': CurrentUser,
        'All_Jobs': Job.objects.all(),
        'All_Users': User.objects.all(),
    }
    return render(request, 'dashboard.html', context)

def addnewjob(request):
    if 'user' not in request.session:
        return redirect('/')
    return render(request, 'addjob.html')

def addjob(request):
    if 'user' not in request.session:
        return redirect('/')
    if request.method == 'POST':
        errors = Job.objects.JobValidator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/addnewjob')
        else:
            CurrentUser = User.objects.get(id=request.session['user'])
            newjob = Job.objects.create(title=request.POST['title'], desc=request.POST['desc'], location=request.POST['location'], user=CurrentUser)
            return redirect('/dashboard')

def addtouser(request, id):
    if 'user' not in request.session:
        return redirect('/')
    MyJob = Job.objects.get(id=id)
    user = User.objects.get(id=request.session['user'])
    MyJob.usersjob.add(user)
    return redirect('/dashboard')

def edit(request, id):
    if 'user' not in request.session:
        return redirect('/')
    MyJob = Job.objects.get(id=id)
    context = {
        'job': MyJob
    }
    return render(request, 'edit.html', context)

def update(request, id):
    if 'user' not in request.session:
        return redirect('/')
    if request.method == 'POST':
        errors = Job.objects.JobValidator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/edit/' +str(id))
        else:
            jobupdate = Job.objects.get(id=id)
            jobupdate.title = request.POST['title']
            jobupdate.desc = request.POST['desc']
            jobupdate.location = request.POST['location']
            jobupdate.save()
            return redirect('/dashboard')

def cancel(request, id):
    if 'user' not in request.session:
        return redirect('/')
    JobtoCancel = Job.objects.filter(id=id)
    if len(JobtoCancel) != 0:
        JobtoCancel[0].delete()
    return redirect('/dashboard')

def done(request, id):
    if 'user' not in request.session:
        return redirect('/')
    MyJob = Job.objects.get(id=id)
    user = User.objects.get(id=request.session['user'])
    MyJob.usersjob.remove(user)
    JobtoCancel = Job.objects.filter(id=id)
    if len(JobtoCancel) != 0:
        JobtoCancel[0].delete()
    return redirect('/dashboard')   

def view(request, id):
    Thisjob = Job.objects.get(id=id)
    context = {
        'job': Thisjob
    }
    return render(request, 'view.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')