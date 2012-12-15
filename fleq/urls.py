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



from django.conf.urls.defaults import *
import settings

from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',

	# Admin
	(r'^admin/', include(admin.site.urls)),
	(r'^admin/new-tournament/', 'quizbowl.views_admin.newTournament'),
	(r'^admin/load-questions/', 'quizbowl.views_admin.loadQuestions'),

  
    # Media
	(r'css/(?P<path>.*)$', 'django.views.static.serve',
	{'document_root': 'static/css'}),
	(r'images/(?P<path>.*)$', 'django.views.static.serve', 
	{'document_root': 'static/images'}),
	(r'js/(?P<path>.*)$', 'django.views.static.serve',
	{'document_root': 'static/js'}),

	# Connect
    url('^$', 'quizbowl.views_connect.Home'),
	url('^signin$', 'quizbowl.views_connect.Signin'),
	url('^logout$', 'quizbowl.views_connect.Logout'),
	url('^welcome$', 'quizbowl.views_connect.Welcome'),

	# Tournaments
	url('^my-tournaments$', 'quizbowl.views_tournaments.MyTournaments'),
	url('^active-tournaments$', 'quizbowl.views_tournaments.ActiveTournaments'),
	url('^next-tournaments$', 'quizbowl.views_tournaments.NextTournaments'),
	url('^finished-tournaments$', 'quizbowl.views_tournaments.FinishedTournaments'),

	url('^new-tournament$', 'quizbowl.views_admin.NewTournament'),
	url('^load-questions$', 'quizbowl.views_admin.LoadQuestions'),

	url('^tournament/(?P<gid>\d+)$', 'quizbowl.views_tournaments.TournamentStatistics'),
	url('^tournament/(?P<gid>\d+)/join$', 'quizbowl.views_tournaments.JoinTournament'),
	url('^tournament/(?P<gid>\d+)/disjoin$', 'quizbowl.views_tournaments.DisjoinTournament'),

	# Games
	url('^next-games$', 'quizbowl.views_games.NextGames'),
	url('^won-games$', 'quizbowl.views_games.WonGames'),
	url('^lost-games$', 'quizbowl.views_games.LostGames'),

	url('^game-room/(?P<gid>\d+)$', 'quizbowl.views_games.GameRoom'),
   	url('^game-room/(?P<gid>\d+)/select-time$', 'quizbowl.views_games.SelectStartTime'),   
   	url('^game-room/(?P<gid>\d+)/delete-time$', 'quizbowl.views_games.DeleteStartTime'),
)


urlpatterns += patterns('django.views.generic.simple',
	(r'^login/$', 'direct_to_template', {'template': 'login.html'}),
) 
