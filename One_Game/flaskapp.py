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
	return render_template('game.html', fieldname = "statistic")

@app.route("/playerstats/<URL>")
def PlayerStatistics(stats):

    visitingDictionary = {}
    homeDictionary = {}

    #Away Game
    game = "https://static.godrakebulldogs.com/custompages/Statistics/mbb-17-18/du-02.htm"
    #Home Game
    #game = "https://static.godrakebulldogs.com/custompages/Statistics/mbb-17-18/du-05.htm"
    data = []
    data2 = []

    soup = BeautifulSoup(urllib.request.urlopen(game).read(), features = "lxml")

    tbody = soup('table', {"style":"font-family:verdana;color:black;background:white;font-size:xx-small;text-align:right;"})[1].find_all('tr')
    tbody2 = soup('table', {"style":"font-family:verdana;color:black;background:white;font-size:xx-small;text-align:right;"})[3].find_all('tr')



	#Scrapes the stats for the first half of the game
    for col in tbody:
        rows = col.findChildren(recursive = False)
        rows = [ele.text.strip() for ele in rows]
        data.append(rows)


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





    if visitors_match:
        visiting_team = Team("Drake")

        players = []

        tbody3 = soup('table', {"border": "0", "cellspacing": "0", "cellpadding": "2"})[0].find_all('tr', {"bgcolor": "#ffffff"})

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



    #####AUTOMATED#####

    elif home_match:
        home_team = Team("Drake")


        players = []

        tbody4 = soup('table', {"border": "0", "cellspacing": "0", "cellpadding": "2"})[1].find_all('tr', {"bgcolor": "#ffffff"})


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



    #####AUTOMATED#####
    if visitors_match:
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





    ####AUTOMATED#####
    elif home_match:
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




    if home_match:

	    num_keys = len(homeDictionary)
	    html_list = []
	    maximum = 0

	    for x in range(0,num_keys):

	        if stats == 'points_for':
		        current = list(homeDictionary.values())[x].points_for
		        if current > maximum:
		        	maximum = current
		        	key = str(list(homeDictionary.keys())[x])
		        	stat = "Points Scored: " + str(current)
	        elif stats == 'shots_missed':
		        current = list(homeDictionary.values())[x].shots_missed
		        if current > maximum:
		        	maximum = current
		        	key = str(list(homeDictionary.keys())[x])
		        	stat = "Shots Missed: " + str(current)
	        elif stats == 'shot_attempts':
		        current = list(homeDictionary.values())[x].shot_attempts
		        if current > maximum:
		        	maximum = current
		        	key = str(list(homeDictionary.keys())[x])
		        	stat = "Shots Attempted: " + str(current)
	        elif stats == 'Fouls_by_Team':
		        current = list(homeDictionary.values())[x].Fouls_by_Team
		        if current > maximum:
		        	maximum = current
		        	key = str(list(homeDictionary.keys())[x])
		        	stat = "Fouls by Team: " + str(current)
	        elif stats == 'assists':
		        current = list(homeDictionary.values())[x].assists
		        if current > maximum:
		        	maximum = current
		        	key = str(list(homeDictionary.keys())[x])
		        	stat = "Assists: " + str(current)
	        elif stats == 'turnovers':
		        current = list(homeDictionary.values())[x].turnovers
		        if current > maximum:
		        	maximum = current
		        	key = str(list(homeDictionary.keys())[x])
		        	stat = "Turnovers: " + str(current)
	        elif stats == 'points_against':
		        current = list(homeDictionary.values())[x].points_against
		        if current > maximum:
		        	maximum = current
		        	key = str(list(homeDictionary.keys())[x])
		        	stat = "Points Against: " + str(current)
	        elif stats == 'Fouls_by_Opponent':
		        current = list(homeDictionary.values())[x].Fouls_by_Opponent
		        if current > maximum:
		        	maximum = current
		        	key = str(list(homeDictionary.keys())[x])
		        	stat = "Fouls by Opponent: " + str(current)
	        elif stats == 'assists_against':
		        current = list(homeDictionary.values())[x].assists_against
		        if current > maximum:
		        	maximum = current
		        	key = str(list(homeDictionary.keys())[x])
		        	stat = "Assists Against: " + str(current)
	        elif stats == 'turnovers_forced':
		        current = list(homeDictionary.values())[x].turnovers_forced
		        if current > maximum:
		        	maximum = current
		        	key = str(list(homeDictionary.keys())[x])
		        	stat = "Turnovers Forces: " + str(current)
	        elif stats == 'FT_missed':
		        current = list(homeDictionary.values())[x].FT_missed
		        if current > maximum:
		        	maximum = current
		        	key = str(list(homeDictionary.keys())[x])
		        	stat = "Free Throws Missed: " + str(current)
	        elif stats == 'FT_attempted':
		        current = list(homeDictionary.values())[x].FT_attempted
		        if current > maximum:
		        	maximum = current
		        	key = str(list(homeDictionary.keys())[x])
		        	stat = "Free Throws Attempted: " + str(current)
	        else:
		        key=" "
		        stat = "No statistic was chosen."



	    html_string = ("<h3 align = 'left'>" + key + "</h3> <p align = 'left'>" + stat +  "</p>")



	    return html_string

    elif visitors_match:

	    num_keys = len(visitingDictionary)
	    html_list = []
	    maximum = 0

	    for x in range(0,num_keys):

	        if stats == 'points_for':
		        current = list(visitingDictionary.values())[x].points_for
		        if current > maximum:
		        	maximum = current
		        	key = str(list(visitingDictionary.keys())[x])
		        	stat = "Points Scored: " + str(current)
	        elif stats == 'shots_missed':
		        current = list(visitingDictionary.values())[x].shots_missed
		        if current > maximum:
		        	maximum = current
		        	key = str(list(visitingDictionary.keys())[x])
		        	stat = "Shots Missed: " + str(current)
	        elif stats == 'shot_attempts':
		        current = list(visitingDictionary.values())[x].shot_attempts
		        if current > maximum:
		        	maximum = current
		        	key = str(list(visitingDictionary.keys())[x])
		        	stat = "Shots Attempted: " + str(current)
	        elif stats == 'Fouls_by_Team':
		        current = list(visitingDictionary.values())[x].Fouls_by_Team
		        if current > maximum:
		        	maximum = current
		        	key = str(list(visitingDictionary.keys())[x])
		        	stat = "Fouls by Team: " + str(current)
	        elif stats == 'assists':
		        current = list(visitingDictionary.values())[x].assists
		        if current > maximum:
		        	maximum = current
		        	key = str(list(visitingDictionary.keys())[x])
		        	stat = "Assists: " + str(current)
	        elif stats == 'turnovers':
		        current = list(visitingDictionary.values())[x].turnovers
		        if current > maximum:
		        	maximum = current
		        	key = str(list(visitingDictionary.keys())[x])
		        	stat = "Turnovers: " + str(current)
	        elif stats == 'points_against':
		        current = list(visitingDictionary.values())[x].points_against
		        if current > maximum:
		        	maximum = current
		        	key = str(list(visitingDictionary.keys())[x])
		        	stat = "Points Against: " + str(current)
	        elif stats == 'Fouls_by_Opponent':
		        current = list(visitingDictionary.values())[x].Fouls_by_Opponent
		        if current > maximum:
		        	maximum = current
		        	key = str(list(visitingDictionary.keys())[x])
		        	stat = "Fouls by Opponent: " + str(current)
	        elif stats == 'assists_against':
		        current = list(visitingDictionary.values())[x].assists_against
		        if current > maximum:
		        	maximum = current
		        	key = str(list(visitingDictionary.keys())[x])
		        	stat = "Assists Against: " + str(current)
	        elif stats == 'turnovers_forced':
		        current = list(visitingDictionary.values())[x].turnovers_forced
		        if current > maximum:
		        	maximum = current
		        	key = str(list(visitingDictionary.keys())[x])
		        	stat = "Turnovers Forces: " + str(current)
	        elif stats == 'FT_missed':
		        current = list(visitingDictionary.values())[x].FT_missed
		        if current > maximum:
		        	maximum = current
		        	key = str(list(visitingDictionary.keys())[x])
		        	stat = "Free Throws Missed: " + str(current)
	        elif stats == 'FT_attempted':
		        current = list(visitingDictionary.values())[x].FT_attempted
		        if current > maximum:
		        	maximum = current
		        	key = str(list(visitingDictionary.keys())[x])
		        	stat = "Free Throws Attempted: " + str(current)
	        else:
		        key=" "
		        stat = "No statistic was chosen."



	    html_string = ("<h3 align = 'left'>" + key + "</h3> <p align = 'left'>" + stat +  "</p>")



	    return html_string

		




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
	text = request.form['statistics']
	html_list = PlayerStatistics(text)
	return display_html(html_list)




if __name__ == '__main__':
	app.run(debug=True)