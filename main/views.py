from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.http import JsonResponse
from loginregistro.models import *
from .models import *
from .decorators import loginauth
import bcrypt

@loginauth
def index(request):
    context = {
        'users': User.objects.all()
    }
    return render(request, 'dashboard.html', context)

def newuser(request):
    if request.session['permission'] != 'admin':
        return redirect('/userdashboard')
    else:
        context={
            'permissions': Permission.objects.all()
        }
        return render(request, 'newuser.html', context)

def createuser(request):
    if request.method == 'POST':
        errors = User.objects.validator(request.POST)
    # En caso de que se devuelvan errores del validador, se guardan con messages y se redirecciona al formulario de registro para mostrarlos
        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect("/userdashboard/users/new")
        pwhash = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()
        nuevo_usuario = User.objects.create(
            first_names=request.POST["first_names"],
            last_names=request.POST["last_names"],
            email=request.POST["email"],
            password=pwhash,
            dateborn=request.POST["dateborn"],
            permission= Permission.objects.get(permissionLevel=request.POST["permission"])
        )
        messages.success(request, "Registered in successfully")
        return redirect("/userdashboard")

def showuser(request, id):
    context={
        'user': User.objects.get(id=id)
    }
    return render(request, 'showuser.html', context)

def newmessage(request):
    newmessage= Message.objects.create(
        content=request.POST["message"],
        user=User.objects.get(id=request.session["user"]),
        destiny= User.objects.get(id=request.POST["destiny"])
    )
    return redirect("/userdashboard/users/" + request.POST['destiny'])

def newcomment(request):
    newcomment= Comment.objects.create(
        content=request.POST["comment"],
        message=Message.objects.get(id=request.POST["message"]),
        user=User.objects.get(id=request.session["user"])
    )
    return redirect("/userdashboard/users/" + request.POST['destiny'])

@loginauth
def editself(request):
    context={
        'user': User.objects.get(id=request.session["user"])
    }
    return render(request, 'editself.html',context)

def editadmin(request, id):
    context={
        'user': User.objects.get(id=id),
        'permissions': Permission.objects.all()
    }
    return render(request, 'editself.html',context)

@loginauth
def editinfo(request):
    if request.session['admin'] == True:
        user=User.objects.get(id=request.POST["user"])
        user.permission= Permission.objects.get(permissionLevel=request.POST["permission"])
    else:
        user=User.objects.get(id=request.session["user"])
    user.first_names=request.POST["first_names"]
    user.last_names=request.POST["last_names"]
    user.email=request.POST["email"]
    user.dateborn=request.POST["dateborn"]
    user.save()
    return redirect("/userdashboard/users/"+ str(user.id))

@loginauth
def editpass(request):
    if request.session['admin'] == True:
        user=User.objects.get(id=request.POST["user"])
    else:
        user=User.objects.get(id=request.session["user"])
    pwhash=bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()
    user.password=pwhash
    user.save()
    return redirect("/userdashboard/users/"+  str(user.id))

