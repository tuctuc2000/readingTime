from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from readingTime.models import Category, Book, Profile, Contact
from readingTime.forms import RegisterForm, EditProfileForm, ContactForm

def home(request):
    category_list = Category.objects.all()
    context_dict = {}
    context_dict['categories'] = category_list
    
    if request.user.is_authenticated:
        context_dict['logged_in'] = True
    else:
        context_dict['logged_in'] = False

    response = render(request, 'readingTime/home.html', context=context_dict)
    
    return response
                  
def category(request, category_name='Default category'):
    # we get all books which are linked to the given category name (i.e.: Fiction)
    category_name = str(request.get_full_path)
    # gets the category name from the url
    try:
        category_name = (category_name.split("?",1)[1]).replace("'>>","")
    except:
        category_name = "temporary"
    # gets the books stored in the given category
    books_list = Book.objects.filter(category__name=category_name)
    
    # Checks if a user has logged in
    if request.user.is_authenticated:
        logged_in = True
    else:
        logged_in = False
    
    return render(request,'readingTime/category.html', context={'logged_in': logged_in,
                                                                'books': books_list,
                                                                'category_name': category_name})

def book(request, book_title='Default Title'):
    book_title = str(request.get_full_path)
    # gets the book title from the URL
    try:
        book_title = (book_title.split("?",1)[1]).replace("'>>","").replace("%20"," ")
        # gets the author from the book_title
        author = Book.objects.get(title=book_title).author
        # gets the synopsis from the book_title
        synopsis = Book.objects.get(title=book_title).synopsis
        # gets the personal rating from the book_title
        personal_rating = Book.objects.get(title=book_title).personal_rating
        # gets the global rating from the book_title
        global_rating = Book.objects.get(title=book_title).global_rating
        # gets if the book is in the read_list
        in_read_list = Book.objects.get(title=book_title).in_read_list
    except:
        book_title = "temporary"
        author = "temporary author"
        synopsis = "temporary synopsis"
        personal_rating = global_rating = 5
        in_read_list = False

    # Checks if a user has logged in
    if request.user.is_authenticated:
        logged_in = True
    else:
        logged_in = False
    
    return render(request,'readingTime/book.html', context={'logged_in': logged_in,
                                                            'title': book_title,
                                                            'author': author,
                                                            'synopsis': synopsis,
                                                            'personal_rating': personal_rating,
                                                            'global_rating': global_rating,
                                                            'in_read_list': in_read_list})

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
            # message to display if login unsuccesful
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
            # if user:
            return redirect('readingTime:home')

        else:
            # Invalid form
            # messages.error(request, 'Form contains errors. Double check')
            print(user_form.errors)
            messages.error(request, 'Form contains errors. Double check')
            # user_form = user_form.errors
            #user_form = RegisterForm()
    else:
        # Blank form since we do not have an HTTP POST
        user_form = RegisterForm()
        
    return render(request,'readingTime/register.html',
                  context={'user_form': user_form,
                           're': registered})

def myAccount(request):
    # Current user object
    user = request.user
    email = Profile.objects.get(user=user).email
    first_name = Profile.objects.get(user=user).first_name
    last_name = Profile.objects.get(user=user).last_name
    username = Profile.objects.get(user=user).user

    return render(request, 'readingTime/myAccount.html', context={'first_name': first_name,
                                                                  'last_name': last_name,
                                                                  'email': email,
                                                                  'username': user})

def editProfile(request):
    
    if request.method == 'POST':
        user_form = EditProfileForm(request.POST, instance=request.user)

        # If the form is valid
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
            
            return redirect('readingTime:myAccount')
            
        else:
            # Failed to update profile
            messages.error(request, 'Failed to Update your profile. Try Again!')
    else:
        # Blank form since we do not have an HTTP POST
        user_form = EditProfileForm(instance=request.user)
    
    
    return render(request,'readingTime/editProfile.html',
                  context={'user_form': user_form})

def changePassword(request):
    
    if request.method == 'POST':
        user_form = PasswordChangeForm(data=request.POST, user=request.user)

        # If the form is valid
        if user_form.is_valid():
            user_form.save()
            update_session_auth_hash(request, user_form.user)
            
            return redirect('readingTime:myAccount')
            
        else:
            # Invalid password change
            messages.error(request, 'failed to change the password. Try Again!')
    else:
        # Blank form since we do not have an HTTP POST
        user_form = PasswordChangeForm(user=request.user)
        
    return render(request,'readingTime/changePassword.html',
                  context={'user_form': user_form})

def ContactUs(request):
    if request.user.is_authenticated:
        logged_in = True
    else:
        logged_in = False

    if request.method == 'POST':
        user_form = ContactForm(request.POST,request.FILES)
        if user_form.is_valid():
            Contact = user_form.save()
            # we load our profile instance

            Contact.BookID = user_form.cleaned_data.get('BookID')
            Contact.BookTitle = user_form.cleaned_data.get('BookTitle')
            Contact.Author= user_form.cleaned_data.get('Author')
            Contact.UploadImage=user_form.cleaned_data.get('UploadImage')
            Contact.save()

            return redirect('readingTime:home')
        else:

            print(user_form.errors)
            messages.error(request, 'Form contains errors. Double check')





    else:
        # Blank form since we do not have an HTTP POST
        user_form = ContactForm()

    context_dict = {
        'user_form': user_form,
        'logged_in': logged_in

    }
    return render(request,"readingTime/ContactUs.html",context=context_dict)

