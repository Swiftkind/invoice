from django.urls import path
from accounts import views

urlpatterns = [
	path('', views.IndexView.as_view(), name='index'),
	path('signup/', views.SignupView.as_view(), name='signup'),
	path('signin/', views.SigninView.as_view(), name='signin'),
	path('signout/', views.SignoutView.as_view(), name='signout'),
]