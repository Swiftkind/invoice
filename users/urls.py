from django.contrib.auth import views as auth_views
from django.urls import path


from users import views



urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('signin/', views.SigninView.as_view(), name='signin'),
    path('signout/', views.SignoutView.as_view(), name='signout'),
    path('user/profile/<int:user_id>/', views.UserProfileView.as_view(), name='profile'),
    path('user/update/<int:user_id>/', views.UserUpdateView.as_view(), name='user_update'),
    path('user/settings/<int:user_id>/', views.UserSettingView.as_view(), name='user_setting'),
    path('user/change_password/<int:user_id>/', views.UserChangePassword.as_view(), name='change_password'),

    # Reset Password
    path('password_reset/', auth_views.password_reset, name='password_reset'),
    path('password_reset/done/', auth_views.password_reset_done, name='password_reset_done'),
    path('reset/<str:uidb64>/<slug:token>/',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', auth_views.password_reset_complete, name='password_reset_complete'),
   ]