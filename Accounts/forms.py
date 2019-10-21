from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from .models import (User, UserProfile)
from django.views.decorators.csrf import (csrf_protect)

# Solving a Does not exists problem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate

# Authentication Are handled here !!!


class UserRegisterform(forms.ModelForm):

    # emails are set by default so i don't have to set it manually
    #email =  forms.EmailField()
    password = forms.CharField(label='Paasword', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password Validation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'password2',
        ]
        exclude = ['user']

    # Check if the email has already been taken

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_check = User.objects.filter(email=email)
        if email_check.exists():
            raise forms.ValidationError('This email is taken !!!')
            # else
        return email

    # Check if the two password matches
    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        # run test here
        if password != password2:
            raise forms.ValidationError('Two passwords must matches !!! ')
        return password2

    # overide the save form here  !!

    def save(self, commit=True, *args, **kwargs):
        instance = super(UserRegisterform, self).save(commit=False)
        instance.set_password(self.cleaned_data['password2'])
        if commit:
            instance.save()
        return instance

        # Log in user form 

class LoginFormUser(forms.ModelForm):
    email = forms.EmailField(label='Email Address')
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model  = User
        fields = [
            'email',
            'password'
        ]

        # Using another method here to validate user data and authenticate him  !!
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        loggedin_user = authenticate(
             email=email, password=password)
             # raise this exception if this user in none or no longer active
        if loggedin_user is None or not loggedin_user.is_active:
            raise forms.ValidationError(
                'This data are invalid please try againe !!!!')
        return self.cleaned_data



    # Profile User creating here 
class UserProfileForm(forms.ModelForm):
    full_name  = forms.CharField()
    address = forms.Textarea()
    phone_number = forms.IntegerField()
    #gender = forms.ChoiceField()    

    class Meta:
        model = UserProfile
        fields = [
            'full_name' , 
            'address' , 
            'phone_number'  , 
            #""'gender'
        ]

class UserInfo(forms.ModelForm):
    email= forms.EmailField()
    class Meta:
        model = User
        fields = [
            'email'
        ]

          
class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'active_user', 'admin_user')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
