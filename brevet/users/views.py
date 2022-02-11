from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .forms import SignUpForm
from .tokens import account_activation_token

from .forms import SignUpForm
from .models import User


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            print ('Form is valid')
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = f'Активируйте свою учетную запись на {current_site}'
            message = render_to_string('users/account_activation_email.html', {
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
    return render(request, 'users/signup.html', {'form': form})


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
        login(request, user)
        return redirect('index')
    else:
        return render(request, 'users/account_activation_invalid.html')


def activation_sent(request):
    try:
        context = { 'email': request.session['user_email'] }
        return render(request, 'users/account_activation_sent.html', context=context)
    except KeyError:
        raise Http404