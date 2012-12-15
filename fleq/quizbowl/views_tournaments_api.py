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



from django import db, forms
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.files import File
from django.core.mail import send_mail
from django.db.models import Q
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from quizbowl.models import Category, Date_time, Game, Preferred_start_time, Question, Question_review, Round, Score, Tournament
from datetime import *
from quizbowl.views_notify import notify_user

import datetime
import os
import sys



def myTodayGames(request):
		
	dateNow = datetime.datetime.now().date()
	timeNow = datetime.datetime.now().time()
	
	# Check if I have to play today a game
	myNextGames = Game.objects.filter(Q(log__isnull = False), Q(start_time__gte = dateNow), Q(player1 = request.user) | Q(player2 = request.user)).order_by('-start_time')
	todayGames = []
	for game in myNextGames:
		if game.start_time.date() == dateNow and game.start_time.time() > timeNow:
			todayGames.append(game)
	
	return todayGames



def myNextGames(request):
	dateNow = datetime.datetime.now().date()
	timeNow = datetime.datetime.now().time()
	
	# Check if I have to play today a game
	myNextGames = Game.objects.filter(Q(log__isnull = False), Q(start_time__gte = dateNow), Q(player1 = request.user) | Q(player2 = request.user)).order_by('-start_time')
	nextGames = []
	for game in myNextGames:
		if game.start_time.date() > dateNow:
			nextGames.append(game)
				
	return nextGames	



# Shows active Tournaments of user (player tournament)
def myActiveTournaments(request):
	# Select all Tournaments and Games of user with status player
	dateNow = datetime.datetime.now()
	myActiveTournaments = Tournament.objects.filter(players = request.user).filter(Q(finish_date__gte = dateNow)).order_by('-start_date')

	return myActiveTournaments



# Shows active admin Tournaments of user
def myAdminTournaments(request):

	# Select all Tournaments and Games of user with status player
	dateNow = datetime.datetime.now()
	myActiveAdminTournaments = Tournament.objects.filter(admin = request.user).filter(Q(finish_date__gte = dateNow)).order_by('-start_date')

	return myActiveAdminTournaments



def myPastTournaments(request):
	# Select all Tournaments finished
	dateNow = datetime.datetime.now()
	myFinishedTournaments = Tournament.objects.filter(Q(players = request.user)).filter(finish_date__lt = dateNow).order_by('-start_date')
	
	return myFinishedTournaments
	


def myAdminPendingQuestionReviews(user):
	# Pending Question Reviews
	allMyAdminTournaments = Tournament.objects.filter(admin = user)
	pendingQuestionReviews = 0
	# All reviews in my Tournaments
	for tournament in allMyAdminTournaments:
		questionReviews = Question_review.objects.filter(game__round__tournament = tournament, resolution__exact = '')
		pendingQuestionReviews += len(questionReviews)
	
	allMyTournaments = Tournament.objects.filter(Q(players = user))
	# All reviews in my Tournaments
	for tournament in allMyTournaments:
		questionReviews = Question_review.objects.filter(game__round__tournament = tournament, resolution__exact = '', player = user)
		pendingQuestionReviews += len(questionReviews)	

	return pendingQuestionReviews
