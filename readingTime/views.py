from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse
from readingTime.models import Category, Book
from readingTime.forms import RegisterForm

def home(request):
    category_list = Category.objects.all()
    context_dict = {}
    context_dict['categories'] = category_list

    if request.user.is_authenticated:
        return render(request, 'readingTime/home_logged_in.html', context=context_dict)
    else:
        return render(request, 'readingTime/home.html', context=context_dict)
                  
def category(request):
    return render(request,'readingTime/category.html')

def book(request):
    return render(request,'readingTime/book.html')

def signIn(request):
    # If the user is already logged in (temp -> redirects back to home page)
    if request.user.is_authenticated:
            return redirect('readingTime:home')

    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password1')

        # If username/password valid it returns an object
        user = authenticate(username=username, password=password)
        
        # If object returned (user recognised)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('readingTime:home')
            else:
                return HttpResponse("Rango account disabled!")
        else:
            # TODO message: username/password wrong
            messages.error(request, 'Either username or password invalid! Double check')
            return redirect('readingTime:signIn')
    else:
        form = AuthenticationForm()
        
    return render(request, 'readingTime/signIn.html', {'form': form})

def logOut(request):
    # when clicked, user logged out!
    logout(request)
    return redirect('readingTime:home')


def register(request):
    registered = False
    
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)

        # If the forms are valid
        if user_form.is_valid():

            user = user_form.save()
            # we load our profile instance
            user.refresh_from_db()
            user.profile.first_name = user_form.cleaned_data.get('first_name')
            user.profile.last_name = user_form.cleaned_data.get('last_name')
            user.profile.email = user_form.cleaned_data.get('email')
            user.save()

            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            registered = True
            if user:
                return redirect('readingTime:home')
            
        else:
            # Invalid form
            print(user_form.errors)
            #user_form = RegisterForm()
    else:
        # Blank form since we do not have an HTTP POST
        user_form = RegisterForm()

    
    return render(request,'readingTime/register.html',
                  context={'user_form': user_form,
                           'registered': registered})



