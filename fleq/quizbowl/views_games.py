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
from views_connect import LoginForm, RegisterForm

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
import string
import os




def NextGames(request):

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')

	myFutureGames = Game.objects.filter(Q(log = False), Q(player1 = request.user) | Q(player2 = request.user)).order_by('start_time')

	dates = []

	for game in myFutureGames:
		if not game.start_time_committed and (datetime.datetime.now() + datetime.timedelta(minutes=120)) > game.start_time:
			game.start_time_committed = True
			game.save()

		if not game.start_time.date() in dates:
			dates.append(game.start_time.date())

	# Load strings language to template mynextgames.html
	try:
		lang = strLang()
	except:
		lang = ''

	template = 'pc/next-games.html'

	if request.mobile:
		template = 'mobile/next-games.html'

	return render_to_response(template, {
		'user_me': request.user,
		'myNextGames': myFutureGames,
		'dates': dates,
		'lang': lang,
	})





def SelectStartTime(request, gid):

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')


	game = Game.objects.get(id = gid)
	pst = Preferred_start_time.objects.get(game = game, player = request.user)

	if request.user != game.player1 and request.user != game.player2 and request.user.username == "FLEQBOT":
		return HttpResponseRedirect('/')

	if game.is_over():
		return HttpResponseRedirect('/')

	if game.start_time_committed:
		return HttpResponseRedirect('/game-room/' + gid)

	now = datetime.datetime.now()

	g = game

	# Save all dates of my uncommitted games to select date and time to play
	myUncommittedGamesDate = [] # Contains all options to select in my next games

	startDate = g.round.start_date
	finishDate = g.round.finish_date

	while startDate <= finishDate:
		# Check to show only valid dates
		if startDate >= datetime.datetime.now().date():
			d = {}
			d['gid'] = g.pk
			d['date'] = startDate
			d['dateslashed'] = str(startDate.day) + "/" + str(startDate.month) + "/" + str(startDate.year)

			myUncommittedGamesDate.append(d)

		startDate = startDate + timedelta(days=1)

	if request.method == "GET":
		hour = now.hour

		# Extract all dates and times selected by user to show them
		mySelectedGamesDate = [] # Contains all options selected by user to each game
		opponentSelectedGamesDate = [] # Contains all options selected by opponent to each game

		# Select game preferences by user
		mySelection = Preferred_start_time.objects.filter(Q(player = request.user), Q(game = g))
		for selection in mySelection:
			# Extract all datetimes selected by user to show them
			myDateTimesSelected = Date_time.objects.filter(Q(preferred_start_time = selection)).order_by('date_time')			
			for dateSelected in myDateTimesSelected:
				s = {}
				s['gid'] = g.pk
				s['date'] = dateSelected
				mySelectedGamesDate.append(s)
				
		# Select game preferences by opponent
		if g.player1 == request.user:
			opponent = g.player2
		else:
			opponent = g.player1

		opponentSelection = Preferred_start_time.objects.filter(Q(player = opponent), Q(game = g))

		firstDateSinceNow = datetime.datetime.now()

		if firstDateSinceNow.hour < 22:
			firstDateSinceNow = datetime.datetime(now.year, now.month, now.day, now.hour + 2, 0, 0)
		else:
			firstDateSinceNow = firstDateSinceNow + datetime.timedelta(minutes=120)

		for selection in opponentSelection:
			# Extract all datetimes selected by opponent to show them
			myDateTimesSelected = Date_time.objects.filter(Q(preferred_start_time = selection)).order_by('date_time')			
			for dateSelected in myDateTimesSelected:
				s = {}
				s['gid'] = g.pk
				s['date'] = dateSelected
				
				if dateSelected.date_time >= firstDateSinceNow:			
					opponentSelectedGamesDate.append(s)

		hours = []

		if hour < 6:
			hours = range(8,24)
		elif hour < 22:
			hour = hour + 2
			while hour < 24:
				hours.append(hour)
				hour = hour + 1


		template = 'pc/select-time.html'
	
		if request.mobile:
			template = 'mobile/select-time.html'

		return render_to_response(template, {
				'hours': hours,
				'allhours': range(8,24),
				'today': now.date(),
				'myUncommittedGamesDate': myUncommittedGamesDate,
				'mySelectedGamesDate': mySelectedGamesDate,
				'opponentSelectedGamesDate': opponentSelectedGamesDate,
				'player1': game.player1.username,
				'player2': game.player2.username,
				'date': now,
				'user_me': request.user,
			})




	elif request.method == "POST":

		pst = Preferred_start_time.objects.get(player=request.user, game=game)
		gameDate = pst.game.start_time.date()

		for date in request.POST.getlist('hours'):
			pst = Preferred_start_time.objects.get(player=request.user, game=game)
			date = date.split("/")
			date = datetime.datetime(int(date[3]), int(date[2]), int(date[1]), int(date[0]), 0, 0)
			checkDate = Date_time.objects.filter(date_time = date, preferred_start_time = pst)

			if not checkDate:
				dateTime = Date_time(date_time = date, preferred_start_time = pst)
				dateTime.save()
				pst.committed = True
				pst.save()


			pst = Preferred_start_time.objects.filter(game = pst.game)

			if pst[0].committed and pst[1].committed:
				d_t1 = Date_time.objects.filter(preferred_start_time = pst[0])
				d_t2 = Date_time.objects.filter(preferred_start_time = pst[1])
				for d_t_player1 in d_t1:
					for d_t_player2 in d_t2:
						if d_t_player1.date_time == d_t_player2.date_time and not game.start_time_committed:
							game.start_time = d_t_player1.date_time
							game.start_time_committed = True
							game.save()
							notify_user(game.player1, 'time_commited', game)
							notify_user(game.player2, 'time_commited', game)
							return HttpResponseRedirect('/next-games')



		# Check if players saved the same hour to play
		for date in request.POST.getlist('hourselected'):

			checkDate = Date_time.objects.filter(date_time = date, preferred_start_time = pst)

			if not checkDate:
				dateTime = Date_time(date_time = date, preferred_start_time = pst)
				dateTime.save()
				pst.committed = True
				pst.save()


			pst = Preferred_start_time.objects.filter(game = pst.game)

			if pst[0].committed and pst[1].committed:
				d_t1 = Date_time.objects.filter(preferred_start_time = pst[0])
				d_t2 = Date_time.objects.filter(preferred_start_time = pst[1])
				for d_t_player1 in d_t1:
					for d_t_player2 in d_t2:
						if d_t_player1.date_time == d_t_player2.date_time and not game.start_time_committed:
							game.start_time = d_t_player1.date_time
							game.start_time_committed = True
							game.save()
							notify_user(game.player1, 'time_commited', game)
							notify_user(game.player2, 'time_commited', game)
							return HttpResponseRedirect('/next-games')


		return HttpResponseRedirect('/game-room/' + gid + "/select-time")



def DeleteStartTime(request, gid):

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')

	if request.method == "POST":

		game = Game.objects.get(id = gid)  
		dateNow = datetime.datetime.now()
	
		for date in request.POST.getlist('hours'):

			dateSelected =  Date_time.objects.get(pk = date)

			if dateSelected.preferred_start_time.player == request.user:
				dateSelected.delete()

		return HttpResponseRedirect('/game-room/' + gid + "/select-time")


	else:
		return HttpResponseRedirect('/')




def GameRoom(request, gid):

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')

	game = Game.objects.get(id = gid)

	if request.user != game.player1 and request.user != game.player2 and request.user.username != "FLEQBOT":
		return HttpResponseRedirect('/')

	tournament = game.round.tournament
	r = game.round.round_number
	startDate = game.start_time
	player1 = game.player1
	player2 = game.player2


	template = 'pc/game-room.html'
	dico = []
	
	if game.is_over():

		if request.mobile:
			return HttpResponseRedirect("/")

		lines = ""
		print os.getcwd()
		logfile = open(os.getcwd() + '/logs/' + str(game.id), 'r')
		lines = logfile.readlines()

		for line in lines:
			linesplit = {}
			line = line.split(";", 2)
			linesplit['timestamp'] = line[0].split(".")[0]
			linesplit['user'] = line[1]
			linesplit['message'] = line[2].replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"').replace('&#39;',"'").split(";")[0]
			dico.append(linesplit)

	else:
		if request.mobile:
			template = 'mobile/game-room.html'

	# Load strings language to template mytournaments.html
	try:
		lang = strLang()
	except:
		lang = ''


	return render_to_response(template, {
		'user_me': request.user,
		'game': game,
		'dico': dico,
		'tournament': tournament,
		'round': r,
		'player1': player1,
		'player2': player2,
		'lang': lang,
	})




def WonGames(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	
	# Select all won games
	wonGames = Game.objects.filter(Q(winner = request.user), Q(log=True)).order_by('-start_time')

	# Load strings language to template mynextgames.html
	try:
		lang = strLang()
	except:
		lang = ''

	template = 'pc/won-games.html'

	if request.mobile:
		template = 'mobile/won-games.html'

	return render_to_response(template, {
		'user_me': request.user,
		'lang': lang,
		'wonGames': wonGames,
	})





def LostGames(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	
	# Select all won games
	lostGames = Game.objects.filter(Q(player1 = request.user) | Q(player2 = request.user), ~Q(winner = request.user), Q(log=True)).order_by('-start_time')

	# Load strings language to template mynextgames.html
	try:
		lang = strLang()
	except:
		lang = ''

	template = 'pc/lost-games.html'

	if request.mobile:
		template = 'mobile/lost-games.html'


	return render_to_response(template, {
		'user_me': request.user,
		'lang': lang,
		'lostGames': lostGames,
	})
