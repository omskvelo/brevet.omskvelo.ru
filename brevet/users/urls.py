from django.urls import include, path

from . import views

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('activation_sent/', views.activation_sent, name="account_activation_sent"),
    path('activate/<str:uidb64>/<str:token>', views.activate, name="activate"),
    path('change_password/', views.change_password, name="change_password"),
    path('profile/', views.profile, name="user_profile"),
    path('social/vk/begin/', views.begin_auth_vk, name="begin_auth_vk"),
    path('social/vk/signup/', views.signup_vk, name="signup_vk"),
    path('', include ('django.contrib.auth.urls')),
    ]