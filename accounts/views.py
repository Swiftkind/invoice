from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth import login, logout, authenticate

from accounts.forms import *
from accounts.models import *

class SigninView(TemplateView):
	template_name = 'accounts/signin.html'

	def get(self, request, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect('index')
		form = SigninForm()
		return render(self.request, self.template_name,{'form':form})

	def post(self, request, *args, **kwargs):
		form = SigninForm(self.request.POST)
		if form.is_valid():
			login(self.request, form.auth)
			return redirect('index')
		return render(self.request, self.template_name, {'form':form})

class SignoutView(View):
	def get(self, request, *args, **kwargs):
		logout(self.request)
		return redirect('signin')

class SignupView(TemplateView):
	template_name = 'accounts/signup.html'

	def get(self, request, *args, **kwargs):
		form = SignupForm()
		return render(self.request, self.template_name, {'form':form})

	def post(self, request, *args, **kwargs):
		form = SignupForm(self.request.POST)
		if form.is_valid():
			form.save()
			user = authenticate(self.request, email=self.request.POST['email'], password=self.request.POST['password'])
			login(self.request, user)
			return redirect('index')
		return render(self.request, self.template_name, {'form': form})