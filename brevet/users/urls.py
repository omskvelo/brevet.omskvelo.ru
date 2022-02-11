from django.urls import include, path

from . import views

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('actiovation_sent/', views.activation_sent, name="account_activation_sent"),
    path('activate/<str:uidb64>/<str:token>', views.activate, name="activate"),
    path('', include ('django.contrib.auth.urls')),
    ]