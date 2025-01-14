from django.urls import path
from readingTime import views


app_name = 'readingTime'

urlpatterns = [
    # TODO handle the URL mapping by name rather than by the URL
    # See Section 8.1
    path('', views.home, name='home'),
    path('signIn/', views.signIn, name='signIn'),
    path('myAccount/', views.myAccount, name='myAccount'),
    path('editProfile/', views.editProfile, name='editProfile'),
    path('changePassword/', views.changePassword, name='changePassword'),
    path('logOut/', views.logOut, name='logOut'),
    path('register/', views.register, name='register'),
    path('ContactUs/', views.ContactUs, name='ContactUs'),
    # we use slug since we have dashes
    path('category/<slug:category>', views.category, name='category'),
    path('category/', views.category, name='category'),
    path('book/', views.book, name='book'),
    path('book/<slug:book>', views.book, name='book'),
    
]
