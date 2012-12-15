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


from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from quizbowl.models import Category, User

from datetime import *
import datetime

# Sends and email to the user to notify an update in the Tournament
def notify_user(user, case, instance):
	subject = ""
	message = ""
	from_email = "fleq.libresoft@gmail.com"
	to_email = user.email

	if case == 'new_tournament':
		tournament = instance
		subject += "Nuevo torneo"
		message += "Enhorabuena, " + user.username + ":\n\n"
		message += "El torneo '" + unicode(tournament) + "', en el que estabas inscrito, acaba de dar comienzo.\n" 
		message += "Por favor, revisa tu perfil de jugador (http://pfc-jgonzalez.libresoft.es) para obtener los detalles de la primera partida."
		message += "\n\n\n"

	elif case == 'time_commited':
		game = instance
		tournament = game.round.tournament
		subject += u"Confirmación fecha y hora de partida"
		message += "Estimado " + user.username + ":\n\n"
		message += "Te informamos que, atendiendo a las preferencias de los jugadores, la partida de la ronda " + str(game.round.round_number) 
		message += " del torneo '" + unicode(tournament) + u"' a la que estás convocado se celebrará el día " + game.start_time.strftime("%d/%m/%Y") + " a las " +  game.start_time.strftime("%H:%M%Z") + " horas.\n"
		message += u"Por favor, revisa tu perfil de jugador (http://pfc-jgonzalez.libresoft.es) para obtener más detalles."
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
		message += u"Por favor, revisa tu perfil de usuario (http://pfc-jgonzalez.libresoft.es) para obtener más detalles."
		message += "\n\n\n"
    
	elif case == 'review_closed':
		question_review = instance
		tournament = question_review.game.round.tournament
		subject += u"Revisión de pregunta atendida"
		message += "Estimado " + user.username + ":\n\n"
		message += u"Te informamos que la revisión de pregunta que solicitaste en referencia a la partida de la ronda " 
		message += str(question_review.game.round.round_number) + " del torneo '" + unicode(tournament) + "' ha sido resuelta.\n"
		message += u"Por favor, revisa los detalles de esa partida (http://pfc-jgonzalez.libresoft.es) para obtener más detalles."
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
		message += u"Por favor, revisa tu perfil de jugador (http://pfc-jgonzalez.libresoft.es) para obtener los detalles de la partida que jugarás en esta ronda y elegir tu hora de preferencia."
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

	elif case == 'recover_user':
		recover = instance
		subject += u"Recuperación de cuenta de usuario"
		message += "Estimado " + user.username + ":\n\n"
		message += u"Has solicitado recuperar tu cuenta de usuario porque no recuerdas tu contraseña. Para hacerlo, accede a través del siguiente enlace:\n\n"
		message += "http://pfc-jgonzalez.libresoft.es/recover-account/" + recover.code + "\n\n"
		message += u"Desde él, podrás introducir una nueva contraseña que modificará a la que tenías anteriormente."
		message += "\n\n\n"		


	message += "Atentamente,\n\n\tFLEQ (Free LibreSoft Educational Quizbowl)"
    
	send_mail(subject, message, from_email, [to_email])
    
	log = "Date: " + str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S %Z")) + "\n"
	log += "Subject: " + subject + "\n"
	log += "To: " + to_email + "\n"
	log += "Message:\n" + message + "\n"
	log += "\n\n"

	if case != 'recover_user':
		tournament.mail_log += log
		tournament.save()



def contactEmail(info):
	to_email = "fleq.libresoft@gmail.com"
	from_email = info['userEmail']

	try:
		user = User.objects.get(email=info['userEmail'])
	except:
		user = ""

	# First, send an email to Administrator
	subject = "[FLEQ CONTACT FORM]" + " " + info['subject']
	message = "----------- INFO USER -----------\n"
	
	if user:
		message += "User: " + user.username + "\n"
		message += "Name: " + unicode(user.first_name) + " " + unicode(user.last_name) + "\n"
		message += "Email contact: " + user.email + "\n"
	else:
		message += "User: anonymous" + "\n"
		message += "Email contact: " + info['userEmail'] + "\n"

	message += "----------- END INFO USER -----------\n\n"
	message += info['message']
	send_mail(subject, message, from_email, [to_email])

	# After that, send an email to User
	subject = "[FLEQ CONTACT SUCCESSFULL]" + " " + info['subject']
	message = "Thanks for your message!\n\n"
	message += "Our team have received your request and soon will contact you with our reply. We'll try to be as fast as we can...\n\n"        
	message += u"\tThanks to contact with FLEQ Project (Free LibreSoft Educational Quizbowl - http://pfc-jgonzalez.libresoft.es)."
	send_mail(subject, message, to_email, [from_email])
