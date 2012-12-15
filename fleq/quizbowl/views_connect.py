#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################################################
#                                                                           #
#  FLEQ (Free LibreSoft Educational Quizbowl)                               #
#  A synchronous on-line competition software to improve and                #
#  motivate learning.                                                       #
#                                                                           #
#  Copyright (C) 2012  Arturo Moral, Gregorio Robles, Félix Redondo         #
#                      & Jorge González Navarro                             #
#                                                                           #
#  This program is free software: you can redistribute it and/or modify     #
#  it under the terms of the GNU Affero General Public License as           #
#  published by the Free Software Foundation, either version 3 of the       #
#  License, or (at your option) any later version.                          #
#                                                                           #
#  This program is distributed in the hope that it will be useful,          #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#  GNU Affero General Public License for more details.                      #
#                                                                           #
#  You should have received a copy of the GNU Affero General Public License #
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.    #
#                                                                           #
#  Contact authors : Arturo Moral <amoral@gmail.com>                        #
#                    Gregorio Robles <grex@gsyc.urjc.es>                    #
#                    Félix Redondo <felix.redondo.sierra@gmail.com>         #
#                    Jorge González Navarro <j.gonzalezna@gmail.com>        #
#                                                                           #
#############################################################################



from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.conf import settings

from quizbowl.models import UserProfile, RecoverUser
from quizbowl.views_language import strLang, setBox
from quizbowl.views_tournaments_api import *
from quizbowl.views_notify import notify_user




def Welcome(request):
	if request.mobile:
		return render_to_response('mobile/welcome.html', {})

	return render_to_response('pc/welcome.html', {})


# Login to the app
def Home(request):

	if request.user.is_authenticated():

		nextGames = len(Game.objects.filter(Q(log = False), Q(start_time__gte = datetime.datetime.now()), Q(player1 = request.user) | Q(player2 = request.user)))
		wonGames = len(Game.objects.filter(Q(winner = request.user), Q(log=True)))
		lostGames = len(Game.objects.filter(Q(player1 = request.user) | Q(player2 = request.user), ~Q(winner = request.user), Q(log=True)))
		myTournaments = len(Tournament.objects.filter(players = request.user))
		activeTournaments = len(Tournament.objects.filter(start_date__lte = datetime.date.today(), finish_date__gte = datetime.date.today()))
		nextTournaments = len(Tournament.objects.filter(start_date__gt = datetime.date.today()))
		finishedTournaments = len(Tournament.objects.filter(finish_date__lt = datetime.datetime.now()))

		if request.mobile:
			return render_to_response('mobile/home.html', {
				'nextGames': nextGames,
				'wonGames': wonGames,
				'lostGames': lostGames,
				'myTournaments': myTournaments,
				'activeTournaments': activeTournaments,
				'nextTournaments': nextTournaments,
				'finishedTournaments': finishedTournaments,	
			})
		
		
		return HttpResponseRedirect("/next-games")


	else:

		# Load strings language to template login.html
		try:
			lang = strLang()
		except:
			lang = ''

		if request.method == 'POST':
			loginForm = LoginForm(request.POST)
			if loginForm.is_valid():
				user = authenticate(username=request.POST['username'], password=request.POST['password'])
				login(request, user)
		
				if request.mobile:
					return render_to_response('mobile/home.html', {})
				else:
					return HttpResponseRedirect('/next-games')

			else:
				registerForm = RegisterForm()
				template = 'pc/splash.html'

				if request.mobile:
					template = 'mobile/login.html'

				return render_to_response(template, {
					'loginForm': loginForm,
					'lang': lang,
				})

		else:
			if request.mobile:
				return render_to_response('mobile/login.html', {})

			return render_to_response('pc/splash.html', {})





def Logout(request):
	logout(request)

	if request.mobile:
 		return render_to_response('mobile/login.html', {})

	return HttpResponseRedirect("/")





def Signin(request):

	try:
		lang = strLang()
	except:
		lang = ''

	if request.method == 'POST':
		registerForm = RegisterForm(request.POST)

		if registerForm.is_valid(): 
			user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
			user.is_staff = False
			user.first_name = request.POST['first_name']
			user.last_name = request.POST['last_name']
			userProfile = UserProfile(user=user)
			user.save()
			userProfile.save()

			user = authenticate(username=request.POST['username'], password=request.POST['password'])
			login(request, user)


			if request.mobile:
				return render_to_response('mobile/welcome.html', {})

			return render_to_response('pc/welcome.html', {
				'user': request.user
			})
			

		else:
			template = 'pc/signin.html'

			if request.mobile:
				template = 'mobile/signin.html'

			return render_to_response(template, {
				'user_me': request.user,
				'registerForm': registerForm,
				'lang': lang,
			})

	else:
		registerForm = RegisterForm()

		template = 'pc/signin.html'

		if request.mobile:
			template = 'mobile/signin.html'

		return render_to_response(template, {
			'user_me': request.user,
			'registerForm': registerForm,
			'lang': lang,
		})




class RegisterForm(forms.Form):
	username = forms.CharField(max_length=100)
	first_name = forms.CharField(max_length=100)
	last_name = forms.CharField(max_length=100)
	password = forms.CharField(widget=forms.PasswordInput(),max_length=100)
	password2 = forms.CharField(widget=forms.PasswordInput(),max_length=100,label=(strLang()['label_password2']))
	email = forms.EmailField(max_length=100)
	
	def clean_username(self):
		username = self.cleaned_data.get('username')
		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError(strLang()['error_register_username_exists'])
	
	def clean_email(self):
		email = self.cleaned_data.get('email')
		try:
			email = User.objects.get(email=email)
		except User.DoesNotExist:
			return email
		raise forms.ValidationError(strLang()['error_register_email_exists'])

	def clean_first_name(self):
		first_name = self.cleaned_data.get('first_name')
		if not first_name:
			raise forms.ValidationError(strLang()['error_register_first_name_required'])
		return first_name
		
	def clean_last_name(self):
		last_name = self.cleaned_data.get('last_name')
		if not last_name:
			raise forms.ValidationError(strLang()['error_register_last_name_required'])
		return last_name

	def clean(self):
		cleaned_data = super(RegisterForm, self).clean()
		password = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')
		if password != password2:
			self._errors["password"] = self.error_class([strLang()['error_register_passwords_differents']])
			self._errors["password2"] = self.error_class([strLang()['error_register_passwords_differents']])
			
		return cleaned_data





class LoginForm(forms.Form):
	username = forms.CharField(max_length=100)
	password = forms.CharField(widget=forms.PasswordInput(),max_length=100)
	
	def clean_password(self):
		password = self.cleaned_data.get('password')
		if not password: raise forms.ValidationError(strLang()['error_login_password_required'])	
		return password

	def clean_username(self):
		username = self.cleaned_data.get('username')
		if not username: raise forms.ValidationError(strLang()['error_login_username_required'])	
		return username
	
	def clean(self):
		cleaned_data = super(LoginForm, self).clean()
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		if user is not None:
			if not user.is_active:
				raise forms.ValidationError(strLang()['error_login_failed'])
		else:
			raise forms.ValidationError(strLang()['error_login_failed'])
		
		return cleaned_data
