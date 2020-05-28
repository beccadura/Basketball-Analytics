#!/usr/bin/env python3

from flask import Flask 
# app = Flask(__name__)

#import Basketball
import TeamStats
import Team
import PlayerStats
import bs4
from bs4 import BeautifulSoup
import urllib.request
from flask import render_template
from flask import request, g, Response
from urllib.request import Request, urlopen
from flask import jsonify

from TeamStats import *
import re

from bs4 import BeautifulSoup
import urllib
import json

app = Flask(__name__, template_folder='template')




@app.route('/playerstats') 
def PlayerStats_form():
	return render_template('game.html', fieldname = "Season", fieldname2 = "Statistics", fieldname3 = "Games Included")

@app.route("/playerstats/<URL>")
# def PlayerStats(URL, stats):
def PlayerStatistics(URL, stats, games_included):
	# visiting_team = Team("Drake")
	# visitingDictionary = {}


	game_data = []

	game_soup = BeautifulSoup(urllib.request.urlopen("https://static.godrakebulldogs.com/custompages/Statistics/" + URL).read(), features = "lxml")


	    #Scrapes the stats for the first half of the game
	game_tbody = game_soup('table')[0].find_all('tr')

	for col in game_tbody:
	    rows = col.findChildren(recursive = False)
	    rows[0] = rows[0].text.strip()
	    rows[1] = rows[1].text.strip()
	    rows[2] = rows[2].text.strip()
	        # rows = [ele.text.strip() for ele in rows]
	    game_data.append(rows)

	row_number = 1
	for row in game_data[1:]:
		index = str(row[3].find('a'))
		if URL == "mbb-17-18/teamstat.htm":
			url2 = index[9:18]
			final_url = str("https://static.godrakebulldogs.com/custompages/Statistics/mbb-17-18/" + url2)
		elif URL == "mbb-18-19/teamstat.htm":
			url2 = index[9:17]
			final_url = str("https://static.godrakebulldogs.com/custompages/Statistics/mbb-18-19/" + url2)
		(game_data[row_number])[3] = final_url
		row_number += 1

	for row in game_data:
	    date = row[0]
	    location = row[1]
	    result = row[2]
	    url = row[3]

	    # for row in data[1:]:
	    #     print(row[0:4])
	# if games_included == home:
	# 	if "Des Moines, IA" in row[1]:
	# 		x = str(row[3])
	#     	home_url_options.append(x)
	# elif games_included == away:
	# 	if "Des Moines, IA" not in row[1]:
	# 		x = str(row[3])
	#     	home_url_options.append(x)
	# else:
	# 	x = str(row[3])
	#     url_options.append(x)


	url_options = []
	home_url_options = []
	visiting_url_options = []

	for row in game_data[1:]:
		if games_included == "home":
			#print(row[1])
			if "Des Moines" in row[1]:
				x = str(row[3])
				#print(x)
				home_url_options.append(x)
		elif games_included == "away":
			if "Des Moines" not in str(row[1]):
				x = str(row[3])
				visiting_url_options.append(x)
				#print(visiting_url_options)
		elif games_included == "all_games":
			x = str(row[3])
			url_options.append(x)
	    # x = str(row[3])
	    # url_options.append(x)
	

	visitingDictionary = {}
	homeDictionary = {}
	Dictionary = {}

	if games_included == "home":
		home_team = Team("Drake")
		# homeDictionary = {}
		num = len(home_url_options)
		last_five_games = home_url_options[num-5:num]
	elif games_included == "away":
		visiting_team = Team("Drake")
		# visitingDictionary = {}
		num = len(visiting_url_options)
		last_five_games = visiting_url_options[num-5:num]
	elif games_included == "all_games":
		team = Team("Drake")
		# Dictionary = {}
		num = len(url_options)
		last_five_games = url_options[num-5:num]


	# num = len(url_options)
	# last_five_games = url_options[num-5:num]
	#print(last_five_games)

	if games_included == "home" or games_included == "away":

		for game in last_five_games:


		    # if game == "https://static.godrakebulldogs.com/custompages/Statistics/mbb-17-18/du-15.htm":
		    # 	for x in visiting_team.get_tuple():
		    # 		visiting_team.sub_out(x)
		    # 	continue

		    	
		    data = []
		    data2 = []

		    soup = BeautifulSoup(urllib.request.urlopen(game).read(), features = "lxml")


		    tbody = soup('table', {"style":"font-family:verdana;color:black;background:white;font-size:xx-small;text-align:right;"})[1].find_all('tr')
		    tbody2 = soup('table', {"style":"font-family:verdana;color:black;background:white;font-size:xx-small;text-align:right;"})[3].find_all('tr')



		    	


		    #Scrapes the stats for the first half of the game
		    #tbody = soup('table', {"style":"font-family:verdana;color:black;background:white;font-size:xx-small;text-align:right;"})[1].find_all('tr')

		    for col in tbody:
		        rows = col.findChildren(recursive = False)
		        rows = [ele.text.strip() for ele in rows]
		        data.append(rows)

		    #print(tbody)

		    
		    #tbody2 = soup('table', {"style":"font-family:verdana;color:black;background:white;font-size:xx-small;text-align:right;"})[3].find_all('tr')

		    for col in tbody2:
		    	rows2 = col.findChildren(recursive = False)
		    	rows2 = [ele.text.strip() for ele in rows2]
		    	data2.append(rows2)


		    headers = data[0]



		    for x in headers:
		        visitors_match = re.search("VISITORS: Drake", x)
		        home_match = re.search("HOME TEAM: Drake", x)
		        if visitors_match or home_match:
		            break

		    # if home_match:
		    # 	continue


		    if visitors_match:
		        visiting_team = Team("Drake")

		        players = []

		        tbody3 = soup('table', {"border": "0", "cellspacing": "0", "cellpadding": "2"})[0].find_all('tr', {"bgcolor": "#ffffff"})


		       # if URL == "mbb-17-18/teamstat.htm":
		        #	tbody3 = soup('table', {"border": "0", "cellspacing": "0", "cellpadding": "2"})[0].find_all('tr', {"bgcolor": "#ffffff"})
		        #elif URL == "mbb-18-19/teamstat.htm":
		        #	tbody3 = soup('table')[2].find_all('tr', {"bgcolor": "#ffffff"})

		        for col in tbody3:
		            rows = col.findChildren(recursive=False)
		            rows = [ele.text.strip() for ele in rows]
		            players.append(rows)

		        row_number = 0
		        for row in players:
		            match = re.search(r'TM', str(row))
		            if match:
		                break
		            else:
		                row_number += 1

		        players = players[:row_number]

		        for row in players:
		            player_name = row[1]
		            if player_name not in visiting_team.roster:
		            	visiting_team.add_to_roster(PlayerStats(player_name))


		        for row in players[0:5]:
		            player_name = row[1]
		            visiting_team.sub_in(player_name)
		        #print(str(players))




		    #####AUTOMATED#####
		    # elif headers[0] == "HOME TEAM: Drake":

		    elif home_match:
		        home_team = Team("Drake")


		        players = []

		        tbody4 = soup('table', {"border": "0", "cellspacing": "0", "cellpadding": "2"})[1].find_all('tr', {"bgcolor": "#ffffff"})


		        #if URL == "mbb-17-18/teamstat.htm":
		        #	tbody4 = soup('table', {"border": "0", "cellspacing": "0", "cellpadding": "2"})[1].find_all('tr', {"bgcolor": "#ffffff"})
		        #elif URL == "mbb-18-19/teamstat.htm":
		        #	tbody4 = soup('table')[3].find_all('tr', {"bgcolor": "#ffffff"})
		        	# tbody4 = soup('table')[3].find_all('tr', {"bgcolor": "#ffffff"})
		        	#tbody4 = soup('table', {"border": "0", "cellspacing": "0", "cellpadding": "2"})[1].find_all('tr', {"bgcolor": "#ffffff"})
		   

		        for col in tbody4:
		            rows = col.findChildren(recursive=False)
		            rows = [ele.text.strip() for ele in rows]
		            players.append(rows)


		        row_number = 0
		        for row in players:
		            match = re.search(r'TM', str(row))
		            if match:
		                break
		            else:
		                row_number += 1

		        players = players[:row_number]

		        for row in players:
		            player_name = row[1]
		            if player_name not in home_team.roster:
		            	home_team.add_to_roster(PlayerStats(player_name))
		            # home_team.add_to_roster(PlayerStats(player_name))


		        for row in players[0:5]:
		            player_name = row[1]
		            home_team.sub_in(player_name)
		            # if player_name not in home_team.roster:
		            # 	home_team.sub_in(player_name)

		        #print(str(players))


		    #####AUTOMATED#####
		    if visitors_match:
		        # visitingDictionary = {}
		        visitingDictionary[visiting_team.get_tuple()] = TeamStats()

		        for row in data:

		            home = row[0]
		            visitors = row[4]

		            # entered game
		            match = re.search(r'SUB IN : (.*)', str(visitors))
		            if match:
		                subin = match.group(1)
		                if any(i.isdigit() for i in subin):
		                	break
		                else:
		                	if (subin not in visiting_team.roster) and (subin not in visiting_team.group_of_five):
		                		visiting_team.add_to_roster(PlayerStats(subin))
		                	visiting_team.sub_in(subin)

		            # exited game
		            match = re.search(r'SUB OUT: (.*)', str(visitors))
		            if match:
		                subout = match.group(1)
		                if any(i.isdigit() for i in subin):
		                	break
		                else:
		                	visiting_team.sub_out(subout)

		            # 2 pointer
		            match = re.search(r'GOOD! (DUNK|LAYUP|JUMPER) by (.*)', str(visitors))
		            if match:
		                player = match.group(2)
		                visiting5tuple = visiting_team.get_tuple()
		                if not (visiting5tuple in visitingDictionary):
		                    visitingDictionary[visiting5tuple] = TeamStats()
		                visitingDictionary[visiting5tuple].points_for += 2
		                visitingDictionary[visiting5tuple].shot_attempts += 1

		            # FT
		            match = re.search(r'GOOD! FT SHOT by (.*)', str(visitors))
		            if match:
		                player = match.group(1)
		                visiting5tuple = visiting_team.get_tuple()
		                if not (visiting5tuple in visitingDictionary):
		                    visitingDictionary[visiting5tuple] = TeamStats()
		                visitingDictionary[visiting5tuple].points_for += 1
		                visitingDictionary[visiting5tuple].FT_attempted += 1

		            # 3 Pointer
		            match = re.search(r'GOOD! 3 PTR by (.*)', str(visitors))
		            if match:
		                player = match.group(1)
		                visiting5tuple = visiting_team.get_tuple()
		                if not (visiting5tuple in visitingDictionary):
		                    visitingDictionary[visiting5tuple] = TeamStats()
		                visitingDictionary[visiting5tuple].points_for += 3
		                visitingDictionary[visiting5tuple].shot_attempts += 1

		            # Fouls by
		            match = re.search(r'FOUL by (.*)', str(visitors))
		            if match:
		                player = match.group(1)
		                visiting5tuple = visiting_team.get_tuple()
		                if not (visiting5tuple in visitingDictionary):
		                    visitingDictionary[visiting5tuple] = TeamStats()
		                visitingDictionary[visiting5tuple].Fouls_by_Team += 1

		            # Assists
		            match = re.search(r'ASSIST (.*)', str(visitors))
		            if match:
		                player = match.group(1)
		                visiting5tuple = visiting_team.get_tuple()
		                if not (visiting5tuple in visitingDictionary):
		                    visitingDictionary[visiting5tuple] = TeamStats()
		                visitingDictionary[visiting5tuple].assists += 1

		            # Turnovers
		            match = re.search(r'TURNOVR (.*)', str(visitors))
		            if match:
		                player = match.group(1)
		                visiting5tuple = visiting_team.get_tuple()
		                if player not in visiting5tuple:
		                	# player_list = [x for x in visiting_team.roster if x.name == player]
		                	# visiting_team.group_of_five.append(player_list[0])
		                	# visiting_team.group_of_five.append(player)
		                	#visiting_team.roster.remove(player)
		                	visiting5tuple = visiting_team.get_tuple()
		                if not (visiting5tuple in visitingDictionary):
		                    visitingDictionary[visiting5tuple] = TeamStats()
		                visitingDictionary[visiting5tuple].turnovers += 1

		            # POINTS AGAINST
		            # 2 pointer
		            match = re.search(r'GOOD! (DUNK|LAYUP|JUMPER) by (.*)', str(home))
		            if match:
		                player = match.group(2)
		                visiting5tuple = visiting_team.get_tuple()
		                if not (visiting5tuple in visitingDictionary):
		                    visitingDictionary[visiting5tuple] = TeamStats()
		                visitingDictionary[visiting5tuple].points_against += 2


		            # FT
		            match = re.search(r'GOOD! FT SHOT by (.*)', str(home))
		            if match:
		                player = match.group(1)
		                visiting5tuple = visiting_team.get_tuple()
		                if not (visiting5tuple in visitingDictionary):
		                    visitingDictionary[visiting5tuple] = TeamStats()
		                visitingDictionary[visiting5tuple].points_against += 1



		            # 3 Pointer
		            match = re.search(r'GOOD! 3 PTR by (.*)', str(home))
		            if match:
		                player = match.group(1)
		                visiting5tuple = visiting_team.get_tuple()
		                if not (visiting5tuple in visitingDictionary):
		                    visitingDictionary[visiting5tuple] = TeamStats()
		                visitingDictionary[visiting5tuple].points_against += 3

		            # Fouls
		            match = re.search(r'FOUL by (.*)', str(home))
		            if match:
		                player = match.group(1)
		                visiting5tuple = visiting_team.get_tuple()
		                if not (visiting5tuple in visitingDictionary):
		                    visitingDictionary[visiting5tuple] = TeamStats()
		                visitingDictionary[visiting5tuple].Fouls_by_Opponent += 1

		            # Assists Against
		            match = re.search(r'ASSIST (.*)', str(home))
		            if match:
		                player = match.group(1)
		                visiting5tuple = visiting_team.get_tuple()
		                if not (visiting5tuple in visitingDictionary):
		                    visitingDictionary[visiting5tuple] = TeamStats()
		                visitingDictionary[visiting5tuple].assists_against += 1

		            # Turnovers Forced
		            match = re.search(r'TURNOVR (.*)', str(home))
		            if match:
		                player = match.group(1)
		                visiting5tuple = visiting_team.get_tuple()
		                if not (visiting5tuple in visitingDictionary):
		                    visitingDictionary[visiting5tuple] = TeamStats()
		                visitingDictionary[visiting5tuple].turnovers_forced += 1




		             ############MISSED
		            # 2 pointer
		            match = re.search(r'MISSED (DUNK|LAYUP|JUMPER) by (.*)', str(visitors))
		            if match:
		                player = match.group(2)
		                visiting5tuple = visiting_team.get_tuple()
		                if not (visiting5tuple in visitingDictionary):
		                    visitingDictionary[visiting5tuple] = TeamStats()
		                visitingDictionary[visiting5tuple].shots_missed += 1
		                visitingDictionary[visiting5tuple].shot_attempts += 1

		            # FT
		            match = re.search(r'MISSED FT SHOT by (.*)', str(visitors))
		            if match:
		                player = match.group(1)
		                visiting5tuple = visiting_team.get_tuple()
		                if not (visiting5tuple in visitingDictionary):
		                    visitingDictionary[visiting5tuple] = TeamStats()
		                visitingDictionary[visiting5tuple].FT_missed += 1
		                visitingDictionary[visiting5tuple].FT_attempted += 1

		            # 3 Pointer
		            match = re.search(r'MISSED 3 PTR by (.*)', str(visitors))
		            if match:
		                player = match.group(1)
		                visiting5tuple = visiting_team.get_tuple()
		                if not (visiting5tuple in visitingDictionary):
		                    visitingDictionary[visiting5tuple] = TeamStats()
		                visitingDictionary[visiting5tuple].shots_missed += 1
		                visitingDictionary[visiting5tuple].shot_attempts += 1




		        for x in visiting_team.get_tuple():
		        	visiting_team.sub_out(x)

		        for row in players[0:5]:
		        	player_name = row[1]
		        	visiting_team.sub_in(player_name)






		        for row in data2:

		            home = row[0]
		            visitors = row[4]

		            # entered game
		            match = re.search(r'SUB IN : (.*)', str(visitors))
		            if match:
		                subin = match.group(1)
		                if any(i.isdigit() for i in subin):
		                	break
		                else:
		                	if (subin not in visiting_team.roster) and (subin not in visiting_team.group_of_five):
		                		visiting_team.add_to_roster(PlayerStats(subin))
		                	visiting_team.sub_in(subin)

		            # exited game
		            match = re.search(r'SUB OUT: (.*)', str(visitors))
		            if match:
		                subout = match.group(1)
		                if any(i.isdigit() for i in subin):
		                	break
		                else:
		                	visiting_team.sub_out(subout)


		            # 2 pointer
		            match = re.search(r'GOOD! (DUNK|LAYUP|JUMPER) by (.*)', str(visitors))
		            if match:
		                player = match.group(2)
		                visiting5tuple = visiting_team.get_tuple()
		                if not (visiting5tuple in visitingDictionary):
		                    visitingDictionary[visiting5tuple] = TeamStats()
		                visitingDictionary[visiting5tuple].points_for += 2
		                visitingDictionary[visiting5tuple].shot_attempts += 1

		            # FT
		            match = re.search(r'GOOD! FT SHOT by (.*)', str(visitors))
		            if match:
		                player = match.group(1)
		                visiting5tuple = visiting_team.get_tuple()
		                if not (visiting5tuple in visitingDictionary):
		                    visitingDictionary[visiting5tuple] = TeamStats()
		                visitingDictionary[visiting5tuple].points_for += 1
		                visitingDictionary[visiting5tuple].FT_attempted += 1

		            # 3 Pointer
		            match = re.search(r'GOOD! 3 PTR by (.*)', str(visitors))
		            if match:
		                player = match.group(1)
		                visiting5tuple = visiting_team.get_tuple()
		                if not (visiting5tuple in visitingDictionary):
		                    visitingDictionary[visiting5tuple] = TeamStats()
		                visitingDictionary[visiting5tuple].points_for += 3
		                visitingDictionary[visiting5tuple].shot_attempts += 1

		            # Fouls by
		            match = re.search(r'FOUL by (.*)', str(visitors))
		            if match:
		                player = match.group(1)
		                visiting5tuple = visiting_team.get_tuple()
		                if not (visiting5tuple in visitingDictionary):
		                    visitingDictionary[visiting5tuple] = TeamStats()
		                visitingDictionary[visiting5tuple].Fouls_by_Team += 1

		            # Assists
		            match = re.search(r'ASSIST (.*)', str(visitors))
		            if match:
		                player = match.group(1)
		                visiting5tuple = visiting_team.get_tuple()
		                if not (visiting5tuple in visitingDictionary):
		                    visitingDictionary[visiting5tuple] = TeamStats()
		                visitingDictionary[visiting5tuple].assists += 1

		            # Turnovers
		            match = re.search(r'TURNOVR (.*)', str(visitors))
		            if match:
		                player = match.group(1)
		                visiting5tuple = visiting_team.get_tuple()
		                if not (visiting5tuple in visitingDictionary):
		                    visitingDictionary[visiting5tuple] = TeamStats()
		                visitingDictionary[visiting5tuple].turnovers += 1

		            # POINTS AGAINST
		            # 2 pointer
		            match = re.search(r'GOOD! (DUNK|LAYUP|JUMPER) by (.*)', str(home))
		            if match:
		                player = match.group(2)
		                visiting5tuple = visiting_team.get_tuple()
		                if not (visiting5tuple in visitingDictionary):
		                    visitingDictionary[visiting5tuple] = TeamStats()
		                visitingDictionary[visiting5tuple].points_against += 2


		            # FT
		            match = re.search(r'GOOD! FT SHOT by (.*)', str(home))
		            if match:
		                player = match.group(1)
		                visiting5tuple = visiting_team.get_tuple()
		                if not (visiting5tuple in visitingDictionary):
		                    visitingDictionary[visiting5tuple] = TeamStats()
		                visitingDictionary[visiting5tuple].points_against += 1



		            # 3 Pointer
		            match = re.search(r'GOOD! 3 PTR by (.*)', str(home))
		            if match:
		                player = match.group(1)
		                visiting5tuple = visiting_team.get_tuple()
		                if not (visiting5tuple in visitingDictionary):
		                    visitingDictionary[visiting5tuple] = TeamStats()
		                visitingDictionary[visiting5tuple].points_against += 3

		            # Fouls
		            match = re.search(r'FOUL by (.*)', str(home))
		            if match:
		                player = match.group(1)
		                visiting5tuple = visiting_team.get_tuple()
		                if not (visiting5tuple in visitingDictionary):
		                    visitingDictionary[visiting5tuple] = TeamStats()
		                visitingDictionary[visiting5tuple].Fouls_by_Opponent += 1

		            # Assists Against
		            match = re.search(r'ASSIST (.*)', str(home))
		            if match:
		                player = match.group(1)
		                visiting5tuple = visiting_team.get_tuple()
		                if not (visiting5tuple in visitingDictionary):
		                    visitingDictionary[visiting5tuple] = TeamStats()
		                visitingDictionary[visiting5tuple].assists_against += 1

		            # Turnovers Forced
		            match = re.search(r'TURNOVR (.*)', str(home))
		            if match:
		                player = match.group(1)
		                visiting5tuple = visiting_team.get_tuple()
		                if not (visiting5tuple in visitingDictionary):
		                    visitingDictionary[visiting5tuple] = TeamStats()
		                visitingDictionary[visiting5tuple].turnovers_forced += 1




		             ############MISSED
		            # 2 pointer
		            match = re.search(r'MISSED (DUNK|LAYUP|JUMPER) by (.*)', str(visitors))
		            if match:
		                player = match.group(2)
		                visiting5tuple = visiting_team.get_tuple()
		                if not (visiting5tuple in visitingDictionary):
		                    visitingDictionary[visiting5tuple] = TeamStats()
		                visitingDictionary[visiting5tuple].shots_missed += 1
		                visitingDictionary[visiting5tuple].shot_attempts += 1

		            # FT
		            match = re.search(r'MISSED FT SHOT by (.*)', str(visitors))
		            if match:
		                player = match.group(1)
		                visiting5tuple = visiting_team.get_tuple()
		                if not (visiting5tuple in visitingDictionary):
		                    visitingDictionary[visiting5tuple] = TeamStats()
		                visitingDictionary[visiting5tuple].FT_missed += 1
		                visitingDictionary[visiting5tuple].FT_attempted += 1

		            # 3 Pointer
		            match = re.search(r'MISSED 3 PTR by (.*)', str(visitors))
		            if match:
		                player = match.group(1)
		                visiting5tuple = visiting_team.get_tuple()
		                if not (visiting5tuple in visitingDictionary):
		                    visitingDictionary[visiting5tuple] = TeamStats()
		                visitingDictionary[visiting5tuple].shots_missed += 1
		                visitingDictionary[visiting5tuple].shot_attempts += 1




		# num_keys = len(visitingDictionary)
		# html_list = []
		# html_string = ''

		# for x in range(0,num_keys):

		#     key = str(list(visitingDictionary.keys())[x])
		#         # value = str(list(visitingDictionary.values())[x])
		#     if stats == 'points_for':
		#     	stat = "Points Scored: " + str(list(visitingDictionary.values())[x].points_for)
		#     elif stats == 'shots_missed':
		#     	stat = "Shots Missed: " + str(list(visitingDictionary.values())[x].shots_missed)
		#     elif stats == 'shot_attempts':
		#     	stat = "Shots Attempted: " + str(list(visitingDictionary.values())[x].shot_attempts)
		#     elif stats == 'Fouls_by_Team':
		#     	stat = "Fouls by Team: " + str(list(visitingDictionary.values())[x].Fouls_by_Team)
		#     elif stats == 'assists':
		#     	stat = "Assists: " + str(list(visitingDictionary.values())[x].assists)
		#     elif stats == 'turnovers':
		#     	stat = "Turnovers: " + str(list(visitingDictionary.values())[x].turnovers)
		#     elif stats == 'points_against':
		#     	stat = "Points Against: " + str(list(visitingDictionary.values())[x].points_against)
		#     elif stats == 'Fouls_by_Opponent':
		#     	stat = "Fouls by Opponent: " + str(list(visitingDictionary.values())[x].Fouls_by_Opponent)
		#     elif stats == 'assists_against':
		#     	stat = "Assists Against: " + str(list(visitingDictionary.values())[x].assists_against)
		#     elif stats == 'turnovers_forced':
		#     	stat = "Turnovers Forced: " + str(list(visitingDictionary.values())[x].turnovers_forced)
		#     elif stats == 'FT_missed':
		#     	stat = "Free Throws Missed: " + str(list(visitingDictionary.values())[x].FT_missed)
		#     elif stats == 'FT_attempted':
		#     	stat = "Free Throws Attempted: " + str(list(visitingDictionary.values())[x].FT_attempted)
		#     else:
		#     	stat = "No statistic was chosen."

		#     html_list.append("<h3 align = 'left'>" + key + "</h3> <p align = 'left'>" + stat +  "</p>")

		# html_string = html_string.join(html_list)

		# return html_string




		    ####AUTOMATED#####
		    elif home_match:
		        # visitingDictionary = {}
		        homeDictionary[home_team.get_tuple()] = TeamStats()

		        for row in data:

		            home = row[0]
		            visitors = row[4]

		            # entered game
		            match = re.search(r'SUB IN : (.*)', str(home))
		            if match:
		                subin = match.group(1)
		                if any(i.isdigit() for i in subin):
		                	break
		                else:
		                	if (subin not in home_team.roster) and (subin not in home_team.group_of_five):
		                		home_team.add_to_roster(PlayerStats(subin))
		                	home_team.sub_in(subin)

		            # exited game
		            match = re.search(r'SUB OUT: (.*)', str(home))
		            if match:
		                subout = match.group(1)
		                if any(i.isdigit() for i in subin):
		                	break
		                else:
		                	home_team.sub_out(subout)


		            # 2 pointer
		            match = re.search(r'GOOD! (DUNK|LAYUP|JUMPER) by (.*)', str(home))
		            if match:
		                player = match.group(2)
		                home5tuple = home_team.get_tuple()
		                if not (home5tuple in homeDictionary):
		                    homeDictionary[home5tuple] = TeamStats()
		                homeDictionary[home5tuple].points_for += 2
		                homeDictionary[home5tuple].shot_attempts += 1

		            # FT
		            match = re.search(r'GOOD! FT SHOT by (.*)', str(home))
		            if match:
		                player = match.group(1)
		                home5tuple = home_team.get_tuple()
		                if not (home5tuple in homeDictionary):
		                    homeDictionary[home5tuple] = TeamStats()
		                homeDictionary[home5tuple].points_for += 1
		                homeDictionary[home5tuple].FT_attempted += 1

		            # 3 Pointer
		            match = re.search(r'GOOD! 3 PTR by (.*)', str(home))
		            if match:
		                player = match.group(1)
		                home5tuple = home_team.get_tuple()
		                if not (home5tuple in homeDictionary):
		                    homeDictionary[home5tuple] = TeamStats()
		                homeDictionary[home5tuple].points_for += 3
		                homeDictionary[home5tuple].shot_attempts += 1

		            # Fouls by
		            match = re.search(r'FOUL by (.*)', str(home))
		            if match:
		                player = match.group(1)
		                home5tuple = home_team.get_tuple()
		                if not (home5tuple in homeDictionary):
		                    homeDictionary[home5tuple] = TeamStats()
		                homeDictionary[home5tuple].Fouls_by_Team += 1

		            # Assists
		            match = re.search(r'ASSIST (.*)', str(home))
		            if match:
		                player = match.group(1)
		                home5tuple = home_team.get_tuple()
		                if not (home5tuple in homeDictionary):
		                    homeDictionary[home5tuple] = TeamStats()
		                homeDictionary[home5tuple].assists += 1

		            # Turnovers
		            match = re.search(r'TURNOVR (.*)', str(home))
		            if match:
		                player = match.group(1)
		                home5tuple = home_team.get_tuple()
		                if player not in home5tuple:
		                	# player_list = [x for x in visiting_team.roster if x.name == player]
		                	# visiting_team.group_of_five.append(player_list[0])
		                	# visiting_team.group_of_five.append(player)
		                	#visiting_team.roster.remove(player)
		                	home5tuple = home_team.get_tuple()
		                if not (home5tuple in homeDictionary):
		                    homeDictionary[home5tuple] = TeamStats()
		                homeDictionary[home5tuple].turnovers += 1

		            # POINTS AGAINST
		            # 2 pointer
		            match = re.search(r'GOOD! (DUNK|LAYUP|JUMPER) by (.*)', str(visitors))
		            if match:
		                player = match.group(2)
		                home5tuple = home_team.get_tuple()
		                if not (home5tuple in homeDictionary):
		                    homeDictionary[home5tuple] = TeamStats()
		                homeDictionary[home5tuple].points_against += 2


		            # FT
		            match = re.search(r'GOOD! FT SHOT by (.*)', str(visitors))
		            if match:
		                player = match.group(1)
		                home5tuple = home_team.get_tuple()
		                if not (home5tuple in homeDictionary):
		                    homeDictionary[home5tuple] = TeamStats()
		                homeDictionary[home5tuple].points_against += 1



		            # 3 Pointer
		            match = re.search(r'GOOD! 3 PTR by (.*)', str(visitors))
		            if match:
		                player = match.group(1)
		                home5tuple = home_team.get_tuple()
		                if not (home5tuple in homeDictionary):
		                    homeDictionary[home5tuple] = TeamStats()
		                homeDictionary[home5tuple].points_against += 3

		            # Fouls
		            match = re.search(r'FOUL by (.*)', str(visitors))
		            if match:
		                player = match.group(1)
		                home5tuple = home_team.get_tuple()
		                if not (home5tuple in homeDictionary):
		                    homeDictionary[home5tuple] = TeamStats()
		                homeDictionary[home5tuple].Fouls_by_Opponent += 1

		            # Assists Against
		            match = re.search(r'ASSIST (.*)', str(visitors))
		            if match:
		                player = match.group(1)
		                home5tuple = home_team.get_tuple()
		                if not (home5tuple in homeDictionary):
		                    homeDictionary[home5tuple] = TeamStats()
		                homeDictionary[home5tuple].assists_against += 1

		            # Turnovers Forced
		            match = re.search(r'TURNOVR (.*)', str(visitors))
		            if match:
		                player = match.group(1)
		                home5tuple = home_team.get_tuple()
		                if not (home5tuple in homeDictionary):
		                    homeDictionary[home5tuple] = TeamStats()
		                homeDictionary[home5tuple].turnovers_forced += 1




		             ############MISSED
		            # 2 pointer
		            match = re.search(r'MISSED (DUNK|LAYUP|JUMPER) by (.*)', str(home))
		            if match:
		                player = match.group(2)
		                home5tuple = home_team.get_tuple()
		                if not (home5tuple in homeDictionary):
		                    homeDictionary[home5tuple] = TeamStats()
		                homeDictionary[home5tuple].shots_missed += 1
		                homeDictionary[home5tuple].shot_attempts += 1

		            # FT
		            match = re.search(r'MISSED FT SHOT by (.*)', str(home))
		            if match:
		                player = match.group(1)
		                home5tuple = home_team.get_tuple()
		                if not (home5tuple in homeDictionary):
		                    homeDictionary[home5tuple] = TeamStats()
		                homeDictionary[home5tuple].FT_missed += 1
		                homeDictionary[home5tuple].FT_attempted += 1

		            # 3 Pointer
		            match = re.search(r'MISSED 3 PTR by (.*)', str(home))
		            if match:
		                player = match.group(1)
		                home5tuple = home_team.get_tuple()
		                if not (home5tuple in homeDictionary):
		                    homeDictionary[home5tuple] = TeamStats()
		                homeDictionary[home5tuple].shots_missed += 1
		                homeDictionary[home5tuple].shot_attempts += 1




		        for x in home_team.get_tuple():
		        	home_team.sub_out(x)

		        for row in players[0:5]:
		        	player_name = row[1]
		        	home_team.sub_in(player_name)






		        for row in data2:

		            home = row[0]
		            visitors = row[4]

		            # entered game
		            match = re.search(r'SUB IN : (.*)', str(home))
		            if match:
		                subin = match.group(1)
		                if any(i.isdigit() for i in subin):
		                	break
		                else:
		                	if (subin not in home_team.roster) and (subin not in home_team.group_of_five):
		                		home_team.add_to_roster(PlayerStats(subin))
		                	home_team.sub_in(subin)

		            # exited game
		            match = re.search(r'SUB OUT: (.*)', str(home))
		            if match:
		                subout = match.group(1)
		                if any(i.isdigit() for i in subin):
		                	break
		                else:
		                	home_team.sub_out(subout)


		            # 2 pointer
		            match = re.search(r'GOOD! (DUNK|LAYUP|JUMPER) by (.*)', str(home))
		            if match:
		                player = match.group(2)
		                home5tuple = home_team.get_tuple()
		                if not (home5tuple in homeDictionary):
		                    homeDictionary[home5tuple] = TeamStats()
		                homeDictionary[home5tuple].points_for += 2
		                homeDictionary[home5tuple].shot_attempts += 1

		            # FT
		            match = re.search(r'GOOD! FT SHOT by (.*)', str(home))
		            if match:
		                player = match.group(1)
		                home5tuple = home_team.get_tuple()
		                if not (home5tuple in homeDictionary):
		                    homeDictionary[home5tuple] = TeamStats()
		                homeDictionary[home5tuple].points_for += 1
		                homeDictionary[home5tuple].FT_attempted += 1

		            # 3 Pointer
		            match = re.search(r'GOOD! 3 PTR by (.*)', str(home))
		            if match:
		                player = match.group(1)
		                home5tuple = home_team.get_tuple()
		                if not (home5tuple in homeDictionary):
		                    homeDictionary[home5tuple] = TeamStats()
		                homeDictionary[home5tuple].points_for += 3
		                homeDictionary[home5tuple].shot_attempts += 1

		            # Fouls by
		            match = re.search(r'FOUL by (.*)', str(home))
		            if match:
		                player = match.group(1)
		                home5tuple = home_team.get_tuple()
		                if not (home5tuple in homeDictionary):
		                    homeDictionary[home5tuple] = TeamStats()
		                homeDictionary[home5tuple].Fouls_by_Team += 1

		            # Assists
		            match = re.search(r'ASSIST (.*)', str(home))
		            if match:
		                player = match.group(1)
		                home5tuple = home_team.get_tuple()
		                if not (home5tuple in homeDictionary):
		                    homeDictionary[home5tuple] = TeamStats()
		                homeDictionary[home5tuple].assists += 1

		            # Turnovers
		            match = re.search(r'TURNOVR (.*)', str(home))
		            if match:
		                player = match.group(1)
		                home5tuple = home_team.get_tuple()
		                if player not in home5tuple:
		                	# player_list = [x for x in visiting_team.roster if x.name == player]
		                	# visiting_team.group_of_five.append(player_list[0])
		                	# visiting_team.group_of_five.append(player)
		                	#visiting_team.roster.remove(player)
		                	home5tuple = home_team.get_tuple()
		                if not (home5tuple in homeDictionary):
		                    homeDictionary[home5tuple] = TeamStats()
		                homeDictionary[home5tuple].turnovers += 1

		            # POINTS AGAINST
		            # 2 pointer
		            match = re.search(r'GOOD! (DUNK|LAYUP|JUMPER) by (.*)', str(visitors))
		            if match:
		                player = match.group(2)
		                home5tuple = home_team.get_tuple()
		                if not (home5tuple in homeDictionary):
		                    homeDictionary[home5tuple] = TeamStats()
		                homeDictionary[home5tuple].points_against += 2


		            # FT
		            match = re.search(r'GOOD! FT SHOT by (.*)', str(visitors))
		            if match:
		                player = match.group(1)
		                home5tuple = home_team.get_tuple()
		                if not (home5tuple in homeDictionary):
		                    homeDictionary[home5tuple] = TeamStats()
		                homeDictionary[home5tuple].points_against += 1



		            # 3 Pointer
		            match = re.search(r'GOOD! 3 PTR by (.*)', str(visitors))
		            if match:
		                player = match.group(1)
		                home5tuple = home_team.get_tuple()
		                if not (home5tuple in homeDictionary):
		                    homeDictionary[home5tuple] = TeamStats()
		                homeDictionary[home5tuple].points_against += 3

		            # Fouls
		            match = re.search(r'FOUL by (.*)', str(visitors))
		            if match:
		                player = match.group(1)
		                home5tuple = home_team.get_tuple()
		                if not (home5tuple in homeDictionary):
		                    homeDictionary[home5tuple] = TeamStats()
		                homeDictionary[home5tuple].Fouls_by_Opponent += 1

		            # Assists Against
		            match = re.search(r'ASSIST (.*)', str(visitors))
		            if match:
		                player = match.group(1)
		                home5tuple = home_team.get_tuple()
		                if not (home5tuple in homeDictionary):
		                    homeDictionary[home5tuple] = TeamStats()
		                homeDictionary[home5tuple].assists_against += 1

		            # Turnovers Forced
		            match = re.search(r'TURNOVR (.*)', str(visitors))
		            if match:
		                player = match.group(1)
		                home5tuple = home_team.get_tuple()
		                if not (home5tuple in homeDictionary):
		                    homeDictionary[home5tuple] = TeamStats()
		                homeDictionary[home5tuple].turnovers_forced += 1




		             ############MISSED
		            # 2 pointer
		            match = re.search(r'MISSED (DUNK|LAYUP|JUMPER) by (.*)', str(home))
		            if match:
		                player = match.group(2)
		                home5tuple = home_team.get_tuple()
		                if not (home5tuple in homeDictionary):
		                    homeDictionary[home5tuple] = TeamStats()
		                homeDictionary[home5tuple].shots_missed += 1
		                homeDictionary[home5tuple].shot_attempts += 1

		            # FT
		            match = re.search(r'MISSED FT SHOT by (.*)', str(home))
		            if match:
		                player = match.group(1)
		                home5tuple = home_team.get_tuple()
		                if not (home5tuple in homeDictionary):
		                    homeDictionary[home5tuple] = TeamStats()
		                homeDictionary[home5tuple].FT_missed += 1
		                homeDictionary[home5tuple].FT_attempted += 1

		            # 3 Pointer
		            match = re.search(r'MISSED 3 PTR by (.*)', str(home))
		            if match:
		                player = match.group(1)
		                home5tuple = home_team.get_tuple()
		                if not (home5tuple in homeDictionary):
		                    homeDictionary[home5tuple] = TeamStats()
		                homeDictionary[home5tuple].shots_missed += 1
		                homeDictionary[home5tuple].shot_attempts += 1
		        # #homeDictionary = {}
		        # homeDictionary[home_team.get_tuple()] = TeamStats()

		        # for row in data:

		        #     home = row[0]
		        #     visitors = row[4]

		        #     #entered game
		        #     match = re.search(r'SUB IN : (.*)', str(home))
		        #     if match:
		        #         subin = match.group(1)
		        #         home_team.sub_in(subin)

		        #     #exited game
		        #     match = re.search(r'SUB OUT: (.*)', str(home))
		        #     if match:
		        #         subout = match.group(1)
		        #         home_team.sub_out(subout)

		        #     # 2 pointer
		        #     match = re.search(r'GOOD! (DUNK|LAYUP|JUMPER) by (.*)', str(home))
		        #     if match:
		        #         player = match.group(2)
		        #         home5tuple = home_team.get_tuple()
		        #         if not (home5tuple in homeDictionary):
		        #             homeDictionary[home5tuple] = TeamStats()
		        #         homeDictionary[home5tuple].points_for +=2
		        #         homeDictionary[home5tuple].shot_attempts += 1

		        #     # FT
		        #     match = re.search(r'GOOD! FT SHOT by (.*)', str(home))
		        #     if match:
		        #         player = match.group(1)
		        #         home5tuple = home_team.get_tuple()
		        #         if not (home5tuple in homeDictionary):
		        #             homeDictionary[home5tuple] = TeamStats()
		        #         homeDictionary[home5tuple].points_for += 1
		        #         homeDictionary[home5tuple].FT_attempted += 1

		        #     # 3 Pointer
		        #     match = re.search(r'GOOD! 3 PTR by (.*)', str(home))
		        #     if match:
		        #         player = match.group(1)
		        #         home5tuple = home_team.get_tuple()
		        #         if not (home5tuple in homeDictionary):
		        #             homeDictionary[home5tuple] = TeamStats()
		        #         homeDictionary[home5tuple].points_for += 3
		        #         homeDictionary[home5tuple].shot_attempts += 1

		        #     # Fouls
		        #     match = re.search(r'FOUL by (.*)', str(home))
		        #     if match:
		        #         player = match.group(1)
		        #         home5tuple = home_team.get_tuple()
		        #         if not (home5tuple in homeDictionary):
		        #             homeDictionary[home5tuple] = TeamStats()
		        #         homeDictionary[home5tuple].Fouls_by_Team += 1

		        #     # Assists
		        #     match = re.search(r'ASSIST (.*)', str(home))
		        #     if match:
		        #         player = match.group(1)
		        #         home5tuple = home_team.get_tuple()
		        #         if not (home5tuple in homeDictionary):
		        #             homeDictionary[home5tuple] = TeamStats()
		        #             homeDictionary[home5tuple].assists += 1

		        #     # Turnovers
		        #     match = re.search(r'TURNOVR (.*)', str(home))
		        #     if match:
		        #         player = match.group(1)
		        #         home5tuple = home_team.get_tuple()
		        #         if not (home5tuple in homeDictionary):
		        #             homeDictionary[home5tuple] = TeamStats()
		        #             homeDictionary[home5tuple].turnovers += 1



		        # #POINTS AGAINST
		        #     # 2 pointer
		        #     match = re.search(r'GOOD! (DUNK|LAYUP|JUMPER) by (.*)', str(visitors))
		        #     if match:
		        #         player = match.group(2)
		        #         home5tuple = home_team.get_tuple()
		        #         if not (home5tuple in homeDictionary):
		        #             homeDictionary[home5tuple] = TeamStats()
		        #         homeDictionary[home5tuple].points_against +=2


		        #     # FT
		        #     match = re.search(r'GOOD! FT SHOT by (.*)', str(visitors))
		        #     if match:
		        #         player = match.group(1)
		        #         home5tuple = home_team.get_tuple()
		        #         if not (home5tuple in homeDictionary):
		        #             homeDictionary[home5tuple] = TeamStats()
		        #         homeDictionary[home5tuple].points_against += 1


		        #     # 3 Pointer
		        #     match = re.search(r'GOOD! 3 PTR by (.*)', str(visitors))
		        #     if match:
		        #         player = match.group(1)
		        #         home5tuple = home_team.get_tuple()
		        #         if not (home5tuple in homeDictionary):
		        #             homeDictionary[home5tuple] = TeamStats()
		        #             homeDictionary[home5tuple].points_against += 3

		        #     # Fouls
		        #     match = re.search(r'FOUL by (.*)', str(visitors))
		        #     if match:
		        #         player = match.group(1)
		        #         home5tuple = home_team.get_tuple()
		        #         if not (home5tuple in homeDictionary):
		        #             homeDictionary[home5tuple] = TeamStats()
		        #             homeDictionary[home5tuple].Fouls_by_Opponent += 1

		        #     # Assists Against
		        #     match = re.search(r'ASSIST (.*)', str(visitors))
		        #     if match:
		        #         player = match.group(1)
		        #         home5tuple = home_team.get_tuple()
		        #         if not (home5tuple in homeDictionary):
		        #             homeDictionary[home5tuple] = TeamStats()
		        #             homeDictionary[home5tuple].assists_against += 1

		        #     # Turnovers Forced
		        #     match = re.search(r'TURNOVR (.*)', str(visitors))
		        #     if match:
		        #         player = match.group(1)
		        #         home5tuple = home_team.get_tuple()
		        #         if not (home5tuple in homeDictionary):
		        #             homeDictionary[home5tuple] = TeamStats()
		        #             homeDictionary[home5tuple].turnovers_forced += 1




		        #     ############MISSED
		        #     # 2 pointer
		        #     match = re.search(r'MISSED! (DUNK|LAYUP|JUMPER) by (.*)', str(home))
		        #     if match:
		        #         player = match.group(2)
		        #         home5tuple = home_team.get_tuple()
		        #         if not (home5tuple in homeDictionary):
		        #             homeDictionary[home5tuple] = TeamStats()
		        #         homeDictionary[home5tuple].shots_missed +=1
		        #         homeDictionary[home5tuple].shot_attempts += 1

		        #     # FT
		        #     match = re.search(r'MISSED! FT SHOT by (.*)', str(home))
		        #     if match:
		        #         player = match.group(1)
		        #         home5tuple = home_team.get_tuple()
		        #         if not (home5tuple in homeDictionary):
		        #             homeDictionary[home5tuple] = TeamStats()
		        #         homeDictionary[home5tuple].FT_missed += 1
		        #         homeDictionary[home5tuple].FT_attempted += 1

		        #     # 3 Pointer
		        #     match = re.search(r'MISSED! 3 PTR by (.*)', str(home))
		        #     if match:
		        #         player = match.group(1)
		        #         home5tuple = home_team.get_tuple()
		        #         if not (home5tuple in homeDictionary):
		        #             homeDictionary[home5tuple] = TeamStats()
		        #         homeDictionary[home5tuple].shots_missed += 3
		        #         homeDictionary[home5tuple].shot_attempts += 1


		if games_included == "home":

			num_keys = len(homeDictionary)
			html_list = []
			html_string = ''

			for x in range(0,num_keys):

			    key = str(list(homeDictionary.keys())[x])
			        # value = str(list(visitingDictionary.values())[x])
			    if stats == 'points_for':
			    	stat = "Points Scored: " + str(list(homeDictionary.values())[x].points_for)
			    elif stats == 'shots_missed':
			    	stat = "Shots Missed: " + str(list(homeDictionary.values())[x].shots_missed)
			    elif stats == 'shot_attempts':
			    	stat = "Shots Attempted: " + str(list(homeDictionary.values())[x].shot_attempts)
			    elif stats == 'Fouls_by_Team':
			    	stat = "Fouls by Team: " + str(list(homeDictionary.values())[x].Fouls_by_Team)
			    elif stats == 'assists':
			    	stat = "Assists: " + str(list(homeDictionary.values())[x].assists)
			    elif stats == 'turnovers':
			    	stat = "Turnovers: " + str(list(homeDictionary.values())[x].turnovers)
			    elif stats == 'points_against':
			    	stat = "Points Against: " + str(list(homeDictionary.values())[x].points_against)
			    elif stats == 'Fouls_by_Opponent':
			    	stat = "Fouls by Opponent: " + str(list(homeDictionary.values())[x].Fouls_by_Opponent)
			    elif stats == 'assists_against':
			    	stat = "Assists Against: " + str(list(homeDictionary.values())[x].assists_against)
			    elif stats == 'turnovers_forced':
			    	stat = "Turnovers Forced: " + str(list(homeDictionary.values())[x].turnovers_forced)
			    elif stats == 'FT_missed':
			    	stat = "Free Throws Missed: " + str(list(homeDictionary.values())[x].FT_missed)
			    elif stats == 'FT_attempted':
			    	stat = "Free Throws Attempted: " + str(list(homeDictionary.values())[x].FT_attempted)
			    else:
			    	stat = "No statistic was chosen."

			    html_list.append("<h3 align = 'left'>" + key + "</h3> <p align = 'left'>" + stat +  "</p>")

			html_string = html_string.join(html_list)

			return html_string

		elif games_included == "away":

			num_keys = len(visitingDictionary)
			html_list = []
			html_string = ''

			for x in range(0,num_keys):

			    key = str(list(visitingDictionary.keys())[x])
			        # value = str(list(visitingDictionary.values())[x])
			    if stats == 'points_for':
			    	stat = "Points Scored: " + str(list(visitingDictionary.values())[x].points_for)
			    elif stats == 'shots_missed':
			    	stat = "Shots Missed: " + str(list(visitingDictionary.values())[x].shots_missed)
			    elif stats == 'shot_attempts':
			    	stat = "Shots Attempted: " + str(list(visitingDictionary.values())[x].shot_attempts)
			    elif stats == 'Fouls_by_Team':
			    	stat = "Fouls by Team: " + str(list(visitingDictionary.values())[x].Fouls_by_Team)
			    elif stats == 'assists':
			    	stat = "Assists: " + str(list(visitingDictionary.values())[x].assists)
			    elif stats == 'turnovers':
			    	stat = "Turnovers: " + str(list(visitingDictionary.values())[x].turnovers)
			    elif stats == 'points_against':
			    	stat = "Points Against: " + str(list(visitingDictionary.values())[x].points_against)
			    elif stats == 'Fouls_by_Opponent':
			    	stat = "Fouls by Opponent: " + str(list(visitingDictionary.values())[x].Fouls_by_Opponent)
			    elif stats == 'assists_against':
			    	stat = "Assists Against: " + str(list(visitingDictionary.values())[x].assists_against)
			    elif stats == 'turnovers_forced':
			    	stat = "Turnovers Forced: " + str(list(visitingDictionary.values())[x].turnovers_forced)
			    elif stats == 'FT_missed':
			    	stat = "Free Throws Missed: " + str(list(visitingDictionary.values())[x].FT_missed)
			    elif stats == 'FT_attempted':
			    	stat = "Free Throws Attempted: " + str(list(visitingDictionary.values())[x].FT_attempted)
			    else:
			    	stat = "No statistic was chosen."

			    html_list.append("<h3 align = 'left'>" + key + "</h3> <p align = 'left'>" + stat +  "</p>")

			html_string = html_string.join(html_list)

			return html_string

		elif games_included == "all_games":

			num_keys = len(Dictionary)
			html_list = []
			html_string = ''

			for x in range(0,num_keys):

			    key = str(list(Dictionary.keys())[x])
			        # value = str(list(visitingDictionary.values())[x])
			    if stats == 'points_for':
			    	stat = "Points Scored: " + str(list(Dictionary.values())[x].points_for)
			    elif stats == 'shots_missed':
			    	stat = "Shots Missed: " + str(list(Dictionary.values())[x].shots_missed)
			    elif stats == 'shot_attempts':
			    	stat = "Shots Attempted: " + str(list(Dictionary.values())[x].shot_attempts)
			    elif stats == 'Fouls_by_Team':
			    	stat = "Fouls by Team: " + str(list(Dictionary.values())[x].Fouls_by_Team)
			    elif stats == 'assists':
			    	stat = "Assists: " + str(list(Dictionary.values())[x].assists)
			    elif stats == 'turnovers':
			    	stat = "Turnovers: " + str(list(Dictionary.values())[x].turnovers)
			    elif stats == 'points_against':
			    	stat = "Points Against: " + str(list(Dictionary.values())[x].points_against)
			    elif stats == 'Fouls_by_Opponent':
			    	stat = "Fouls by Opponent: " + str(list(Dictionary.values())[x].Fouls_by_Opponent)
			    elif stats == 'assists_against':
			    	stat = "Assists Against: " + str(list(Dictionary.values())[x].assists_against)
			    elif stats == 'turnovers_forced':
			    	stat = "Turnovers Forced: " + str(list(Dictionary.values())[x].turnovers_forced)
			    elif stats == 'FT_missed':
			    	stat = "Free Throws Missed: " + str(list(Dictionary.values())[x].FT_missed)
			    elif stats == 'FT_attempted':
			    	stat = "Free Throws Attempted: " + str(list(Dictionary.values())[x].FT_attempted)
			    else:
			    	stat = "No statistic was chosen."

			    html_list.append("<h3 align = 'left'>" + key + "</h3> <p align = 'left'>" + stat +  "</p>")

			html_string = html_string.join(html_list)

			return html_string

	        # for f in homeDictionary.keys():
	        #     print(f, homeDictionary[f])
	        #     return(f, homeDictionary[f])

	        # key = str(list(homeDictionary.keys())[0])
	        # value = str(list(homeDictionary.values())[0])
	        # return key + "\n\t" + value


	        # num_keys = len(homeDictionary)

	        # key = str(list(homeDictionary.keys())[0])
	        # value = str(list(homeDictionary.values())[0])
	        # if stats == 'points_for':
	        #     stat = "Points Scored: " + str(list(homeDictionary.values())[0].points_for)
	        # elif stats == 'shots_missed':
	        #     stat = "Shots Missed: " + str(list(homeDictionary.values())[0].shots_missed)
	        # elif stats == 'shots_attempts':
	        #     stat = "Shots Attempted: " + str(list(homeDictionary.values())[0].shots_attempts)
	        # elif stats == 'Fouls_by_Team':
	        #     stat = "Fouls by Team: " + str(list(homeDictionary.values())[0].Fouls_by_Team)
	        # elif stats == 'assists':
	        #     stat = "Assists: " + str(list(homeDictionary.values())[0].assists)
	        # elif stats == 'turnovers':
	        #     stat = "Turnovers: " + str(list(homeDictionary.values())[0].turnovers)
	        # elif stats == 'points_against':
	        #     stat = "Points Against: " + str(list(homeDictionary.values())[0].points_against)
	        # elif stats == 'Fouls_by_Opponent':
	        #     stat = "Fouls by Opponent: " + str(list(homeDictionary.values())[0].Fouls_by_Opponent)
	        # elif stats == 'assists_against':
	        #     stat = "Assists Against: " + str(list(homeDictionary.values())[0].assists_against)
	        # elif stats == 'turnovers_forced':
	        #     stat = "Turnovers Forced: " + str(list(homeDictionary.values())[0].turnovers_forced)
	        # elif stats == 'FT_missed':
	        #     stat = "Free Throws Missed: " + str(list(homeDictionary.values())[0].FT_missed)
	        # elif stats == 'FT_attempted':
	        #     stat = "Free Throws Attempted: " + str(list(homeDictionary.values())[0].FT_attempted)
	        # else:
	        #     stat = "No statistic was chosen."

	        # return key, stat
		# return jsonify(Basketball.main(URL))
		# return Response(stats, mimetype='text/html')


def display_html(html_list):
    html = ""
    html+= """<html> 
	<head>
    <title>Drake Basketball Analysis </title>
	<style>
 
	body{
    	text-align: center;    
	}
	h3{
	    # font-family: 'Amatic SC', cursive;
	    # font-weight: normal;
	    color: #8ac640;
	}
	 
	</style>
	 
	</head>
	<body>
	<div class="block1">
	<h1>Game Statistics for Groups of Players</h1>
	""" + html_list + """
	</div>
	</body>
	</html>"""
    return html


@app.route('/playerstats', methods=['POST']) 
def PlayerStats_form_post():
	text = request.form['gameurl'] 
	text2 = request.form['statistics']
	text3 = request.form['games']
	html_list = PlayerStatistics(text, text2, text3)
	return display_html(html_list)




if __name__ == '__main__':
	app.run(debug=True)