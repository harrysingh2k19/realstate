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
    if request.user.is_authenticated :
        return redirect('dashboard')
    else:
        if request.method == 'GET':
            return render(request, 'signin.html',{'user_form': AuthenticationForm(),'login':True})
        else:
            user_input = form_user(data=request.POST)
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user is None:
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
            user.username = temp
            user.set_password(user.password)
            user.save()
            return redirect("index")
        else:
            return redirect("index")


def new_request(request):
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
                return redirect("dashboard")
            else:
                return HttpResponseRedirect('/')
    else:
        return redirect("dashboard")

def dashboard(request):
    if request.user.is_authenticated :
        if model_admin.objects.filter(user=request.user): #Admin
            user_data = model_info.objects.all()
            return render(request, 'dashboard.html',{'user_data':user_data, 'admin':True})
            # return HttpResponse("bhai ho nhi raha h " )
        else:# for genral user
            user_data = model_info.objects.filter(user=request.user)
            print(len(user_data))
            if len(user_data)==0:
                return render(request, 'dashboard.html',{'user_data':False})
            else:
                return render(request, 'dashboard.html',{'user_data':user_data})

    else:
        return redirect("index")

# def details(request, pk):
#     if request.user.is_authenticated :
#         if request.method == 'GET':
#             if model_info.objects.all().filter(id =pk ):# For Admin
#                 if model_admin.objects.filter(user=request.user):
#                     article = model_info.objects.all().filter(id =pk )
#                     return render(request, 'details.html',{'user_data':article, 'admin':True,'user_form':form_details})
#                 else: # user
#                     article = model_info.objects.all().filter(id =pk )
#                     return render(request, 'details.html',{'user_data':article, 'admin':False})
#             else:
#                 return render(request, 'dashboard.html',{'user_data':False, 'admin':True})
#         elif request.method == 'Post' :
#             print("post to h bhai")
#             user_input = form_info(data=request.POST)
#             if user_input.is_valid():
#                 print("bhai aaya to shi hu" )
#                 user = user_input.save(commit=False)
#                 user.Assign = request.user
#                 user.save()
#                 return HttpResponse("Bhai Game ho gaya")
#             else:
#                 return HttpResponse("Bhai Game ho gaya")
#
#     else:
#         return HttpResponse("Bhai Game ho gaya")

def details(request, pk):
    if request.method == 'GET':
        if model_info.objects.all().filter(id =pk ):# For Admin
            if model_admin.objects.filter(user=request.user):
                article = model_info.objects.all().filter(id =pk )
                for a in article : print(a.id)
                return render(request, 'details.html',{'user_data':article, 'admin':True,'user_form':form_details})
            else: # user
                article = model_info.objects.all().filter(id =pk )
                article2 = model_assign.objects.all().filter(id =pk )
                return render(request, 'details.html',{'user_data':article, 'admin':False, 'user_dataa':article2})
        else:
            return render(request, 'dashboard.html',{'user_data':False, 'admin':True})
    else :
        print("post to h bhai")
        post = dict(request.POST)
        article = model_info.objects.all().filter(id =pk )
        for a in article : post['Ticket'] = a.id
        post['request_assigned'] =request.user
        user_input = form_details(data = post)
        if user_input.is_valid():
            print("bhai aaya to shi hu" )
            user = user_input.save(commit=False)
            user.Assign = request.user
            user.save()
            return redirect("dashboard")
        else:
            print(user_input.errors)
            return redirect("dashboard")




def signout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

    # user_form = form_user
    # print("m registarrti mhu ")
    # return render(request, 'registration.html',{'user_form': user_form})
