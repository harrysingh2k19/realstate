from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,  AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import form_user,form_info, form_details
from .models import model_info, model_admin, model_assign
from django import forms
from django.http import HttpResponse
import datetime

def index(request):
    if request.user.is_authenticated :# To Check user logged redirect to dashboard
        return redirect('dashboard')
    else:
        if request.method == 'GET': #  if it is not POST some data then it want data GET
            return render(request, 'signin.html',{'user_form': AuthenticationForm(),'login':True})
        else:  # If request id POST
            user_input = form_user(data=request.POST)
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user is None: # if not authenticated
                return render(request, 'signin.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
            else:
                login(request, user)
                return redirect('dashboard')

def signup(request):
    if request.method == 'GET':
        user_form = form_user()
        return render(request, 'registration.html',{'user_form': form_user,'register':True})
    if request.method == 'POST':
        user_input = form_user(data=request.POST)
        if user_input.is_valid():
            user = user_input.save()
            temp=user_input.cleaned_data['email']
            user.username = temp                     # to allocated the email id as username
            user.set_password(user.password)
            user.save()
            return redirect("index")
        else:
            return redirect("index")


def new_request(request):  # to raise new ticket
    if request.user.is_authenticated :
        if request.method == 'GET':
            user_form = form_info
            return render(request, 'registration.html',{'user_form': user_form,'register':False})
        else:
            user_input = form_info(data=request.POST)
            if user_input.is_valid():
                user = user_input.save(commit=False)
                user.user = request.user
                user.save()
                return redirect("dashboard") # after save data return dashboard
            else:
                print(user_input.errors)        # If got anny error
                return HttpResponseRedirect('/')
    else: # if user not logged
        return redirect("dashboard")

def dashboard(request):
    if request.user.is_authenticated :
        if model_admin.objects.filter(user=request.user):   # Admin
            user_data = model_info.objects.exclude(request_status = 'Complete')    #print all entry except with complete status
            return render(request, 'dashboard.html',{'user_data':user_data, 'admin':True})
        else:                                               # for genral user
            user_data = model_info.objects.filter(user=request.user) # all data of raised by the user
            if len(user_data)==0:
                return render(request, 'dashboard.html',{'user_data':False})
            else:
                return render(request, 'dashboard.html',{'user_data':user_data})
    else:
        return redirect("index") # if user not logged

def details(request, pk):
    if request.method == 'GET':                    # if page not sending any data
        if model_info.objects.all().filter(id =pk ):# For Admin
            if model_admin.objects.filter(user=request.user):
                article = model_info.objects.all().filter(id =pk )
                return render(request, 'details.html',{'user_data':article, 'admin':True,'user_form':form_details})
            else:                                   # user
                article = model_info.objects.all().filter(id =pk )
                article2 = model_assign.objects.all().filter(id =pk )
                return render(request, 'details.html',{'user_data':article, 'admin':False, 'user_dataa':article2})
        else:
            return render(request, 'dashboard.html',{'user_data':False, 'admin':True})
    else :                                                    # post
        user_input = form_details(data=request.POST)
        if user_input.is_valid():
            article = model_info.objects.all().filter(id =pk )
            for a in article:  # save valuse in model_info
                a.request_status = user_input.cleaned_data['request_status']
                a.request_remark = user_input.cleaned_data['request_remark']
                for b in model_admin.objects.filter(user=request.user): a.request_assigned = b
                a.save()
            return redirect("dashboard")
        else:
            return redirect("dashboard")

def signout(request):   # for signout
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')
