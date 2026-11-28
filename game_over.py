import pygame
from Config import Config as cg

class Game_over:
    
    def __init__(self, screen, clock, winner):
        self.screen = screen
        self.clock = clock
        self.winner = winner
        
        # fontes criadas uma única vez
        self.titulo_font = pygame.font.SysFont('consolas', 80, bold=True)
        self.item_font = pygame.font.SysFont('consolas', 40)
        self.dica_font = pygame.font.SysFont('consolas', 20)

        self.largura, self.altura = cg.LARGURA, cg.ALTURA
    
    
    def draw(self):
        self.screen.fill(cg.BLACK)
        
        text = self.titulo_font.render(f"{self.winner} Ganhou!!!", True, cg.BRANCO)
        self.screen.blit(text, text.get_rect(
            center = (self.largura // 2, self.altura // 2)
        ))
        
        dica = self.dica_font.render("ESC ou Espaço para voltar", True, cg.CINZA)
        self.screen.blit(dica, dica.get_rect(
            center=(self.largura // 2, self.altura - 40)
        ))
        
        pygame.display.flip()
        
    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                quit = pygame.key.get_pressed()
                if quit[pygame.K_ESCAPE] or quit[pygame.K_SPACE]or event.type == pygame.QUIT:
                    running = False
                    
            self.draw()
            self.clock.tick(cg.FPS)
            
if __name__ == "__main__":
    pygame.init()
    tela = pygame.display.set_mode(cg.TELA)
    clock = pygame.time.Clock()
    
    game_over = Game_over(tela, clock, "aquilis")
    game_over.run()
    
    pygame.quit()