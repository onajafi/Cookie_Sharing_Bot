# -*- coding: utf-8 -*-

import emoji

class Duel:
    """A Class to control the process of Duels"""

    FirstPoint=0
    SecondPoint=0
    target=3

    F_temp_Move=0
    S_temp_Move=0
    ready_to_move=False

    def __init__(self,FirstUsrId,SecondUsrId,Amnt,FirstName,SecondName):
        self.F_Id=FirstUsrId
        self.S_Id=SecondUsrId
        self.Amnt=Amnt
        self.F_name=FirstName
        self.S_name=SecondName

    def solo_move(self,UsrId,Move):
        if(self.F_Id==UsrId):
            self.F_temp_Move = Move
        elif(self.S_Id==UsrId):
            self.S_temp_Move = Move

        if(self.F_temp_Move != 0 and self.S_temp_Move != 0):
            self.ready_to_move=True

    def compute_solo_moves(self):
        return self.PointUpdater(self.F_temp_Move,self.S_temp_Move)

    def move(self,FirstMove,SecondMove):
        "gets the move in a range of 1 to 3 and tells the winner by 1 or 2"

        self.F_temp_Move = 0
        self.S_temp_Move = 0
        self.ready_to_move = False

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

        M_MSG= self.F_name + " Gave a "
        if(FirstMove==1):
            M_MSG = M_MSG + emoji.emojize(
                emoji.demojize(u'🍪') + 'Banana Cookie' + emoji.demojize(u'🍌'))
        elif (FirstMove == 2):
            M_MSG = M_MSG + emoji.emojize(
                emoji.demojize(u'🍪') + 'Chocolate Chip Cookie' + emoji.demojize(u'🍫'))
        elif (FirstMove == 3):
            M_MSG = M_MSG + emoji.emojize(
                emoji.demojize(u'🍪') + 'Vanilla Ice-Cream Cookie' + emoji.demojize(u'🍦'))

        M_MSG = M_MSG + "\n" + self.S_name + " Gave a "

        if (SecondMove == 1):
            M_MSG = M_MSG + emoji.emojize(
                emoji.demojize(u'🍪') + 'Banana Cookie' + emoji.demojize(u'🍌'))
        elif (SecondMove == 2):
            M_MSG = M_MSG + emoji.emojize(
                emoji.demojize(u'🍪') + 'Chocolate Chip Cookie' + emoji.demojize(u'🍫'))
        elif (SecondMove == 3):
            M_MSG = M_MSG + emoji.emojize(
                emoji.demojize(u'🍪') + 'Vanilla Ice-Cream Cookie' + emoji.demojize(u'🍦'))

        M_MSG = M_MSG + "\n\nSo far,\n"

        result=self.move(FirstMove,SecondMove)
        if(result==1):
            self.FirstPoint += 1
            if(self.FirstPoint < self.target):
                return M_MSG + self.F_name + " " + str(self.FirstPoint) + "-" + str(self.SecondPoint) + " " + self.S_name
            else:
                return M_MSG + self.F_name + " " + str(self.FirstPoint) + "-" + str(self.SecondPoint) + " " + self.S_name \
                        + "\nand the winner is " + self.F_name

        elif(result==2):
            self.SecondPoint += 1
            if (self.SecondPoint < self.target):
                return M_MSG + self.F_name + " " + str(self.FirstPoint) + "-" + str(self.SecondPoint) + " " + self.S_name
            else:
                return M_MSG + self.F_name + " " + str(self.FirstPoint) + "-" + str(self.SecondPoint) + " " + self.S_name \
                       + "\nand the winner is " + self.S_name

        return result

    def winner(self):
        if(self.FirstPoint >= self.target):
            return (self.F_Id,self.F_name)
        elif(self.SecondPoint >= self.target):
            return (self.S_Id,self.S_name)
        return None

    def looser(self):
        if (self.FirstPoint >= self.target):
            return (self.S_Id, self.S_name)
        elif (self.SecondPoint >= self.target):
            return (self.F_Id,self.F_name)
        return None

    def Ready_to_move(self):
        return self.ready_to_move
