from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login as django_login, logout as django_logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from account.forms import LoginForm, RegistrationForm, UserCreationForm, CustomChangePasswordForm
from account.tasks import send_confirmation_mail
from account.tokens import account_activation_token
from django.db.models import Q
from django.contrib.auth.hashers import make_password


User = get_user_model()


class Home(CreateView):

    form_class = UserCreationForm
    template_name = 'home.html'
    success_url = reverse_lazy('home')  

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])  
        user.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.order_by("id").all() 
        return context


class CustomLoginView(LoginView):
    template_name ='login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')


class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        result = super().form_valid(form)
        send_confirmation_mail(user=self.object, current_site=get_current_site(self.request))
        return result


class ActiveAccountView(View):

    def get(self, request, *args, **kwargs):
        uidb64  =  kwargs ['uidb64']
        token = kwargs['token']
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except ( TypeError , ValueError , OverflowError , User . DoesNotExist ):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user . save ()
            messages.success(request, 'Your account activated!')
            return redirect(reverse_lazy('login'))
        else:
            messages.warning(request, 'Something went wrong!')
            return redirect(reverse_lazy('login'))


def search_user(request):
    data = request.POST.get("query")
    users = User.objects.filter(Q(first_name=data) | Q(username=data) | Q(phone=data) | Q(email=data))
    return render(request,'home.html',{"users":users})


def edit(request):
    users=User.objects.all()
    return render(request,'home.html',{"users":users})


def update(request,id):
    if request.method == "POST":
        user=User.objects.get(id=id)
        user.first_name = request.POST.get('first_name')
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.save()
        return redirect('home')
    return render(request,'home.html')


def delete(request,id):
    users = User.objects.filter(id=id)
    users.delete()
    return redirect('home')

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'change-password.html'
    success_url = reverse_lazy('password_change_done')

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'password_change_done.html'
    form_class = CustomChangePasswordForm
    success_url = reverse_lazy('login')



   
        

 










