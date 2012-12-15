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

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.conf import settings
from quizbowl.views_language import strLang, setBox
import datetime

from quizbowl.models import Date_time, Game, Preferred_start_time, Question_review, Round, Score, Tournament, Question, UserProfile



def MyTournaments(request):

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
           
	dateNow = datetime.datetime.now()
	myTournaments = Tournament.objects.filter(players = request.user).order_by('-start_date')
	  
	tournamentCategories = []

	for t in myTournaments:
		categories = t.categories.all()
		c = {}
		c['tid'] = t.pk
		c['categories'] = categories
		tournamentCategories.append(c)


	# Load strings language to template mytournaments.html
	try:
		lang = strLang()
	except:
		lang = ''

	template = 'pc/my-tournaments.html'

	if request.mobile:
		template = 'pc/my-tournaments.html'

	return render_to_response(template, {
		'user_me': request.user,
		'myTournaments': myTournaments,
		'tournamentCategories': tournamentCategories,
		'lang': lang,
	})




def ActiveTournaments(request):

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')

	activeTournaments = Tournament.objects.filter(start_date__lte = datetime.date.today(), finish_date__gte = datetime.date.today()).order_by('-start_date')
	tournamentCategories = []

	for t in activeTournaments:
		categories = t.categories.all()
		c = {}
		c['tid'] = t.pk
		c['categories'] = categories
		tournamentCategories.append(c)


	# Load strings language to template mytournaments.html
	try:
		lang = strLang()
	except:
		lang = ''

	template = 'pc/active-tournaments.html'

	if request.mobile:
		template = 'mobile/active-tournaments.html'


	return render_to_response(template, {
		'user_me': request.user,
		'activeTournaments': activeTournaments,
		'tournamentCategories': tournamentCategories,
		'lang': lang,
	})




def NextTournaments(request):

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
           
	nextTournaments = Tournament.objects.filter(start_date__gt = datetime.date.today())
	  
	tournamentCategories = []

	for t in nextTournaments:
		categories = t.categories.all()
		c = {}
		c['tid'] = t.pk
		c['categories'] = categories
		tournamentCategories.append(c)


	# Load strings language to template mytournaments.html
	try:
		lang = strLang()
	except:
		lang = ''

	template = 'pc/next-tournaments.html'

	if request.mobile:
		template = 'mobile/next-tournaments.html'


	return render_to_response(template, {
		'user_me': request.user,
		'nextTournaments': nextTournaments,
		'tournamentCategories': tournamentCategories,
		'lang': lang,
	})




def FinishedTournaments(request):

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')

	finishedTournaments = Tournament.objects.filter(finish_date__lt = datetime.datetime.now()).order_by('-start_date')
	tournamentCategories = []

	for t in finishedTournaments:
		categories = t.categories.all()
		c = {}
		c['tid'] = t.pk
		c['categories'] = categories
		tournamentCategories.append(c)


	# Load strings language to template mytournaments.html
	try:
		lang = strLang()
	except:
		lang = ''

	template = 'pc/finished-tournaments.html'

	if request.mobile:
		template = 'mobile/finished-tournaments.html'


	return render_to_response(template, {
		'user_me': request.user,
		'finishedTournaments': finishedTournaments,
		'tournamentCategories': tournamentCategories,
		'lang': lang,
	})





def TournamentStatistics(request, gid):

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')

	tournament = Tournament.objects.get(id=gid)
	rounds = Round.objects.filter(tournament = tournament).order_by('round_number')

	# Generate Score Table by this Tournament
	allscores = Score.objects.filter(tournament=tournament).order_by('-points', '-questions_won', 'questions_lost', 'player')
	scores = []
	pos = 0

	for userScore in allscores:
		userProfile = UserProfile.objects.get(user=userScore.player)
		user = {}
		user['profile'] = userProfile
		user['score'] = userScore.points
		
		# Create tournament positions
		if pos == 0:
			user['pos'] = pos+1
		else:
			if scores[pos-1]['score'] == userScore.points:
				user['pos'] = scores[pos-1]['pos']
			else:
				user['pos'] = pos+1
		
		# Initializing vars for question stats
		user['winner_questions'] = userScore.questions_won
		user['loser_questions'] = userScore.questions_lost
		user['winner_games'] = 0
		user['loser_games'] = 0
		
		# For each user, calculate how many games did he play
		gamesUser = []
		for r in rounds:
			game = Game.objects.filter(Q(round = r), Q(player1 = userProfile.user) | Q(player2 = userProfile.user), Q(log=True))
			try:
				#if game[0] and game[0].log:
				if game[0]:				
					gamesUser.append(game)
					# Total points won and lost
					try:
						if game[0].winner != userScore.player and game[0].winner.username != "jgonzalez":
							print "LOST"
							user['loser_games'] += 1
						elif game[0].winner.username == "FLEQBOT":
							user['loser_games'] += 1
						elif game[0].winner == userScore.player:
							user['winner_games'] += 1
					except:
						continue
			except:
				continue
		
		user['reflection_days'] = user['score'] - user['winner_games']
		user['total_games'] = user['loser_games'] + user['winner_games']
		
		# Save user stats and increment counter var
		scores.append(user)
		pos += 1

	rounds = Round.objects.filter(tournament=tournament)
	games = Game.objects.all()

	join = False
	disjoin = False

	if not (request.user in tournament.players.all()) and (datetime.date.today() < tournament.start_date):
		join = True
	elif (request.user in tournament.players.all()) and (datetime.date.today() < tournament.start_date):
		disjoin = True

	# Load strings language to template mytournaments.html
	try:
		lang = strLang()
	except:
		lang = ''


	template = 'pc/tournament-statistics.html'

	if request.mobile:
		template = 'mobile/tournament-statistics.html'


	return render_to_response(template, {
			'user_me': request.user,
			'tournament': tournament,
			'join': join,
			'disjoin': disjoin,
			'scores': scores,
			'rounds': rounds,
			'games': games,
			'lang': lang,
		})






def JoinTournament(request, gid):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')

	try:
		tournament = Tournament.objects.get(pk=gid)
	except:
		return HttpResponseRedirect('/')
	
	# players are added automatically to not started tournament the first time they visit tournament's site
	if (request.user != tournament.admin) and (not request.user in tournament.players.all()) and (datetime.date.today() < tournament.start_date):
		tournament.players.add(request.user)
		tournament.save()
		s = Score(player = request.user, tournament = tournament)
		s.save()

		return HttpResponseRedirect('/tournament/'  + gid)

	else:
		return HttpResponseRedirect('/tournament/'  + gid)





def DisjoinTournament(request, gid):

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')

	try:
		tournament = Tournament.objects.get(pk=gid)
	except:
		return HttpResponseRedirect('/')
	
	# players are added automatically to not started tournament the first time they visit tournament's site
	if (request.user != tournament.admin) and (request.user in tournament.players.all()) and (datetime.date.today() < tournament.start_date):
		tournament.players.remove(request.user)
		tournament.save()
		
		Score.objects.get(player=request.user, tournament=tournament).delete()

		return HttpResponseRedirect('/tournament/'  + gid)

	else:
		return HttpResponseRedirect('/tournament/'  + gid)
