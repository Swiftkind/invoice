from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView
from django.views import View


from users.forms import CompanyForm, UserChangePasswordForm, UserUpdateForm, SigninForm, SignupForm
from users.mixins import UserIsOwnerMixin
from users.models import Company, User 



class SigninView(TemplateView):
    """Signin user
    """
    template_name = 'users/signin.html'

    def get(self, *args, **kwargs):
        """Get signin form
        """
        if self.request.user.is_authenticated:
            return redirect('index')
        form = SigninForm()
        return render(self.request, self.template_name,{'form':form})

    def post(self, *args, **kwargs):
        """Signin user
        """
        form = SigninForm(data=self.request.POST)
        if form.is_valid():
            login(self.request, form.user_cache)
            return redirect('index')
        else:
            context={ 'form':form,}
        return render(self.request, self.template_name, context)



class SignupView(TemplateView):
    """Signup user
    """
    template_name = 'users/signup.html'

    def get(self, *args, **kwargs):
        """Display signup form
        """
        context = { 'company_form' : CompanyForm(),
                    'signup_form' : SignupForm(),
                  }
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        company_form = CompanyForm(self.request.POST, self.request.FILES)
        signup_form = SignupForm(self.request.POST, self.request.FILES)
        if signup_form.is_valid() and company_form.is_valid():
            company = company_form.save(commit=False)
            user = signup_form.save(commit=False)
            company.save()
            user.company = company
            user.save() 
            messages.error(self.request, 'Account successfully created. Activate your account from the admin.')
            return redirect('index')
        else:
             context = { 'company_form' : CompanyForm(self.request.POST),
                         'signup_form' : SignupForm(self.request.POST),
                       }
        return render(self.request, self.template_name, context)



class SignoutView(LoginRequiredMixin, View):
    """Signout a user
    """
    def get(self, *args, **kwargs):
        """Logout user and redirect to signin
        """
        logout(self.request)
        return redirect('signin')



class UserProfileView(UserIsOwnerMixin, TemplateView):
    """User profile
    """
    template_name = 'users/profile.html'

    def get(self, *args, **kwargs):
        """View user details
        """
        context = {'user': get_object_or_404(User, pk=kwargs['user_id'])}
        return render(self.request, self.template_name, context=context)



class UserUpdateView(UserIsOwnerMixin, TemplateView):
    """Update User
    """
    template_name = 'users/update_user.html'

    def get(self, *args, **kwargs):
        """Display form
        """
        user = get_object_or_404(User, pk=kwargs['user_id'])
        if self.request.user == user:
            context = { 'company_form':CompanyForm(instance=user.company), 
                        'user_form': UserUpdateForm(instance=user),
                      }
            return render(self.request, self.template_name, context=context)
        else:
            raise Http404("Does not exist")

    def post(self, request, *args, **kwargs):
        """Update a user
        """
        user = get_object_or_404(User, pk=kwargs['user_id'])
        user_form = UserUpdateForm(self.request.POST, self.request.FILES,instance=user)
        company_form = CompanyForm(self.request.POST, self.request.FILES,instance=user.company)
        if user_form.is_valid() and company_form.is_valid():
            company_form.save()
            user_form.save()
            messages.success(self.request, 'User is successfully updated')
            return redirect('index' )
        else:
            context = { 'company_form': company_form,
                        'user_form' : user_form,
                      }
        return render(self.request, self.template_name, context=context)



class UserSettingView(UserIsOwnerMixin, TemplateView):
    """ User settings
    """
    template_name = 'users/setting.html'

    def get(self, *args, **kwargs):
        """ View setting
        """
        return render(self.request, self.template_name)



class UserChangePassword(UserIsOwnerMixin, TemplateView):
    """ User change password
    """
    template_name = 'users/change_password.html'

    def get(self, *args, **kwargs):
        """ Change password form
        """
        context =  {}
        context['form'] = UserChangePasswordForm()
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        """ Check old and new password match
        """
        form = UserChangePasswordForm(self.request.POST, user=self.request.user)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            context = {}
            context['form'] = UserChangePasswordForm(self.request.POST, user=self.request.user)
            return render(self.request, self.template_name, context)

