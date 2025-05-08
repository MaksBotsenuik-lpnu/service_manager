from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from authenticate.forms import (
    UserLoginForm,
    UserRegisterForm,
    UserProfileForm,
)
from logs.models.account_log import AccountLog


class UserRegistrationView(CreateView):
    """
    View registers the user and redirects to the login page.
    """
    form_class = UserRegisterForm
    template_name = 'authenticate/register.html'
    success_url = reverse_lazy('auth:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        AccountLog.objects.create(user=self.object, action="User registered")
        messages.success(self.request, "Registration successful! Please log in.")
        return response


class UserLoginView(LoginView):
    """
    View logs in the user and redirects to the main page.
    """
    template_name = 'authenticate/login.html'
    form_class = UserLoginForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        AccountLog.objects.create(user=form.get_user(), action="User logged in")
        messages.success(self.request, f"Welcome back, {form.get_user().get_full_name()}!")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Invalid email or password. Please try again.")
        return super().form_invalid(form)


class UserLogoutView(LogoutView):
    """
    View logs out the user and redirects to the login page.
    """
    next_page = reverse_lazy('auth:login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            AccountLog.objects.create(user=request.user, action="User logged out")
        return super().dispatch(request, *args, **kwargs)


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        logs = AccountLog.objects.order_by('-timestamp')[:10]
        return render(request, 'index.html', {'user': user, 'logs': logs})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('service:client-list')
    else:
        form = UserRegisterForm()
    return render(request, 'authenticate/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('service:client-list')
    else:
        form = UserLoginForm()
    return render(request, 'authenticate/login.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('auth:profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'authenticate/profile.html', {'form': form})


class AccountLogListView(LoginRequiredMixin, ListView):
    model = AccountLog
    template_name = 'authenticate/account_logs.html'
    context_object_name = 'logs'
    paginate_by = 10

    def get_queryset(self):
        return AccountLog.objects.order_by('-timestamp')[:10]

