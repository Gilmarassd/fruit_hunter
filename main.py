import pygame, random, os

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("assets/mondamusic-retro-arcade-game-music-512837.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)  # Toca em loop

LARGURA, ALTURA = 960, 540
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("FRUIT HUNTER")

fonte = pygame.font.SysFont(None, 36)
fonte_titulo = pygame.font.SysFont(None, 72)

relogio = pygame.time.Clock()

player_img = pygame.image.load("assets/LPA (5).png").convert_alpha()
player_img = pygame.transform.scale(player_img, (96, 96))

background = pygame.image.load("assets/background (6).png").convert()
background = pygame.transform.scale(background, (LARGURA, ALTURA))

frutas = [
    "assets/fruits (1).png",
    "assets/fruits (10).png",
    "assets/fruits (13).png",
    "assets/fruits (4).png",
    "assets/fruits (5).png"
]


def nova_fruta():
    arq = random.choice(frutas)
    img = pygame.image.load(arq).convert_alpha()
    img = pygame.transform.scale(img, (48, 48))
    return img, random.randint(50, 900), random.randint(80, 480)


estado = "menu"
meta = 15

while True:

    if estado == "jogo":
        try:
            tempo = 45 - ((pygame.time.get_ticks() - inicio) // 1000)
        except:
            tempo = 45

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if e.type == pygame.KEYDOWN:

            if estado == "menu" and e.key == pygame.K_RETURN:
                px, py = 100, 250
                pontos = 0
                fruta_img, fx, fy = nova_fruta()
                inicio = pygame.time.get_ticks()
                estado = "jogo"

            elif estado in ["vitoria", "derrota"] and e.key == pygame.K_RETURN:
                estado = "menu"

    tela.blit(background, (0, 0))

    if estado == "menu":
        tela.blit(fonte_titulo.render("FRUIT HUNTER", True, (255, 255, 255)), (250, 120))
        controles = [
            "W A S D - Movimentar",
            "ENTER - Iniciar",
            "Colete 15 frutas em 45 segundos"
        ]
        y = 250
        for t in controles:
            tela.blit(fonte.render(t, True, (255, 255, 255)), (300, y))
            y += 50


    elif estado == "jogo":

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_w]: py -= 5
        if teclas[pygame.K_s]: py += 5
        if teclas[pygame.K_a]: px -= 5
        if teclas[pygame.K_d]: px += 5

        player_rect = pygame.Rect(px, py, 60, 60)
        fruta_rect = pygame.Rect(fx, fy, 48, 48)

        tela.blit(player_img, (px, py))
        tela.blit(fruta_img, (fx, fy))

        if player_rect.colliderect(fruta_rect):
            pontos += 1
            fruta_img, fx, fy = nova_fruta()

        tempo = 45 - ((pygame.time.get_ticks() - inicio) // 1000)

        tela.blit(fonte.render(f"Frutas: {pontos}/{meta}", True, (255, 255, 255)), (10, 10))
        tela.blit(fonte.render(f"Tempo: {tempo}", True, (255, 255, 255)), (800, 10))

        if pontos >= meta:
            estado = "vitoria"

        if tempo <= 0:
            estado = "derrota"

    elif estado == "vitoria":
        tela.blit(fonte_titulo.render("VOCE VENCEU!", True, (255, 255, 255)), (220, 200))
        tela.blit(fonte.render("ENTER - Voltar ao menu", True, (255, 255, 255)), (330, 300))

    elif estado == "derrota":
        tela.blit(fonte_titulo.render("TEMPO ESGOTADO!", True, (255, 255, 255)), (170, 200))
        tela.blit(fonte.render("ENTER - Voltar ao menu", True, (255, 255, 255)), (330, 300))

    pygame.display.flip()
    relogio.tick(45)
