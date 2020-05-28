from Team import *

class TeamStats:

    def __init__(self):
        self.points_for = 0
        self.points_against = 0
        self.Fouls_by_Team = 0
        self.Fouls_by_Opponent = 0
        self.assists = 0
        self.turnovers = 0
        self. assists_against = 0
        self.turnovers_forced = 0
        self.shots_missed = 0
        self.shot_attempts = 0
        self.FT_missed = 0
        self.FT_attempted = 0

    # def __str__(self):
    #     return "Team Stats:" + \
    #            "\n\tPoints For: " + str(self.points_for) + \
    #            "\n\tPoints Against: " + str(self.points_against) + \
    #            "\n\tFouls committed: " + str(self.Fouls_by_Team) + \
    #            "\n\tFouls by Opponent: " + str(self.Fouls_by_Opponent) + \
    #            "\n\tAssists: " + str(self.assists) + \
    #            "\n\tTurnovers: " + str(self.turnovers) + \
    #            "\n\tAssists_against: " + str(self.assists_against) + \
    #            "\n\tTurnovers forced: " + str(self.turnovers_forced) + \
    #            "\n\tShots Missed: " + str(self.shots_missed) + \
    #            "\n\tShot Attempts: " + str(self.shot_attempts) + \
    #            "\n\tFT Percentage: " + str((self.FT_attempted - self.FT_missed) / self.FT_attempted) + \
    #            "\n\tShooting Percentage: " + str((self.shot_attempts - self.shots_missed) / self.shot_attempts)