from django.urls import path
from .views import HomePageView, MenuPageView
from . import views

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('manager/', views.ManagerPageView, name='manager'),
    path('menu/', MenuPageView.as_view(), name='menu'),  
    path('menu/espresso/', views.EspressoPageView, name="espresso"),
    path('menu/brewed/', views.BrewedPageView, name="brewed"),
    path('menu/blended/', views.BlendedPageView, name="blended"),
    path('menu/tea/', views.TeaPageView, name="tea"),
    path('menu/other/', views.OtherPageView, name="other"),
]
