from django.urls import path
from users import views

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('signin/', views.SigninView.as_view(), name='signin'),
    path('signout/', views.SignoutView.as_view(), name='signout'),
    path('user/profile/<int:user_id>/', views.UserProfileView.as_view(), name='profile'),
    path('user/update/<int:user_id>/', views.UserUpdateView.as_view(), name='user_update'),
   ]