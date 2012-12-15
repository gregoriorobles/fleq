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



from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
import datetime



def validate_future_date(date):
	if date <= datetime.date.today():
		raise ValidationError("Only future dates are allowed")



class Category(models.Model):
	name = models.CharField(max_length=50, unique=True)

	def __unicode__(self):
		return self.name



class Date_time(models.Model):
	date_time = models.DateTimeField()    
	preferred_start_time = models.ForeignKey("Preferred_start_time") # referenced model name between quotations marks ("") to avoid previous declaration requirement 

	def __unicode__(self):
		return unicode(self.date_time)


        
class Game(models.Model):
	start_time = models.DateTimeField('Start date and time')
	start_time_committed = models.BooleanField(default=False)
	log = models.BooleanField(default=False)
	player1 = models.ForeignKey(User, related_name='Player 1')
	score_player1 = models.PositiveIntegerField()
	player2 = models.ForeignKey(User, related_name='Player 2')
	score_player2 = models.PositiveIntegerField()    
	winner = models.ForeignKey(User, related_name='Winner')
	round = models.ForeignKey("Round")  # referenced model name between quotations marks ("") to avoid previous declaration requirement 

	def is_over(self):
		if self.log:
			return True
		else:
			return False

	def __unicode__(self):
		return "Tournament '%s' - Round %s - %s vs %s" % (unicode(self.round.tournament), self.round.round_number, self.player1, self.player2)
        


class Preferred_start_time(models.Model):
	committed = models.BooleanField(default=False)

	game = models.ForeignKey(Game)
	player = models.ForeignKey(User)
    
	def __unicode__(self):
		return "%s - %s" % (unicode(self.game), self.player)


        
class Question(models.Model):
	alt_answer1 = models.CharField(max_length=120, blank=True, help_text="(optional)")
	alt_answer2 = models.CharField(max_length=120, blank=True, help_text="(optional)")
	alt_answer3 = models.CharField(max_length=120, blank=True, help_text="(optional)")
	answer = models.CharField(max_length=120)
	question = models.CharField(max_length=200, unique=True)
	use_phonetic = models.BooleanField(default=False, editable=False)
    
	categories = models.ManyToManyField(Category)
    
	def __unicode__(self):
		return self.question



class Question_review(models.Model):
	arguments = models.TextField()
	resolution = models.TextField(blank=True)  
	game = models.ForeignKey(Game)
	player = models.ForeignKey(User)
	question = models.ForeignKey(Question)

	def is_closed(self):
		if self.resolution:
			return True
		else:
			return False

	def __unicode__(self):
		return "%s - %s" % (unicode(self.question), unicode(self.game))



class RecoverUser(models.Model):
	user = models.ForeignKey(User)
	code = models.CharField(max_length=16, unique=True)



class Round(models.Model):
	round_number = models.PositiveIntegerField()
	start_date = models.DateField('start date')
	finish_date = models.DateField('finish date')  
	tournament = models.ForeignKey("Tournament")  # referenced model name between quotations marks ("") to avoid previous declaration requirement 

	def __unicode__(self):
		return "%s - round %s" % (unicode(self.tournament), self.round_number)
    

class Score(models.Model):
	points = models.PositiveIntegerField(default=0)
	questions_won = models.PositiveIntegerField(default=0)
	questions_lost = models.PositiveIntegerField(default=0)	
	player = models.ForeignKey(User)
	tournament = models.ForeignKey("Tournament")  # referenced model name between quotations marks ("") to avoid previous declaration requirement 
    
	def __unicode__(self):
		return "%s - %s" % (self.player, unicode(self.tournament))
     


class Tournament(models.Model):
	ROUNDS_CHOICES = (
		(2, '2'),
		(3, '3'),
		(4, '4'),
		(5, '5'),
		(6, '6'),
	)

	DAYS_PER_ROUND_CHOICES = (
		(1, '1'),
		(2, '2'),
		(3, '3'),
	)

	sid = models.CharField(max_length=128)
	days_per_round = models.PositiveIntegerField(choices=DAYS_PER_ROUND_CHOICES)
	name = models.CharField(max_length=50, unique=True)
	rounds = models.PositiveIntegerField(choices=ROUNDS_CHOICES)
	start_date = models.DateField('start date', default=(datetime.datetime.today() + datetime.timedelta(days=10)))
	finish_date = models.DateField('finish date', default="2012-10-10")
	mail_log = models.TextField(blank=True, editable=False)
	admin = models.ForeignKey(User, related_name='admin', default=1)
	categories = models.ManyToManyField(Category)
	players = models.ManyToManyField(User, blank=True)
	optional_info = models.TextField(blank=True)
	only_mobile_devices = models.BooleanField(default=False)

	def __unicode__(self):
		return self.name


class UserProfile(models.Model):
	avatar = models.ImageField(upload_to='images/avatars/', default='images/avatars/default.png')
	user = models.ForeignKey(User)
	winner_games = models.PositiveIntegerField(default=0)
	loser_games = models.PositiveIntegerField(default=0)
