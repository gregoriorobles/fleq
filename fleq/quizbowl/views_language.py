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



from datetime import *
import datetime

# Create the info to show a box
def setBox(status):
	box = {}
	
	lang = strLang()
	box['message'] = lang[status]
	
	if status.count("success"):
		box['status'] = 'success'
	elif status.count("error"):
		box['status'] = 'error'
	elif status.count("info"):
		box['status'] = 'info'
	elif status.count("warning"):
		box['status'] = 'warning'
	
	return box
		

def strLang():
	strng = {}

	### CONTACT.HTML ###
	strng['title_contact_with_us'] = u"Contact Us"

	strng['success_contact_sent'] = u"Your request has been sent successfully! As soon as posible, our team reply you."

	strng['error_contact_empty_subject'] = u"Subject is required!"	
	strng['error_contact_empty_message'] = u"Message is required!"
	strng['error_contact_empty_email'] = u"Email is required to reply you!"		

	### EDIT PROFILE AND CHANGE PASSWORD ###
	strng['label_change_avatar'] = u"Change current avatar"
	strng['help_change_avatar'] = u"Leave this field empty if you want to keep your current avatar"

	strng['label_current_password'] = u"Current password"	
	strng['label_new_password'] = u"New password"
	strng['label_new_password2'] = u"Repeat new password"
	
	strng['title_edit_profile'] = u"Edit My Profile"
	
	strng['button_edit_profile'] = u"Update My Profile"
	strng['button_change_password'] = u"Update My Password"	

	strng['error_change_password_differents'] = u"New password could not be different in both fields required."
	strng['error_change_password_empty_field'] = u"This is field is required."
	strng['error_current_password_incorrect'] = u"Current password introduced is incorrect. Try again!"
	
	strng['success_edit_account'] = u"Your info has been updated successfully!"
	strng['success_change_password'] = u"Your password has been changed successfully!"	

	### GAMEINFO.HTML ###
	strng['vs'] = u"vs"
	strng['finished'] = u"Finished"
	strng['pending'] = u"Pending"
	strng['closed'] = u"Closed"
	strng['title_question_reviews'] = u"Question Reviews"
	strng['title_my_question_reviews'] = u"My Question Reviews"
	
	strng['error_title_game_no_exists'] = u"Oops!"
	strng['error_game_info'] = u"Sorry! You haven't got permission to see the info of this game."
	strng['error_game_no_exists'] = u"Sorry! The game selected doesn't exist in our database."
	strng['error_tournament_info_no_exists'] = u"Error! Tournament info doesn't exist in the system!"
	strng['error_no_tournament_score'] = u"Error! Tournament scores doesn't exist in the system!"
	strng['error_question_reviews_no_exists'] = u"Error! Don't exist question reviews!"
	strng['error_question_no_exists'] = u"Error! Question #ID selected doesn't exist! Try again!"	

	### LOADQUESTIONS.HTML ###
	strng['title_load_questions'] = u"Load File Questions"
	strng['button_load_questions'] = u"Load File"
	strng['success_load_questions'] = u"Questions loaded successfully!"	

	### LOGIN.HTML ###

	# Register an account
	strng['button_register'] = u"Register"
	strng['label_password2'] = u"Repeat password"

	strng['success_register_account'] = u"Your account has been successfully registered! Login now."
	
	strng['error_register_username_exists'] = u"Exists in our database. Choose other."
	strng['error_register_email_exists'] = u"Exists in our database. Choose other."
	strng['error_register_first_name_required'] = u"First name is required."
	strng['error_register_last_name_required'] = u"Last name is required."
	strng['error_register_passwords_differents'] = u"Password could not be different in both fields."

	strng['error_register_before_join_tournament'] = u"Before join to the Tournament selected, you have to register an account. It's free!"
	strng['error_register_before_show_tournament'] = u"Do you want to see all info about Tournaments? Only you have to register an account. It's free!"
	
	# Login an account
	strng['title_login'] = u"Are You Registered?"
	strng['button_login'] = u"Login"
	strng['button_recover_account'] = u"Forgot Password?"
		
	strng['error_login_password_required'] = u"Password is required."
	strng['error_login_username_required'] = u"Username is required."
	strng['error_login_failed'] = u"Login failed!"
	
	### LOSTGAMES.HTML WONGAMES.HTML ###
	strng['title_lost_games'] = u"Lost Games"
	strng['title_won_games'] = u"Won Games"
	
	strng['table_date'] = u"DATE"
	strng['table_tournament'] = u"TOURNAMENT"
	strng['table_round'] = u"ROUND"
	strng['table_vs'] = u"VS"

	### MYNEXTGAMES.HTML ###
	strng['title_my_next_games'] = u"My Next Games"
	strng['round'] = u"Round"
	strng['dates_times_play'] = u"Select all dates and time using ctrl+click that you have available to play"
	
	strng['error_no_next_games'] = u"Sorry! You haven't any game active now!"
	strng['error_datetime_selected_before'] = u"Sorry! One or more dates or times selected are past and you can't play a game in past times! No date and time has been saved. Try again selecting valid dates and times."
	date2hours = datetime.datetime.now() + timedelta(hours = 2)
	strng['error_datetime_selected_too_soon'] = u"Sorry! One or more times selected to play today are too soon. To facilitate that your opponent can see the game schedule, you can't select to play too soon. If you want to play today, choose any time that is about 2 hours from the current time. " + "<br />" + "<center>(<u>Select hours to play today from: " + str(date2hours.hour) + ":00h</u>)</center>"
	
	strng['success_datetime_selected'] = u"Date and times saved successfully! You can select more dates and times to play this game."
	strng['success_datetime_committed'] = u"Date and times saved successfully! Date and time of game has been set with the preferences of your oponent. Show details of game to see when you have to play this game."
	strng['datetime_selected_players'] = u"Date and time selected by players"
	strng['button_select_datetime'] = u"Save date and times to play"
	strng['button_delete_datetimes'] = u"Remove date(s)"
	
	### MYQUESTIONREVIEWS.HTML ###
	strng['title_my_admin_question_reviews'] = u"My Tournament's Question Reviews"

	### MYTOURNAMENTS.HTML ###
	strng['title_my_active_tournaments'] = u"My Active Tournaments"
	strng['title_my_active_admin_tournaments'] = u"My Active Admin Tournaments"
	strng['title_my_finished_tournaments'] = u" My Finished Tournaments"	
	strng['tournament_categories'] = u"Categories selected"
	strng['tournament_start_date'] = u"Start date"
	strng['tournament_finish_date'] = u"Finish date"
	
	strng['error_no_active_tournaments'] = u"Sorry! You haven't any Tournament active now."
	strng['error_no_admin_active_tournaments'] = u"Sorry! You haven't any Tournament with admin permissions active now."
	strng['error_no_won_games'] = u"Sorry! You haven't won any Game."
	strng['error_no_lost_games'] = u"Sorry! You haven't lost any Game."	

	### NEWTOURNAMENT.HTML ###
	strng['title_new_tournament'] = u"Create New Tournament"
	strng['button_new_tournament'] = u"Create New Tournament"
	
	strng['success_create_new_tournament'] = u"Tournament created successfully!"
	
	strng['error_new_tournament_name_exists'] = u"Exists in our database. Choose other."
	
	### NEWQUESTIONREVIEW.HTML ###
	strng['title_new_question_review'] = u"New Question Review"
	strng['label_question_id'] = u"Question #ID"
	strng['label_arguments'] = u"Your arguments"
	strng['button_new_question_review'] = u"Send Question Review"

	### PLAY.HTML ###
	strng['title_play'] = u"Play Now With Webchat Freenode"

	### PROFILE.HTML ###
	strng['title_profile_hi'] = u"Hi"
	strng['profile_last_login'] = u"Last login"
	
	### QUESTIONREVIEW.HTML ###
	strng['title_question_reviews'] = u"Question Review"
	strng['warning_waiting_resolution'] = u"Waiting a resolution by admin"
	strng['arguments'] = u"Arguments"
	strng['resolution'] = u"Resolution"	
	strng['button_save_question_review_resolution'] = u"Add resolution and close review"
	
	strng['error_question_review_no_exists'] = u"Sorry! This question review doesn't exists in our database!"
	strng['success_resolution'] = u"Your resolution has been saved successfully!"
	
	### RECOVERUSER.HTML ###
	strng['label_recover_username'] = u"Write your username registered"
	strng['label_recover_email'] = u"Write your email registered"
	
	strng['title_recover_account'] = u"Recover Account"	
	strng['title_recover_account_new_password'] = u"Change My Password"	
	
	strng['button_recover_account'] = u"Recover Account"
	strng['button_recover_account_new_password'] = u"Set my new Password"
	
	strng['success_recover_account_email_sent'] = u"A message has been sent to verify your email and can recover your account."

	strng['error_recover_account'] = u"One or more errors. Try again"	
	strng['error_unknown_code'] = u"ERROR! Code used to recover an account is wrong."
	strng['error_recover_user_unknown'] = u"This username doesn't exist in our database."
	strng['error_recover_email_unknown'] = u"This email doesn't exist in our database."
	strng['error_recover_user_email_differents'] = u"The username and password you enter do not match both for any user. Try again."

	### TOURNAMENTINFO.HTML ###
	strng['title_info'] = u"Info"
	strng['title_table'] = u"Tournament Table"
	strng['title_tournament_games'] = u"Tournament Games"
	strng['number_rounds'] = u"Number of Rounds"
	strng['remember'] = u"Remember!"
	strng['joined_tournament'] = u"You joined to play this Tournament!"
	
	strng['button_join'] = u"Join to this Tournament Now"

	strng['warning_you_tournament_admin'] = u"You're the admin of this Tournament"
	strng['warning_only_admin'] = u"Only visible for admin tournament or admin system."
	strng['warning_only_players'] = u"Only visible for players."	

	strng['error_you_tournament_admin'] = u"You're the admin of this Tournament"
	strng['error_tournament_no_games'] = u"Sorry! This Tournament hasn't any games!"

	### TOURNAMENTS.HTML ###
	# Next Tournaments
	strng['success_join_tournament'] = u"You have been joined successfully!"
	
	strng['info_join_tournaments'] = u"We've seen that you haven't joined any Tournament. Do you want to play? Select one in <u>Next Tournaments</u> section!"	
	strng['info_new_tournament'] = u"We've seen that you haven't joined any Tournament and you haven't create anyone. Create a Tournament in this section or join a Tournament to play in <u><a href='/tournaments'>Next Tournaments</a></u> section! "		
	
	strng['error_join_tournament'] = u"Error! You can't join to this Tournament"
	strng['error_join_tournament_admin'] = u"Error! You can't join to this Tournament: admin's tournament can't play!"
	strng['error_join_tournament_joined'] = u"Error! You can't join to this Tournament: you have joined it before!"
	strng['error_join_tournament_expired'] = u"Error! You can't join to this Tournament: join period expired!"
	strng['error_tournament_no_exists'] = u"Error! Tournament selected doesn't exists!"
	strng['error_no_next_tournaments'] = u"Sorry! System hasn't got any next Tournament."
	strng['error_no_active_tournaments'] = u"Sorry! System hasn't got any active Tournament."

	strng['title_next_tournaments'] = u"Next Tournaments"
	strng['title_active_tournaments'] = u"Active Tournaments"
	strng['title_finished_tournaments'] = u"Last Finished Tournaments"
	strng['join'] = u"Join"
	
	strng['tournament_started_date'] = u"Started date"
	strng['tournament_finished_date'] = u"Finished date"
	
	### SIDEBAR ###

	strng['title_sidebar_my_active_tournaments'] = u"My Active Tournaments"
	strng['title_sidebar_my_admin_tournaments'] = u"My Admin Tournaments"
	strng['title_sidebar_today_games'] = u"Today Games"
	strng['title_sidebar_next_games'] = u"Next Games"
	strng['committed'] = u"Committed!"
	strng['uncommitted'] = u"Uncommitted!"	
	
	strng['error_sidebar_no_active_tournaments'] = u"No active tournaments."
	strng['error_sidebar_no_admin_active_tournaments'] = u"No admin active tournaments."

	return strng
