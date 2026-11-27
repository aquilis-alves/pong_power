import random

class GeneralPower:

    @staticmethod
    def speed_ball(ball):
        ball.speed[0]*=2
        ball.speed[1]*=2
        ball.color=(255,255,0)

    @staticmethod
    def small_ball(ball):
        ball.radius-=10

class PlayerPower:

    player_with_debuff=None

    @staticmethod
    def lock_player(player1,player2):

        player=random.choice([player1,player2])
        if player==player1:
            PlayerPower.player_with_debuff=player1
            player1.free=False
        else:
            PlayerPower.player_with_debuff=player2
            player2.free=False

    @staticmethod
    def small_player(player1, player2):

        player=random.choice([player1,player2])
        if player==player1:
            PlayerPower.player_with_debuff=player1
            player1.height-=60
        else:
            PlayerPower.player_with_debuff=player2
            player2.height-=60


    
        





    