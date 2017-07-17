

class Duel:
    """A Class to control the process of Duels"""

    FirstPoint=0
    SecondPoint=0
    target=3

    def __init__(self,FirstUsrId,SecondUsrId,Amnt):
        self.F_Id=FirstUsrId
        self.S_Id=SecondUsrId
        self.Amnt=Amnt

    def move(self,FirstMove,SecondMove):
        "gets the move in a range of 1 to 3 and tells the winner by 1 or 2"

        if(FirstMove==SecondMove):
            return 0
        elif(FirstMove==1):# 1 wins 2, 2 wins 3, 3 wins 1
            if(SecondMove==2):
                return 1#First Player is the winner
            elif(SecondMove==3):
                return 2#Second Player is the winner
        elif (FirstMove == 2):
            if (SecondMove == 1):
                return 2
            elif (SecondMove == 3):
                return 1
        elif (FirstMove == 3):
            if (SecondMove == 1):
                return 1
            elif (SecondMove == 2):
                return 2

    def PointUpdater(self,FirstMove,SecondMove):

        result=self.move(FirstMove,SecondMove)
        if(result==1):
            self.FirstPoint += 1
            if(self.FirstPoint < self.target):
                return 1
            else:
                return 3
        elif(result==2):
            self.SecondPoint += 1
            if (self.SecondPoint < self.target):
                return 2
            else:
                return 4
        return result
