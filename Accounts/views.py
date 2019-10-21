from django.shortcuts import render, redirect, HttpResponseRedirect

from django.contrib import messages
from django.views.generic import View
from .models import (
    User, UserProfile, 
)
# imports for creating view
from django.views.generic.edit import(
    CreateView,
    UpdateView, FormView
)

from django.contrib.auth import(
    logout,
    login,
    get_user_model,
    authenticate,

)
from django.contrib.auth.decorators import login_required
from .forms import(
    UserRegisterform,
    LoginFormUser,
    UserProfileForm, 
    UserInfo
)
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import (csrf_protect)
# Create your views here.

# Register USer page here !!!

class RegisterPage(View):
    form_class = UserRegisterform
    template_name = 'Register.html'

    # model = User
    # title  = 'Register'

        # handle get request()
    def get(self, form):
        form = self.form_class()
        return render(self.request, self.template_name, {'form': form})

    # define post request to handle the form if the method is 'POST'

    def post(self, *args, **kwargs):
        # get_user_model = User()
        form = self.form_class(self.request.POST, self.request.FILES)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # IF form is valid
    def form_valid(self, form):

         # commit = False, tells django not to save these data to DBs yet ..
        regis_user = form.save()
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        password2 = form.cleaned_data.get('password2')
        regis_user.set_password(password)
        regis_user = authenticate(self.request,
            email=email, password=password, password2=password2)

        #.user = self.request.user  # set the  user object here
        #regis_user.save()
        # profile = UserPro file.objects.create(user=new_user)
        login(self.request, regis_user)
        messages.success(self.request, f'Your successfully logged in {regis_user.email}')
        return redirect('/Index')

    # In case of invalid data
    def form_invalid(self,form):
        form.errors
        return render(self.request, self.template_name, {'form': form})


# LOgin view here !!

class LoginView(FormView):
    template_name = 'login.html'
    model  = User
    form_class = LoginFormUser
    
        # USe the decorating here to protect the form
    @method_decorator(csrf_protect,  name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

        # handle get request()
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form' : form })

    # define Post request 
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)
        if form.is_valid(): 
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # USe this if form is_valid 
    def form_valid(self, form):
        form.save(commit= False)
        #form_data = self.cleaned_data()
        email = form.cleaned_data.get('email')
        password  = form.cleaned_data.get('password')
        user = authenticate(self.request,  email=email, password=password)
        login(self.request, user)
        messages.success(self.request, 'Your successfuly logged in ')
        return redirect('/Index')

    # IN case of invalid data aka FORm 
    def form_invalid(self, form):
        # palys role just like messages but it the given errors will be shown in terminal too  
        print (form.errors) 
        return render(self.request, self.template_name, {'form': form})

    

# # handle login view with function BV
# def LoginView(request):
#     form_class = LoginFormUser
#     template_name = 'login.html'

#     if request.method == 'POST':
#         form = form_class(request.POST)
#         if form.is_valid():
#             form.save()
#             email = form.cleaned_data.get('email')
#             password1 = form.cleaned_data.get('password1')
#             #  "password_confirmation = form.cleaned_data.get('password_confirmation')
#             user = authenticate(request,  email=email, password=password)
#             login_required(request, user)
#             #messages.success(request, f' Welcome back {email}')
#             return redirect('/Index')

# MAking a log out view 

class LogoutPage(View):
    template_name = 'logout.html'
    model = User
    def get(self, request):
        logout(request)
        messages.success(request, f'Youre successfully logged out Log back in now !!! ')
        return redirect('Login')


# Contact page 
def Contact_Page(request):
    template_name =  'contact_page.html'
    return render(request, template_name, context=None)


# Profile Views here !!!!!!
class Profile_Home(UpdateView):
    model  = User
    template_name  = 'Profile_page.html'
    form_class_user  = UserInfo
    form_class_prof_user = UserProfileForm
    #current_user= self.request.user

    def post(self, *args, **kwargs):
        user_form  = self.form_class_user(self.request.POST, self.request.FILES,instance = self.request.user)
        profile_form = self.form_class_prof_user(self.request.POST, self.request.FILES,instance = self.request.user.profile_user)

        if user_form.is_valid() and profile_form.is_valid():
            return self.form_valid(user_form, profile_form)
            messages.success(self.request, 'Profile has been updated')
            return redirect('/Index')
        else:
            return user_form.errors or profile_form.errors

    def get(self, request):
        user_form = self.form_class_user(instance=  request.user)
        profile_form = self.form_class_prof_user(instance= request.user.profile_user)
        context = {
            'user_form' : user_form,
            'profile_form': profile_form
        }
        return render(request, self.template_name, context)       

    # DO this if the form is valid 
    def form_valid(self, user_form, profile_user):
        #loggedin_user  = self.request.user
        user_form.save()
        profile_user.save()
        return redirect('/Index')

    

