from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from django.contrib.auth import views as auth_views
from django.db.models import Q
# from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import BadHeaderError#, send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
# from django.http import HttpResponse,JsonResponse
# from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from .utils import send_mail
from django.conf import settings
from .models import *
from django.contrib.auth import get_user_model
# from shop.models import Customer


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        print("here in register")
        if form.is_valid():
            print("here in form valid user")
            user = form.save()

            user.refresh_from_db()
            # load the profile instance created by the signal
            phone =form.cleaned_data.get('mobile_number')
            user.phone_number = phone
            user.save()
            raw_password = form.cleaned_data.get('password1')

            # login user after signing up
            user = authenticate(username=user.username, password=raw_password)
            if user is not None:
                print("here in login user")
                login(request, user)
                print('login')
            else:
                messages.error(request, "Invalid credentials! Please try again")
                redirect_to = request.META.get('HTTP_REFERER', '/')
                return redirect(redirect_to)

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            print("redirect")
            print(request.get_full_path())
            messages.success(request, f'Account created for {username}!')
            redirect_to = request.META.get('HTTP_REFERER', '/')
            return redirect(redirect_to)
    else:
        print("here in register else post")
        form = UserRegisterForm()
    # if request.method == 'POST' and request.is_ajax():
    #     return JsonResponse(serializers.serialize('json', form), safe=False)
    print("here in render")
    return render(request, 'users/register.html', {'form': form})


def logoutHandle(request):
    if request.user is not None:
        logout(request)
        messages.success(request, "successfully Logged Out")
    else:
        messages.error(request, "Invalid Request User! Please try again")
    return redirect('shop:ShopHome')

def password_reset_request(request):
    if request.method == "POST":
        UserModel = get_user_model()
        domain = request.headers['Host']
        data = request.POST.get('email', None)
        associated_users = UserModel.objects.filter(Q(email=data))
        # You can use more than one way like this for resetting the password.
        # ...filter(Q(email=data) | Q(username=data))
        # but with this you may need to change the password_reset form as well.
        print(data)
        print(associated_users)
        print(domain)
        if associated_users.exists():
            for user in associated_users:
                subject = "Password Reset Requested"
                email_template_name = "users/password_reset_email.html"
                c = {
                    "email": user.email,
                    'domain': domain,
                    'site_name': 'DryFruitsFactory',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    'header_logo': 'shop/img/header-logo.png',
                }
                message = render_to_string(email_template_name, c)
                try:
                    # send_mail(subject, message, 'kaleemmohideen786@gmail.com', [user.email], fail_silently=False)
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
                    # user.email_user(subject, message)
                    messages.success(request, ('Email for Password-reset sent successfully.'))
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return redirect('password_reset_done')
        else:
            messages.success(request, ('Email is not in Entry. Please Enter correct details'))
            return redirect('shop:ShopHome')
    messages.error(request, "Invalid Request User! Please try again")
    return redirect('shop:ShopHome')


