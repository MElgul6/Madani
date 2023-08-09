from django.urls import path
from account.views import (CustomLoginView,RegisterView, ActiveAccountView,
                        Home, search_user, edit, update, delete, CustomPasswordChangeView, CustomPasswordChangeDoneView)
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from . import views

 
urlpatterns = [
    path('login/', CustomLoginView.as_view(),name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path('logout/', LogoutView.as_view(), name="logout_page"),
    path('activate/<str:uidb64>/<str:token>/', ActiveAccountView.as_view(), name="activate"),
    path('home/', Home.as_view(), name="home"),
    path('reset_password/', auth_views.PasswordResetView.as_view(),name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('home/search_user/', search_user, name='search_user'), 
    path('edit', views.edit, name='edit'),
    path('update/<int:id>', views.update, name='update'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('password-change/', CustomPasswordChangeView.as_view(), name='change_password'), 
    path('password_change/done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),  
]

 





