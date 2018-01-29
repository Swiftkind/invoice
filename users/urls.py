from django.urls import path
from users.views import *

urlpatterns = [
	path('signup/', SignupView.as_view(), name='signup'),
	path('signin/', SigninView.as_view(), name='signin'),
	path('signout/', SignoutView.as_view(), name='signout'),
	path('user/profile/<int:user_id>/', UserProfileView.as_view(), name='profile'),
	path('user/update/<int:user_id>/', UserUpdateView.as_view(), name='user_update'),
	#subusers
	path('user/delete_subuser/<int:user_id>/', SubUserDeleteView.as_view(), name='subuser_delete'),
	path('user/add_subuser/<int:user_id>/', SubUserAddView.as_view(), name='subuser_add'),
	path('user/subusers/', SubUsersView.as_view(), name='subusers'),
]