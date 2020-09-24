from django.shortcuts import render
from basicapp.forms import UserForm,UserProfileInfoForm
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
#from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    return render(request,'basicapp/index.html')

@login_required
def user_logout(request):
    logout(request)
    return render(request,'basicapp/logout.html',{}) 

@login_required
def special(request):
    return HttpResponse("You are logged in. Hurray! Enjoy the perks")

def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.is_staff = True
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basicapp/registration.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})        

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            
            else:
                return HttpResponse('ACCOUNT NOT ACTIVE')
        
        else:
            print("==============================")
            print("Username: {} Password : {}".format(username,password))
            return render(request,"basicapp/alert.html")

    else:
        return render(request,'basicapp/login.html',{})    

                 


