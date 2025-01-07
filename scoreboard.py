from Meteor import *

class scoreboard():
    def __init__(self,player2):
        self.player2 = player2
        self.player1_score = 0 
        self.player2_score = 0
        self.highscore = int(self.readfile_player())
    def update(self):
        if self.player2:
            self.player2_score += 1
        else:
            self.player1_score += 1

    


    def readfile_player(self):
        self.file = open("scores.txt", "r") 
        return self.file.read()

    def updatefile(self):
        if self.player2:
            self.CheckScorep2()
        else:
            self.CheckScorep1()
       
        return self.highscore
    def CheckScorep1(self):
        if not self.player2:
            if self.highscore < self.player1_score:
                self.highscore = self.player1_score
                file =  open ("scores.txt", "w")        
                file.write(str(self.highscore))
                file.close()
    def CheckScorep2(self):
            if self.player1_score > self.player2_score:
                if self.player1_score> self.highscore:
                    self.highscore = self.player1_score
                    file =  open ("scores.txt", "w") 
                    file.write(str(self.highscore))
                    file.close()
                
            else:
                if self.player2_score > self.highscore:
                    self.highscore = self.player2_score
                    file =  open ("scores.txt", "w") 
                    file.write(str(self.highscore))
                    file.close()
        
    

player1_scores = scoreboard(None)
player2_scores = scoreboard(True)