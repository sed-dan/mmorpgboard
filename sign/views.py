from django.core.mail import send_mail
from .models import UserCode
from django.views.generic import CreateView, FormView
from django.contrib.auth.models import User
import random
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import login
from .forms import SignUpForm, CodeForm
from django.shortcuts import redirect
from django.conf import settings


@login_required
def user_profile(request):
    return render(request, 'sign/profile.html')


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'sign/signup_page.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        code = random.randint(100000, 999999)

        UserCode.objects.create(user=user, code=code)

        send_mail(
            subject=f'Подтверждение регистрации на Доске объявлений',
            message=f'Здравствуйте, {user.username}! Ваш код подтверждения регистрации:\n{code}',
            from_email='',
            recipient_list=[user.email],
        )

        self.request.session['verify_user_pk'] = user.pk

        return redirect('verification')

class Verification(FormView):
    template_name = 'sign/verification.html'
    form_class = CodeForm
    success_url = settings.SITE_URL

    def form_valid(self, form):
        code = form.cleaned_data['code']
        user_pk = self.request.session.get('verify_user_pk')
        user = UserCode.objects.get(user=user_pk)

        if user.code == code and user.code_valid():
            user = User.objects.get(pk=user_pk)
            user.is_active = True
            user.save()

            login(self.request, user, backend='django.contrib.auth.backends.User')

            del self.request.session['verify_user_pk']
            return redirect(self.get_success_url())
        else:
            form.add_error('code', 'Неверный или просроченный код подтверждения ')
            return self.form_invalid(form)
