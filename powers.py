import random

class GeneralPower:
    @staticmethod
    def speed_ball(ball):
        ball.speed[0] *= 2
        ball.speed[1] *= 2
        ball.color = (255,255,0)

    @staticmethod
    def small_ball(ball):
        ball.radius -= 10

    @staticmethod
    def many_balls():
        return random.choice([2,3,4])

class PlayerPower:

    players_with_lock_debuff=[]
    players_small_debuff=[]

    @staticmethod
    def lock_player(player1,player2):
        player=random.choice([player1,player2])
        if player not in PlayerPower.players_with_lock_debuff:
            PlayerPower.players_with_lock_debuff.append(player)
            player.free=False

    
    @staticmethod
    def small_player(player1, player2):
        player=random.choice([player1,player2])
        if player not in PlayerPower.players_small_debuff:
            PlayerPower.players_small_debuff.append(player)
            player.height-=60
       


    
        





    