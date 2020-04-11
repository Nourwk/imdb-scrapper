from django.urls import path
from . import views

app_name = 'Scrapping'

urlpatterns = [
    path('', views.applook),
    #path('', include('product.urls')),

]
