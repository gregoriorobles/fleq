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



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                     #  
#   El script se lanza a las 00:01                                    #
#                                                                     #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


from django.core.management import setup_environ
import settings

setup_environ(settings)

from quizbowl.models import Round, Score, Tournament
from quizbowl.views_notify import notify_user
import datetime
import sys


t = Tournament.objects.all()
t = Tournament.objects.filter(start_date = datetime.date.today())

for tournament in t:
    if tournament.players.all().count() < 2:
        # tournaments with one or no users are deleted before starting
        notify_user(tournament.admin, 'tournament_canceled', tournament)
        if tournament.players.all().count() > 0:
            p = tournament.players.all()
            for player in p:
                notify_user(player, 'tournament_canceled', tournament)
        tournament.delete()

    else:
        p = tournament.players.all()
        for player in p:
            notify_user(player, 'new_tournament', tournament)

        i = 1
        actual_date = tournament.start_date
        while True:
            if i <= tournament.rounds:
                round = Round(round_number = i, start_date = actual_date, 
								finish_date = actual_date + datetime.timedelta(tournament.days_per_round-1), tournament = tournament)
                round.save()
                actual_date += datetime.timedelta(tournament.days_per_round)
                i += 1
            else:
                break
