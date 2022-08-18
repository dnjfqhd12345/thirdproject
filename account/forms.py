from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User
from .models import Profile


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)


    class Meta:
        model = User
        fields = ('email', 'date_of_birth', 'favorites_1', 'favorites_2','name',)
        image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    # avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))



    def clean_favorites_2(self):
        favorites_1 = self.cleaned_data.get("favorites_1")
        favorites_2 = self.cleaned_data.get("favorites_2")
        if favorites_1 == favorites_2:
            raise forms.ValidationError("서로 다른 관심분야를 선택해주세요.")
        return favorites_2

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("패스워드가 일치하지 않습니다.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'date_of_birth', 'favorites_1', 'favorites_2',
                  'is_active', 'is_admin','name')
        image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))


    def clean_password(self):
        return self.initial["password"]

class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = Profile
        fields = ['avatar',]
