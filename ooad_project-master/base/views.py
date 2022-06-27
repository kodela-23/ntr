from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from .models import User
import random
from django.core.mail import send_mail
# from django.shortcuts import render_to_response
from django.contrib.auth.hashers import make_password

# Create your views here.
def home(request):
    return render(request,'landingPage.html')

def register(request):
    if request.method=="POST":
        first_name = request.POST["first_name"]
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        address = request.POST["address"]
        try:
            User.objects.create_user(first_name=first_name,email=email,username=username,password=password,address=address)
        except:
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'Username Already Taken')
            return redirect('/')
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Registration Success')
        return redirect('/')
    else:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Invalid Request')
        return redirect('/')

def login(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        obj = authenticate(username=username,password=password)
        if obj is not None:
            auth.login(request,obj)
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'Login Success')
            return redirect("/app")
        else:
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'Invalid Username / Password')
            return redirect('/')
    else:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Invalid Request')
        return redirect('/')

def logout(request):
    auth.logout(request)
    storage = messages.get_messages(request)
    storage.used = True
    messages.info(request,'Logout Successfully')
    return redirect('/')

def changePassword(request):
    if request.method=="POST":
        username=request.POST["username"]
        obj = User.objects.get(username=username)
        number = random.randint(1000,9999)
        request.session["username"]=username
        request.session["otp_send"]=number
        msg = 'Hi '+obj.first_name+',\n\n\tOTP To change password: '+str(number)
        send_mail("Student Welfare - Password Change",msg,from_email='adityaintern11@gmail.com',recipient_list=[obj.email])
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'OTP Shared to your email id')
        return redirect('/validateOtp')
    return render(request,"startRecovery.html")

def validateOtp(request):
    if request.method=="POST":
        otp = request.POST["otp"]
        if int(otp)==int(request.session["otp_send"]):
            return redirect('/setNewPassword')
        else:
            return redirect('/ChangePassword')
    return render(request,'validateOtp.html')

def setNewPassword(request):
    if request.method=="POST":
        password=request.POST["new_password"]
        cnf_password=request.POST["cnf_password"]
        if password==cnf_password:
            password=make_password(password)
            obj = User.objects.get(username=request.session["username"])
            obj.password=password
            obj.save()
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'Password Changed Successfully')
            return redirect('/')
        else:
            return redirect('/setNewPassword')
    return render(request,'setNewPassword.html')