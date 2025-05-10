import uuid

from django.contrib.auth import login, authenticate, logout, get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .forms import SignupForm, ProfileForm,  CustomUserCreationForm
from .models import CustomUser


def home(request):
    return render(request, 'templates/registration/post_list.html')


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'templates/registration/signup.html', {'form': form})


def LoginView(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home_accounts")  # URL名が正しいか確認してください
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "templates/registration/login.html", {"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("home")


User = get_user_model()


@login_required
def account_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if user != request.user:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied

    return render(request, 'templates/registration/accounts_detail.html', {'account_user': user})

@login_required
def profile_edit(request,user_id):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        
        if form.is_valid():
            form.name = request.user
            form.save()
            return redirect('account_detail', user_id=user.id)  # 編集後にプロフィールページへリダイレクト
    else:
        form = ProfileForm(instance=user)
    return render(request, 'templates/registration/profile_edit.html', {'form': form})