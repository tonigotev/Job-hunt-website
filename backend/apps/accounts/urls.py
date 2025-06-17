from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('me/', views.UserDetailView.as_view(), name='user_detail'),
    path('me/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('me/upgrade-to-company/', views.UpgradeToCompanyView.as_view(), name='upgrade_to_company'),
] 