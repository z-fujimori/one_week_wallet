from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm, SettingForm

# Create your views here.
def index(request):
    return render(request, "accounts/index.html")

def signup_view(request):
    print("debug1")
    if request.method == 'POST':
        print("debug2")
        form = CustomUserCreationForm(request.POST)
        print("debug3")
        if form.is_valid():
            print("debug4")
            user = form.save()
            login(request, user)
            messages.success(request, 'アカウントを作成しました！')
            return redirect('accounts:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST, request=request)
        print("v")
        print(form.is_valid())
        print("エラー", form.errors)
        print("^")
        if form.is_valid():
            print("~~~")
            user = form.get_user()
            login(request, user)
            messages.success(request, 'ログインしました！')
            return redirect('accounts:index')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'ログアウトしました。')
    return redirect('accounts:login')

@login_required
def setting(request):
    return render(request, 'accounts/setting.html')

@login_required
def settingStore(request):
    if request.method == "POST":
        form = SettingFrom(request.POST)
        if form.is_valid():
            # cleaned_dataから取得
            title = form.cleaned_data['title']
            amount = form.cleaned_data['amount']
            ...
            return redirect("somewhere")
    else:
        form = SettingFrom()

    return render(request, "myapp/form.html", {"form": form})

