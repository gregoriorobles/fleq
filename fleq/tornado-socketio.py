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


import tornado
import tornado.web
import tornado.httpserver
import tornadio2
import tornadio2.router
import tornadio2.server
import tornadio2.conn
import json

from django.core.management import setup_environ
import settings
setup_environ(settings)

from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from quizbowl.models import Game




class UserTornado(object):

	def __init__(self, socket, username, room):
		self.socket = socket
		self.username = username
		self.room = room



class FleqConnection(tornadio2.conn.SocketConnection):

	participants = set()


	def on_open(self, request):

		try:
			sessionid = str(request.cookies['sessionid']).split("=")[1]
			session = Session.objects.get(session_key=sessionid)
			uid = session.get_decoded().get('_auth_user_id')
			user = User.objects.get(pk=uid)

			if user.is_authenticated:
				create = True
				for person in self.participants:
					if person.username == user.username: # A user only must be in one room and from one device each time
						create = False
						person.socket = self
						person.room = None
						break

				if create:
					self.participants.add(UserTornado(self, user.username, None))

			else:
				return False # The user is not authenticated, then connection is rejected

			return

		except (KeyError, Session.DoesNotExist, User.DoesNotExist):
			return False # Session cookie is missed, or Session/User doesn't exist, then connection is rejected





	def on_message(self, message):

		message = json.loads(message)

		# JOIN
		if message['code'] == "1":

			for person in self.participants:
				if person.username == message['user'] and person.socket == self:

					try:
						game = Game.objects.get(pk=message['room'])
					except Game.DoesNotExist:
						return

					if game.player1.username == person.username or game.player2.username == person.username or person.username == "FLEQBOT":
						person.room = message['room']
						person.socket.send('{"code":"1"}')
					else:
						self.participants.remove(person)

					break


		# NEW MESSAGE
		elif message['code'] == "2":

			for person in self.participants:
				if person.username == message['user'] and person.socket == self:

					for person in self.participants:
						if person.room == message['room']:
							msg = message['message']
							msg = msg.replace('<', '&lt;').replace('>', '&gt;').replace("'", "&#39;")
							person.socket.send('{"code": "2", "user": "' + message['user'] + '", "message": "' + msg + '"}')

					break



	def on_close(self):
		for person in self.participants:
			if person.socket == self:
				self.participants.remove(person)
				break





# Create tornadio server
FleqRouter = tornadio2.router.TornadioRouter(FleqConnection)



# Create socket application
sock_app = tornado.web.Application(
    FleqRouter.urls,
    socket_io_port = 8004,
    socket_io_address = '127.0.0.1'
)




if __name__ == "__main__":

	tornadio2.server.SocketServer(sock_app, auto_start=True)
