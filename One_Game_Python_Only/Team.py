from PlayerStats import *

class Team:

    def __init__(self, name):
        self.name = name
        self.roster = []
        self.group_of_five = []

    def add_to_roster(self, player):
        self.roster.append(player)

    def sub_in(self, player_name):
        player_list = [x for x in self.roster if x.name == player_name]
        self.group_of_five.append(player_list[0])

    def sub_out(self, player_name):
        player_list = [x for x in self.roster if x.name == player_name]
        self.group_of_five.remove(player_list[0])


    def get_tuple(self):
        list_of_names = []
        for player in self.group_of_five:
            list_of_names.append(player.name)
        list_of_names.sort()
        return tuple(list_of_names)


    def get_player(self, player_name):
        player_list = [x for x in self.roster if x.name == player_name]
        return player_list[0]

    def __str__(self):
        output_string = self.name + "\n"
        for p in self.group_of_five:
            output_string += ("\t" + p.name + "\n")

        return output_string