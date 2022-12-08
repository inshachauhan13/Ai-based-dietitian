from django.contrib import admin
from django.urls import path,include
from .views import *
urlpatterns = [
    path('', home,name = "home"),
    path('about/',about, name = 'about'),
    path('faq/',faq, name = 'faq'),
    path('experts/',experts, name = 'experts'),
    path('nutrition/',nutrition,name='nutrition'),
    path('food/',food,name='food'),
    path('input/', input_,name = "input_"),
    path('faqpage/', faqpage_,name = "faqpage_"),
    
    path('process/',process_input,name = 'process'),
    path('search/',search,name='search-bar-down')

]








































