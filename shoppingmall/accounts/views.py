from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.http import HttpResponse
from .models import Buyer, Seller
from django.contrib.auth.decorators import login_required

#SIGNUP for BUYER
def buyersignup(request):
    if request.method =="POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username = request.POST['username'],
                    password = request.POST['password1']
                    )
                buyer = Buyer(user = user)
                buyer.address = request.POST['address']
                buyer.is_buyer = True
                buyer.save()    
                messages.add_message(request, messages.SUCCESS, 'Welcome to our Kingo Market, new buyer!')
                return redirect('home')
            except Exception as e:
                print(e)
                messages.add_message(request, messages.ERROR, 'ID already exists')
                return redirect('buyersignup')
                # user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
        messages.add_message(request, messages.ERROR, 'Passwords are not same')
    return render(request, 'buyersignup.html')

#SIGNUP for SELLER
def sellersignup(request):
    if request.method =="POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username = request.POST['username'],
                    password = request.POST['password1'],
                    )
                seller = Seller(user = user)
                seller.is_seller = True
                seller.phone = request.POST['phonenum']
                seller.save()
                messages.add_message(request, messages.SUCCESS, 'Welcome to our Kingo Market, new seller!')
                return redirect('home')
            except Exception as e:
                print(e)
                messages.add_message(request, messages.ERROR, 'ID already exists')
                return redirect('sellersignup')
        messages.add_message(request, messages.ERROR, 'Passwords are not same')
    return render(request, 'sellersignup.html')

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username = username, password = password)
        if user is not None:
            auth.login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Successfully Login')
            return redirect('home')
        else:
            messages.add_message(request, messages.ERROR, 'Login failed')
            return render(request, 'login.html')
    return render(request, 'login.html')

@login_required
def logout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.add_message(request, messages.SUCCESS, 'Successfully logout')
        return redirect('home')
    return render(request, 'home.html')