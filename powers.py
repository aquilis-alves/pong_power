import random

class GeneralPower:

    @staticmethod
    def speed_ball(ball):
        ball.speed[0]*=1.001
        ball.speed[1]*=1.001

    @staticmethod
    def clear_powers(self):
        pass

class PlayerPower:

    @staticmethod
    def free_player(player1, player2):
        player=random.choice([player1, player2])
        player.free=True


    
        





    