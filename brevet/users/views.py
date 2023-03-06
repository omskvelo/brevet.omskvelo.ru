from hashlib import md5
from datetime import datetime

from django.conf import settings
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.views.decorators.cache import never_cache

from brevet_database.models import Application
from .forms import SignUpForm, SignUpVkForm
from .tokens import account_activation_token
from .models import User

@never_cache
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = settings.CSRF_TRUSTED_ORIGINS[1].split("://")[1]
            
            subject = f'Активируйте свою учетную запись на {current_site}'
            message = render_to_string('registration/account_activation_email.html', {
                'protocol' : request.scheme,
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            request.session['user_email'] = user.email
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@never_cache
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        return render(request, 'registration/account_activation_complete.html')
    else:
        return render(request, 'registration/account_activation_invalid.html')

@never_cache
def activation_sent(request):
    try:
        context = {'email': request.session['user_email']}
        return render(request, 'registration/account_activation_sent.html', context=context)
    except KeyError:
        raise Http404
        
@never_cache
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Пароль успешно изменен.')
            return redirect('index')
        else:
            messages.error(request, 'Невозможно сменить пароль.')
            context = {'form': form}
    else:
        form = PasswordChangeForm(request.user)
        context = {'form': form}
    return render(request, 'registration/change_password.html', context)

@never_cache
def profile(request):
    events = []
    for a in Application.objects.filter(user=request.user, active=True):
        events.append(a.event)

    context = {
        'events':events
    }
    return render(request, 'registration/profile.html', context)


@never_cache
def begin_auth_vk(request):
    vk_cookie = get_vk_cookie(request)
    if not vk_cookie:
        return redirect('login')
    vk_session = parse_cookie(vk_cookie)

    email = generate_vk_email(vk_session.get("mid"))
    user = User.objects.filter(email=email).first()
    if user:
        login(request, user)
        return redirect('index')
    else:
        url = reverse('signup_vk') + '?' + request.META['QUERY_STRING']
        return redirect(url)


@never_cache
def signup_vk(request):
    vk_cookie = get_vk_cookie(request)
    if not vk_cookie:
        return redirect('signup')
    vk_session = parse_cookie(vk_cookie)

    if request.method == 'POST':
        form = SignUpVkForm(request.POST)
        if form.is_valid():
            email = generate_vk_email(vk_session.get("mid"))
            existing_user = User.objects.filter(email=email).first()

            user = User()
            user.phone_number = form.cleaned_data['phone_number']
            user.email = email
            user.first_name = request.GET.get('first_name', '')
            user.last_name = request.GET.get('last_name', '')
            user.password = md5((user.email + user.first_name + user.last_name).encode('utf-8')).hexdigest()
            user.oauth = True
            user.is_active = True
            
            if existing_user or not user.first_name or not user.last_name:
                return redirect('index')
            
            print(user)
            user.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignUpVkForm()
    return render(request, 'registration/signup_vk.html', {'form': form})  

def generate_vk_email(mid:str):
    return "id" + mid + "@vk_oauth_" + md5(mid).hexdigest()

def get_vk_cookie(request):
    vk_cookie_name = f"vk_app_{settings.SOCIAL_AUTH_VK_OPENAPI_APP_ID}"
    vk_cookie = request.COOKIES.get(vk_cookie_name)
    if validate_vk_cookie(vk_cookie):
        return vk_cookie

def parse_cookie(cookie):
    result = {}
    for item in cookie.split("&"):
        key, value = item.split("=")
        result[key] = value

    return result

def validate_vk_cookie(cookie):
    if not cookie:
        return False
    if len(cookie.split('&sig=')) != 2:
        return False
    expire = int(parse_cookie(cookie).get('expire', '0'))
    if expire < datetime.now().timestamp():
        return False

    body, sig = cookie.split('&sig=')
    body = body.replace("&", "") + settings.SOCIAL_AUTH_VK_OPENAPI_SECRET
    body = body.encode('ascii')
    body_sig = md5(body).hexdigest()

    return body_sig == sig
