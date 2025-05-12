from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("id", "email", "name") 

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="アカウントID")  # ラベル調整

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)

    def clean(self):
        id = self.cleaned_data.get('name')
        password = self.cleaned_data.get('password')

        if id and password:
            self.user_cache = authenticate(self.request, id=id, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("ログイン情報が正しくありません")
        return self.cleaned_data