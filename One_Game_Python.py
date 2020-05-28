# from Team import *
from TeamStats import *
import re

from bs4 import BeautifulSoup
import urllib.request

visiting_team = Team("Drake")
visitingDictionary = {}
# visitingDictionary[visiting_team.get_tuple()] = TeamStats()


def main(game_url):
    data = []
    data2 = []

    soup = BeautifulSoup(urllib.request.urlopen(game_url).read(), 'lxml')



    #Scrapes the stats for the first half of the game
    tbody = soup('table', {"style": "font-family:verdana;color:black;background:white;font-size:xx-small;text-align:right;"})[1].find_all('tr')
    tbody2 = soup('table', {"style": "font-family:verdana;color:black;background:white;font-size:xx-small;text-align:right;"})[3].find_all('tr')
    #tbody = soup('table')[7].find_all('tr')

    for col in tbody:
        rows = col.findChildren(recursive = False)
        rows = [ele.text.strip() for ele in rows]
        data.append(rows)


    #tbody2 = soup('table')[9].find_all('tr')

    for col in tbody2:
        rows2 = col.findChildren(recursive = False)
        rows2 = [ele.text.strip() for ele in rows2]
        data2.append(rows2)




    headers = data[0]
    # print(data)
    # print(data2)



    for x in headers:
        visitors_match = re.search("VISITORS: Drake", x)
        home_match = re.search("HOME TEAM: Drake", x)
        if visitors_match or home_match:
            break

    # if home_match:
    #     continue


    if visitors_match:
        visiting_team = Team("Drake")

        players = []

        #tbody3 = soup('table')[2].find_all('tr', {"bgcolor": "#ffffff"})
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
    # elif headers[0] == "HOME TEAM: Drake":

    elif home_match:
        home_team = Team("Drake")


        players = []

        #tbody4 = soup('table', {"border": "0", "cellspacing": "0", "cellpadding": "2"})[1].find_all('tr', {"bgcolor": "#ffffff"})
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
                if (subin not in visiting_team.roster) and (subin not in visiting_team.get_tuple()):
                    visiting_team.add_to_roster(PlayerStats(subin))
                visiting_team.sub_in(subin)

            # exited game
            match = re.search(r'SUB OUT: (.*)', str(visitors))
            if match:
                subout = match.group(1)
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

            # 3 Pointer
            match = re.search(r'TURNOVR by (.*)', str(visitors))
            if match:
                player = match.group(1)
                visiting5tuple = visiting_team.get_tuple()
                if player not in visiting5tuple:
                    visiting_team.sub_in(player)
                    visiting5tuple = visiting_team.get_tuple()
                if not (visiting5tuple in visitingDictionary):
                    visitingDictionary[visiting5tuple] = TeamStats()
                visitingDictionary[visiting5tuple].turnover += 1


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

            # print(row)

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
                if (subin not in visiting_team.roster) and (subin not in visiting_team.get_tuple()):
                    visiting_team.add_to_roster(PlayerStats(subin))
                visiting_team.sub_in(subin)

            # exited game
            match = re.search(r'SUB OUT: (.*)', str(visitors))
            if match:
                subout = match.group(1)
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



    for f in visitingDictionary.keys():
        print(f, visitingDictionary[f])



#main("https://static.godrakebulldogs.com/custompages/Statistics/mbb-19-20/du14.htm")
main("https://static.godrakebulldogs.com/custompages/Statistics/mbb-17-18/du-02.htm")