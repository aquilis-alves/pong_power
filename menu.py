import pygame
from Config import Config as cg
from Ball import Ball

class Menu:
    """Menu navegável por teclado e mouse.

    Uso no main:
        menu = Menu(screen, clock, titulo="PONG", opcoes=["Jogar", "Sair"])
        escolha = menu.run()   # retorna o texto da opção em minúsculo
    """

    def __init__(self, screen, clock, titulo="PONG", opcoes=("Jogar 5", "Jogar 10", "Jogar Inf", "Sair")):
        self.screen = screen
        self.clock = clock
        self.titulo = titulo
        self.opcoes = list(opcoes)
        self.selecionado = 0
        
        # bolas
        

        # fontes criadas uma única vez
        self.titulo_font = pygame.font.SysFont('consolas', 80, bold=True)
        self.item_font = pygame.font.SysFont('consolas', 40)
        self.dica_font = pygame.font.SysFont('consolas', 20)

        self.largura, self.altura = cg.LARGURA, cg.ALTURA
        self.rects = self._criar_rects()

    def _criar_rects(self):
        rects = []
        for i, texto in enumerate(self.opcoes):
            surf = self.item_font.render(texto, True, cg.BRANCO)
            rects.append(surf.get_rect(
                center=(self.largura // 2, self.altura // 2 + i * 70)))
        return rects

    def _escolhida(self, indice):
        return self.opcoes[indice].lower()

    def _tratar_evento(self, event):
        """Retorna a opção escolhida (str) ou None se nada foi decidido."""
        if event.type == pygame.QUIT:
            return "sair"

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selecionado = (self.selecionado - 1) % len(self.opcoes)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selecionado = (self.selecionado + 1) % len(self.opcoes)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return self._escolhida(self.selecionado)
            elif event.key == pygame.K_ESCAPE:
                return "sair"

        if event.type == pygame.MOUSEMOTION:
            for i, r in enumerate(self.rects):
                if r.collidepoint(event.pos):
                    self.selecionado = i

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, r in enumerate(self.rects):
                if r.collidepoint(event.pos):
                    return self._escolhida(i)

        return None

    def draw(self):
        self.screen.fill(cg.AZUL)

        titulo = self.titulo_font.render(self.titulo, True, cg.BRANCO)
        self.screen.blit(titulo, titulo.get_rect(
            center=(self.largura // 2, self.altura // 4)))

        for i, texto in enumerate(self.opcoes):
            ativo = i == self.selecionado
            cor = cg.AMARELO if ativo else cg.BLACK
            rotulo = f"> {texto} <" if ativo else texto
            surf = self.item_font.render(rotulo, True, cor)
            self.screen.blit(surf, surf.get_rect(center=self.rects[i].center))

        dica = self.dica_font.render(
            "Setas/W/S para mover - Enter para escolher", True, cg.CINZA)
        self.screen.blit(dica, dica.get_rect(
            center=(self.largura // 2, self.altura - 40)))

        pygame.display.flip()

    def run(self):
        """Roda o loop do menu e retorna a opção escolhida."""
        self.selecionado = 0
        while True:
            for event in pygame.event.get():
                resultado = self._tratar_evento(event)
                if resultado is not None:
                    return resultado
            self.draw()
            self.clock.tick(cg.FPS)


# Teste isolado: python menu.py
if __name__ == "__main__":
    pygame.init()
    tela = pygame.display.set_mode(cg.TELA)
    relogio = pygame.time.Clock()

    menu = Menu(tela, relogio)
    print("Opção escolhida:", menu.run())

    pygame.quit()