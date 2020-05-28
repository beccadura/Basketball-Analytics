from Team import *

class TeamStats:

    def __init__(self):
        self.points_for = 0
        self.points_against = 0
        self.fouls = 0
        self.minutes_played = 0
        self.rebounds = 0
        self.shots_missed = 0
        self.shot_attempts = 0
        self.FT_missed = 0
        self.FT_attempted = 0
        self.turnover = 0

    def __str__(self):
        return "Team Stats:" + \
               "\n\tPoints For: " + str(self.points_for) + \
               "\n\tPoints Against: " + str(self.points_against) + \
               "\n\tShots Missed: " + str(self.shots_missed) + \
               "\n\tShot Attempts: " + str(self.shot_attempts)

               # "\n\tShooting Percentage: " + str((self.shot_attempts - self.shots_missed) / self.shot_attempts)