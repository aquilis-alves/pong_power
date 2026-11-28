class Config:
    # Tela
    LARGURA = 1280
    ALTURA = 720
    TELA = (LARGURA, ALTURA)
    FPS = 120
    COR_FUNDO = "black"

    # Bola
    BOLA_TAMANHO = 30
    BOLA_POS_INICIAL = (LARGURA // 2, ALTURA // 2)

    # Jogadores
    JOGADOR_TAMANHO = 100
    MARGEM_JOGADOR = 50        
    JOGADOR1_POS = (MARGEM_JOGADOR, ALTURA // 2)
    JOGADOR2_POS = (LARGURA - MARGEM_JOGADOR, ALTURA // 2)
    
    # cores
    BRANCO = (255, 255, 255)
    CINZA = (120, 120, 120)
    AMARELO = (255, 255, 0)
    AZUL=(0,50,210)
    BLACK=(0,0,0)