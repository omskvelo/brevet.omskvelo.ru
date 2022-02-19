from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.views.decorators.cache import never_cache

from brevet_database.models import Application, Event
from .forms import SignUpForm
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
            current_site = get_current_site(request)
            subject = f'Активируйте свою учетную запись на {current_site}'
            message = render_to_string('registration/account_activation_email.html', {
                'protocol' : request.scheme,
                'user': user,
                'domain': current_site.domain,
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
        user.profile.email_confirmed = True
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
    else:
        form = PasswordChangeForm(request.user)
        context = {'form': form}
    return render(request, 'registration/change_password.html', context)

@never_cache
def profile(request):
    events = []
    for a in Application.objects.filter(user=request.user):
        events.append(a.event)

    context = {
        'events':events
    }
    return render(request, 'registration/profile.html', context)
