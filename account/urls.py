from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/scrap/<int:user_id>/', views.ProfileVoteListView.as_view(template_name='wyw/profile_scrap.html'), name='profile_scrap'),
    path('profile/', views.profile, name='profile'),
    path('follow/<int:user_id>/', views.follow, name='follow'),
    path('serializers/userpost', views.UserPost.as_view()),
    path('serializers/userpost/<int:pk>/', views.UserDetailPost.as_view()),
    path('serializers/profilepost', views.ProfilePost.as_view()),
    path('serializers/profilepost/<int:pk>/', views.ProfileDetailPost.as_view()),


]