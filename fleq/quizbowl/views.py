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

import datetime
import os
import sys



class Date_timeForm(forms.Form):
    TIME_CHOICES = (
        (10, '10:00'),
        (16, '16:00'),
        (22, '22:00'),
    )
    
    times = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple(), choices=TIME_CHOICES, label="Choose one start time at least:")
   


class NewQuestion_reviewForm(forms.Form):
    question_number = forms.IntegerField()
    arguments = forms.CharField(widget=forms.Textarea)



class Question_reviewForm(ModelForm):
    class Meta:
        model = Question_review
        fields = ('game', 'question', 'arguments', 'resolution')
       


class UserForm(ModelForm):
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        widgets = {
            'password': forms.PasswordInput(),
        }
    
    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
    def validate_password(value):
        if value != "el campo password":
            raise ValidationError(u"Las contraseñas introducidas no coinciden") 



# Sends and email to the user to notify an update in the Tournament
def notify_user(user, case, instance):
    subject = ""
    message = ""
    from_email = "fleqproject@gmail.com"
    to_email = user.email
    
    if case == 'new_tournament':
        tournament = instance
        subject += "Nuevo torneo"
        message += "Enhorabuena, " + user.username + ":\n\n"
        message += "El torneo '" + unicode(tournament) + "', en el que estabas inscrito, acaba de dar comienzo.\n" 
        message += "Por favor, revisa tu perfil de jugador (http://trivial.libresoft.es) para obtener los detalles de la primera partida."
        message += "\n\n\n"

    elif case == 'time_commited':
        game = instance
        tournament = game.round.tournament
        subject += u"Confirmación fecha y hora de partida"
        message += "Estimado " + user.username + ":\n\n"
        message += "Te informamos que, atendiendo a las preferencias de los jugadores, la partida de la ronda " + str(game.round.round_number) 
        message += " del torneo '" + unicode(tournament) + u"' a la que estás convocado se celebrará el día " + game.start_time.strftime("%d/%m/%Y") + " a las " +  game.start_time.strftime("%H:%M%Z") + " horas.\n"
        message += u"Por favor, revisa tu perfil de jugador (http://trivial.libresoft.es) para obtener más detalles."
        message += "\n\n\n"
    
    elif case == 'hurry_up':
        game = instance
        tournament = game.round.tournament
        subject += "Partida a punto de comenzar"
        message += "Estimado " + user.username + ":\n\n"
        message += "Te informamos que la partida en la que participas perteneciente a la ronda " + str(game.round.round_number) 
        message += " del torneo '" + unicode(game.round.tournament) + u"' empezará en unos minutos (" + game.start_time.strftime("%H:%M%Z") + ")." 
        message += "\n\n\n"
    
    elif case == 'new_review':
        question_review = instance
        tournament = question_review.game.round.tournament
        subject += u"Nueva revisión de pregunta"
        message += "Estimado " + user.username + ":\n\n"
        message += "Como administrador del torneo '" + unicode(tournament) + "', te informamos que el usuario " 
        message += question_review.player.username + u" ha solicitado la revisión de una pregunta realizada en una de las partidas de dicho torneo.\n"
        message += u"Por favor, revisa tu perfil de usuario (http://trivial.libresoft.es) para obtener más detalles."
        message += "\n\n\n"
    
    elif case == 'review_closed':
        question_review = instance
        tournament = question_review.game.round.tournament
        subject += u"Revisión de pregunta atendida"
        message += "Estimado " + user.username + ":\n\n"
        message += u"Te informamos que la revisión de pregunta que solicitaste en referencia a la partida de la ronda " 
        message += str(question_review.game.round.round_number) + " del torneo '" + unicode(tournament) + "' ha sido resuelta.\n"
        message += u"Por favor, revisa los detalles de esa partida (http://trivial.libresoft.es) para obtener más detalles."
        message += "\n\n\n"
    
    elif case == 'tournament_canceled':
        tournament = instance
        c = Category.objects.filter(tournament=tournament)
        subject += "Torneo cancelado"
        message += "Estimado " + user.username + ":\n\n"
        if user == tournament.admin: 
            message += "Como administrador del torneo '" + unicode(tournament) + "', te informamos que este ha sido cancelado por ser "
            message += u"el número de participantes inferior al mínimo (2).\n\n"
            message += u"A continuación se detallan las características del torneo cancelado:\n\n"
            message += "\t- Nombre: " + unicode(tournament) + "\n"
            message += "\t- Fecha de comienzo: " + tournament.start_date.strftime("%d/%m/%Y") + "\n" 
            message += u"\t- Número de rondas: " + str(tournament.rounds) + "\n" 
            message += u"\t- Duración de cada ronda (días): " + str(tournament.days_per_round) + "\n" 
            message += u"\t- Categoría(s): " 
            for category in list(c):
                message += unicode(category) + ", "
            message = message[:-2]
            message += "\n\n\n"
        else:
            message += "Te informamos que el torneo '" + unicode(tournament) + "' al que estabas inscrito, ha sido cancelado. "
            message += u"Por favor, ponte en contacto con el administrador del torneo para obtener más información.\n" 
            message += "Sentimos las molestias que hayamos podido ocasionarte."
            message += "\n\n\n"
    
    elif case == 'new_game':
        round = instance
        tournament = round.tournament
        subject += "Nueva ronda de partidas"
        message += "Estimado " + user.username + ":\n\n"
        message += u"Te informamos que la ronda número " + str(round.round_number) + " del torneo '" + unicode(tournament) + "' ha dado comienzo.\n"
        message += u"Por favor, revisa tu perfil de jugador (http://trivial.libresoft.es) para obtener los detalles de la partida que jugarás en esta ronda y elegir tu hora de preferencia."
        message += "\n\n\n"
    
    elif case == 'meditation_round':
        round = instance
        tournament = round.tournament
        subject = u"Ronda de reflexión"
        message += "Estimado " + user.username + ":\n\n"
        message += u"Debido a limitaciones relacionadas con la lógica del juego, te informamos que no podrás enfrentarte a ningún "
        message += "jugador durante la ronda " + str(round.round_number) + " del torneo '" + unicode(tournament) + u"' al que estás inscrito.\n"
        message += u"Como compensación, tu puntación en el torneo ha sido incrementada 1 punto, igual que si hubieses ganado la partida correspondiente a la ronda.\n\n"
        message += u"Sentimos las molestias que hayamos podido ocasionarte y deseamos que aproveches de la mejor manera posible esta ronda de reflexión."
        message += "\n\n\n"
    
    elif case == 'tournament_over':
        tournament = instance
        subject += "Torneo finalizado"
        message += "Estimado " + user.username + ":\n\n"
        message += "Te informamos que el torneo '" + unicode(tournament) + "' ha finalizado.\n"        
        message += u"Puedes consultar la tabla de clasificación de jugadores en la página del torneo (http://trivial.libresoft.es)."    
        message += "\n\n\n"

    message += "Atentamente,\n\n\tFLEQ (Free LibreSoft Educational Quizbowl)"
    
    send_mail(subject, message, from_email, [to_email])
    
    log = "Date: " + str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S %Z")) + "\n"
    log += "Subject: " + subject + "\n"
    log += "To: " + to_email + "\n"
    log += "Message:\n" + message + "\n"
    log += "\n\n"
    
    tournament.mail_log += log
    tournament.save()       
    

    
def games_history(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    response = "You're logged as " + request.user.username + " <a href='/logout'>(sign out)</a> <br>"
    response += "<br>" "<br>"
    
    if not request.user.is_staff:
        response += "You are not authorized to view this page <br>"
        response += "<br>" "<br>"
        response += "<a href='/accounts/profile'>Go to user profile</a>"
        return HttpResponse(response)

    for tournament in Tournament.objects.filter(admin = request.user):
        response += "<strong><u>Tournament: </u>" + unicode(tournament) + "</strong>" "<br>"
        for round in Round.objects.filter(tournament = tournament):
            response += "<strong>Round " + str(round.round_number) + "</strong>" "<br>"
            for game in Game.objects.filter(round = round):
                response += "<a href='/games/" + str(game.id) + "/'>(" + game.player1.username + " vs " + game.player2.username + ")</a>" "<br>"
        response += "<br>"     
        
    response += "<br>" 
    response += "<a href='/accounts/profile'>Go to user profile</a>"

    return HttpResponse(response)
       


@csrf_exempt
def new_question_review(request, gid):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    response = "You're logged as " + request.user.username + " <a href='/logout'>(sign out)</a> <br>"
    response += "<br>" "<br>"

    g = Game.objects.get(id = gid)
    if request.user != g.player1 and request.user != g.player2:
        response += "You are not authorized to view this page <br>"
        response += "<br>" "<br>"
        response += "<a href='/accounts/profile'>Go to user profile</a>"
        return HttpResponse(response)
    
    if request.method == 'POST': # If the form has been submitted...
        form = NewQuestion_reviewForm(request.POST) # A form bound to the POST data
        if form.is_valid(): 
            q = Question.objects.get(id = form.cleaned_data['question_number'])
            qr = Question_review(arguments = form.cleaned_data['arguments'],
                                 game = g,
                                 question = q,
                                 player = request.user)
            qr.save()
            notify_user(qr.game.round.tournament.admin, 'new_review', qr)

            return HttpResponseRedirect('/games/' + str(g.id) + '/') # Redirect after POST
    else:
        form = NewQuestion_reviewForm() # An unbound form

    return render_to_response('blank_form.html', {
        'form': form,
    })
  

  
@csrf_exempt    
def question_review(request, question_review_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    response = "You're logged as " + request.user.username + " <a href='/logout'>(sign out)</a> <br>"
    response += "<br>" "<br>"

    qr = Question_review.objects.get(id = question_review_id)
    if request.user != qr.player and request.user != qr.game.round.tournament.admin:
        response += "You are not authorized to view this page <br>"
        response += "<br>" "<br>"
        response += "<a href='/accounts/profile'>Go to user profile</a>"
        return HttpResponse(response)

    if request.user == qr.player:
        response += "<strong>Reviewed question: </strong>" + qr.question.question + "<br>"
        response += "<strong>Your review aguments:</strong>" "<br>"
        response += qr.arguments + "<br>"
        response += "<strong>Game admin's resolution:</strong>" "<br>"
        response += qr.resolution + "<br>"
    else:
        if request.method == 'POST': # If the form has been submitted...
            form = Question_reviewForm(request.POST) # A form bound to the POST data
            if form.is_valid(): 
                qr.resolution = form.cleaned_data['resolution']
                qr.save()
                notify_user(qr.player, 'review_closed', qr)
                return HttpResponseRedirect('/accounts/profile/') # Redirect after POST
        else:
            form = Question_reviewForm(instance = qr) # An unbound form
            form.fields['game'].widget.attrs['readonly'] = True
            form.fields['question'].widget.attrs['readonly'] = True
            form.fields['arguments'].widget.attrs['readonly'] = True

        return render_to_response('blank_form.html', {
            'form': form,
        })


    response += "<br>" "<br>"        
    response += "<a href='/games/" + str(qr.game.id) + '/' + "'>Go to game site</a>"    
    return HttpResponse(response)
