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



from django.contrib import admin
from quizbowl.models import Category, Date_time, Game, Preferred_start_time, Question, Question_review, RecoverUser, Round, Score, Tournament, UserProfile

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('pk', 'name')
	fields = ['name']
	
class DateTimeAdmin(admin.ModelAdmin):
	list_display = ('pk', 'date_time', 'preferred_start_time')
	fields = ['date_time', 'preferred_start_time']

class GameAdmin(admin.ModelAdmin):
	list_display = ('pk', 'start_time', 'start_time_committed', 'player1', 'player2', 'score_player1', 'score_player2', 'winner', 'round')
	#readonly_fields=('pk', 'log')	
	fields = ['start_time', 'start_time_committed', 'player1', 'player2', 'score_player1', 'score_player2', 'winner', 'round', 'log']

class PreferredStartTimeAdmin(admin.ModelAdmin):
	list_display = ('pk', 'committed', 'game', 'player')
	fields = ['committed', 'game', 'player']	

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'question', 'answer', 'alt_answer1', 'alt_answer2', 'alt_answer3', 'use_phonetic')
    list_filter = ['question', 'answer', 'alt_answer1', 'alt_answer2', 'alt_answer3', 'use_phonetic']
  
class RecoverUserAdmin(admin.ModelAdmin):
	list_display = ('pk', 'user', 'code')
	list_filter = ['user', 'code']

class TournamentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'sid', 'name', 'start_date', 'finish_date', 'admin', 'optional_info')
    list_filter = ['sid', 'name', 'start_date', 'finish_date', 'admin', 'optional_info']

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('pk', 'user', 'winner_games', 'loser_games', 'avatar')
	fields = ['user', 'winner_games', 'loser_games', 'avatar']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Date_time, DateTimeAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Preferred_start_time, PreferredStartTimeAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Question_review)
admin.site.register(RecoverUser, RecoverUserAdmin)
admin.site.register(Round)
admin.site.register(Score)
admin.site.register(Tournament, TournamentAdmin)
