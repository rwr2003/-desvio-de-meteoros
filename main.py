import pygame
import sys
import random

# 1. Inicializa o Pygame e configura a janela
pygame.init()
LARGURA, ALTURA = 700, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Desvio de Meteoros")
relogio = pygame.time.Clock()

# Configurações do jogador, obstáculos e recorde
nave = pygame.Rect(325, 520, 50, 50)
velocidade_nave = 7
meteoros = []
velocidade_meteoro = 6
pontos = 0
recorde = 0

# Fundo estrelado (30 estrelas em posições aleatórias)
estrelas = [[random.randint(0, LARGURA), random.randint(0, ALTURA)] for _ in range(30)]

# Configurações da explosão
particulas = []
tempo_explosao = 0

# Fontes e Estado inicial
fonte = pygame.font.SysFont(None, 36)
fonte_titulo = pygame.font.SysFont(None, 64)
estado = "INICIAR"

def criar_explosao(x, y):
    particulas.clear()
    cores = [(255, 200, 0), (255, 100, 0), (255, 50, 50), (0, 200, 255)]
    for _ in range(40):
        particula = {
            "x": x,
            "y": y,
            "vx": random.uniform(-6, 6),
            "vy": random.uniform(-6, 6),
            "tamanho": random.randint(5, 11),
            "cor": random.choice(cores)
        }
        particulas.append(particula)

# 2. Loop principal do jogo (Game Loop)
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if (evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE) or evento.type == pygame.MOUSEBUTTONDOWN:
            if estado == "INICIAR":
                estado = "JOGANDO"
            elif estado == "FIM":
                pontos = 0
                velocidade_meteoro = 6
                meteoros.clear()
                particulas.clear()
                nave.x = 325
                estado = "JOGANDO"

    tela.fill((15, 15, 25))

    # Atualiza e desenha as estrelas no fundo
    for estrela in estrelas:
        estrela[1] += 2
        if estrela[1] > ALTURA:
            estrela[1] = 0
            estrela[0] = random.randint(0, LARGURA)
        pygame.draw.circle(tela, (100, 100, 130), (estrela[0], estrela[1]), 2)

    # --- TELA 1: INICIAR ---
    if estado == "INICIAR":
        titulo = fonte_titulo.render("DESVIO DE METEOROS", True, (0, 200, 255))
        instrucao = fonte.render("Pressione ESPACO ou TOQUE para iniciar", True, (255, 255, 255))
        controles = fonte.render("PC: Setas | Celular: Toque nos lados da tela", True, (180, 180, 200))

        tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 200))
        tela.blit(instrucao, (LARGURA // 2 - instrucao.get_width() // 2, 300))
        tela.blit(controles, (LARGURA // 2 - controles.get_width() // 2, 360))

    # --- TELA 2: JOGANDO ---
    elif estado == "JOGANDO":
        teclas = pygame.key.get_pressed()
        toque_ativo = pygame.mouse.get_pressed()[0]
        pos_toque_x = pygame.mouse.get_pos()[0]

        if (teclas[pygame.K_LEFT] or (toque_ativo and pos_toque_x < LARGURA // 2)) and nave.left > 0:
            nave.x -= velocidade_nave
        if (teclas[pygame.K_RIGHT] or (toque_ativo and pos_toque_x >= LARGURA // 2)) and nave.right < LARGURA:
            nave.x += velocidade_nave

        velocidade_atual = velocidade_meteoro + (pontos // 10)
        chance_spawn = max(25, 70 - (pontos // 5) * 3)

        if random.randint(1, chance_spawn) == 1:
            pos_x = random.randint(0, LARGURA - 40)
            novo_meteoro = pygame.Rect(pos_x, -40, 40, 40)
            meteoros.append(novo_meteoro)

        for meteoro in meteoros[:]:
            meteoro.y += velocidade_atual
            if meteoro.top > ALTURA:
                meteoros.remove(meteoro)
                pontos += 1
                if pontos > recorde:
                    recorde = pontos

            if nave.colliderect(meteoro):
                criar_explosao(nave.centerx, nave.centery)
                tempo_explosao = 60
                estado = "EXPLODINDO"

        # Desenha o Jogador (Azul) + Carinha do Bem
        pygame.draw.rect(tela, (0, 200, 255), nave, border_radius=8)
        pygame.draw.circle(tela, (15, 15, 25), (nave.x + 15, nave.y + 18), 4)
        pygame.draw.circle(tela, (15, 15, 25), (nave.x + 35, nave.y + 18), 4)
        boca_bem = pygame.Rect(nave.x + 13, nave.y + 22, 24, 16)
        pygame.draw.arc(tela, (15, 15, 25), boca_bem, 3.14, 6.28, 3)

        # Desenha os Meteoros (Vermelhos) + Carinha do Mal
        for meteoro in meteoros:
            pygame.draw.rect(tela, (255, 70, 70), meteoro, border_radius=6)
            pygame.draw.circle(tela, (255, 255, 255), (meteoro.x + 12, meteoro.y + 16), 3)
            pygame.draw.circle(tela, (255, 255, 255), (meteoro.x + 28, meteoro.y + 16), 3)
            pygame.draw.line(tela, (15, 15, 25), (meteoro.x + 7, meteoro.y + 9), (meteoro.x + 16, meteoro.y + 13), 3)
            pygame.draw.line(tela, (15, 15, 25), (meteoro.x + 33, meteoro.y + 9), (meteoro.x + 24, meteoro.y + 13), 3)
            boca_mal = pygame.Rect(meteoro.x + 10, meteoro.y + 24, 20, 12)
            pygame.draw.arc(tela, (15, 15, 25), boca_mal, 0, 3.14, 3)

        texto_pontos = fonte.render(f"Pontos: {pontos}  |  Recorde: {recorde}", True, (255, 255, 255))
        tela.blit(texto_pontos, (15, 15))

    # --- TELA 2.5: EXPLODINDO ---
    elif estado == "EXPLODINDO":
        for meteoro in meteoros:
            pygame.draw.rect(tela, (255, 70, 70), meteoro, border_radius=6)

        for p in particulas:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["tamanho"] = max(0, p["tamanho"] - 0.15)
            if p["tamanho"] > 0:
                pygame.draw.circle(tela, p["cor"], (int(p["x"]), int(p["y"])), int(p["tamanho"]))

        texto_pontos = fonte.render(f"Pontos: {pontos}  |  Recorde: {recorde}", True, (255, 255, 255))
        tela.blit(texto_pontos, (15, 15))

        tempo_explosao -= 1
        if tempo_explosao <= 0:
            estado = "FIM"

    # --- TELA 3: FIM DE JOGO ---
    elif estado == "FIM":
        fim = fonte_titulo.render("FIM DE JOGO", True, (255, 70, 70))
        placar_final = fonte.render(f"Pontuacao: {pontos}   |   Recorde: {recorde}", True, (255, 255, 255))
        reiniciar = fonte.render("Pressione ESPACO ou TOQUE para jogar de novo", True, (0, 200, 255))

        tela.blit(fim, (LARGURA // 2 - fim.get_width() // 2, 200))
        tela.blit(placar_final, (LARGURA // 2 - placar_final.get_width() // 2, 290))
        tela.blit(reiniciar, (LARGURA // 2 - reiniciar.get_width() // 2, 360))

    pygame.display.flip()
    relogio.tick(60)
