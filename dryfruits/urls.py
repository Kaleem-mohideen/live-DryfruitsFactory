"""dryfruits URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path as url
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.views.generic import RedirectView
from users.forms import *
from django.views.static import serve
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    url(r'^favicon\.ico$',RedirectView.as_view(url='static/shop/img/favicon/favicon.png')),
    path('payments/', include('payments.urls')),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', user_views.logoutHandle, name='logout'),
    path("password-reset/", user_views.password_reset_request, name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name = "users/password_reset_confirm.html"), name ='password_reset_confirm'),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "users/password_reset_complete.html"), name ='password_reset_complete'),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]#+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
