# Here we import the path function and the views module
from django.urls import path, include  # include is for viewsets
from . import views
from django.contrib import admin

#for the newsletter
from .views import EBookSignupView




# Now describe our url patterns forthe email /comniguring Active Campaign
urlpatterns = [
    # DetailView - shows question details and voting form
    path('ebook-signup', EBookSignupView.as_view()),
    
]

