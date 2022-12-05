from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView, name='home'),
    path('analytics/', views.AnalyticsPageView, name='analytics'),
    path('menu/', views.MenuPageView.as_view(), name='menu'),  
    path('menu/menu-home', views.MenuHomePageView, name='menu-home'),
    path('menu/drinks/<str:pk>', views.DrinksPageView, name='drinks'),
    path('menu/<int:pk>/', views.ItemDetailView, name='item-detail'),
    path('locations/', views.LocationView, name='locations'),
    path('checkout/', views.CheckoutPageView, name='checkout'),
    path('search/', views.SearchPageView, name='search'),
]
