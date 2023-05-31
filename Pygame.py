import pygame as pg
import time
import random

class Personagem(pg.sprite.Sprite):
    personagem1 = pg.image.load('personagem1.png')
    personagem2 = pg.image.load('personagem2.png')

    def __init__(self):
        super().__init__()
        self.x = 50
        self.y = ALTURA/2
        self.vel = 4
        self.largura = 100
        self.altura = 50
        self.vidas = 3

        self.image = self.personagem1
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)

    def update(self):
        self.rect.center = (self.x, self.y)

    def movimento(self, keys):
        # Movimento horizontal
        if keys[pg.K_LEFT]:
            self.x -= self.vel
            self.image = self.personagem2
        elif keys[pg.K_RIGHT]:
            self.x += self.vel
            self.image = self.personagem1

        # Movimento vertical
        if keys[pg.K_UP]:
            self.y -= self.vel
        elif keys[pg.K_DOWN]:
            self.y += self.vel

        # Verificar se o personagem saiu da tela e reposicionar do lado oposto
        if self.x < 0:
            self.x = LARGURA
        elif self.x > LARGURA:
            self.x = 0
        if self.y < 0:
            self.y = ALTURA
        elif self.y > ALTURA:
            self.y = 0

    def reset_pos(self):
        self.x = 50
        self.y = ALTURA / 2

    def perde_vida(self):
        self.vidas -= 1
        if self.vidas >= 0:
            self.reset_pos()
        return self.vidas


class Carro(pg.sprite.Sprite):
    carro_vermelho = pg.image.load('carro_vermelho.png')
    carro_azul = pg.image.load('carro_azul.png')

    def __init__(self, numero):
        super().__init__()
        if numero == 1:
            self.x = 190
            self.image = self.carro_vermelho
            self.vel = -1 * random.randint(1, 6)
        else:
            self.x = 460
            self.image = self.carro_azul
            self.vel = random.randint(4, 9)

        self.y = ALTURA / 2
        self.largura = 100
        self.altura = 150
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.mask = pg.mask.from_surface(self.image)

    def update(self):
        self.movimento()
        self.rect.center = (self.x, self.y)

    def movimento(self):
        # Movimento vertical dos carros
        self.y += self.vel

        if self.vel < 0:
            if self.y <= -75:
                self.y = ALTURA + 75
                self.vel = -1 * random.randint(1, 6)
        else:
            if self.y >= ALTURA + 75:
                self.y = -75
                self.vel = random.randint(4, 9)


class Bandeira(pg.sprite.Sprite):
    imagem_bandeira = pg.image.load('bandeira.png')

    def __init__(self):
        super().__init__()
        self.x = LARGURA / 2
        self.y = ALTURA / 2
        self.largura = 60
        self.altura = 90
        self.vel = 5

        self.image = self.imagem_bandeira
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.mask = pg.mask.from_surface(self.image)


    def update(self):
        self.rect.center = (self.x, self.y)
        self.movimento()

    def movimento(self):
        # Movimento vertical da bandeira
        self.y += self.vel
        if self.y >= ALTURA + self.altura:
            self.y = -self.altura / 2
            self.x = random.randint(100, LARGURA - 100)


# Imagens de explosão pré-carregadas
explosao_imagens = [pg.image.load('explosao_{}.png'.format(i)) for i in range(1, 9)]

class Explosao(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frame = 0
        self.x = x
        self.y = y
        self.image = explosao_imagens[0]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self):
        self.frame += 1
        if self.frame >= len(explosao_imagens):
            self.kill()
        else:
            self.image = explosao_imagens[self.frame]
            self.rect = self.image.get_rect(center=(self.x, self.y))


class Scoreboard:
    def __init__(self):
        self.font = pg.font.Font(None, 36)
        self.vidas = 3
        self.pontos = 0

    def draw(self, surface):
        # Desenhar as informações do placar na tela
        vidas_text = self.font.render('Vidas: {}'.format(self.vidas), 1, (10, 10, 10))
        pontos_text = self.font.render('Pontos: {}'.format(self.pontos), 1, (10, 10, 10))
        surface.blit(vidas_text, (10, 10))
        surface.blit(pontos_text, (10, 50))

    def perde_vida(self):
        # Reduzir a quantidade de vidas
        self.vidas -= 1

    def ganha_ponto(self):
        # Aumentar a quantidade de pontos
        self.pontos += 1


def colisao(sprite1, sprite2):
    # Verificar se houve colisão entre dois sprites usando máscaras de colisão
    return pg.sprite.collide_mask(sprite1, sprite2)


LARGURA = 800
ALTURA = 600

# Carregar as imagens para as telas de "You Win" e "Game Over"
you_win = pg.transform.scale(pg.image.load('tela1.png'), (LARGURA, ALTURA))
game_over = pg.transform.scale(pg.image.load('tela2.png'), (LARGURA, ALTURA))


pg.init()
pg.mixer.init()
musica = pg.mixer.music.load('muisca_de_fundo_cr.mp3')
pg.mixer.music.set_volume(0.5)

janela = pg.display.set_mode((LARGURA, ALTURA))
pg.display.set_caption("Jogo da Corrida")
tempo = pg.time.Clock()

personagem = Personagem()
carros = pg.sprite.Group(Carro(1), Carro(2))
bandeira = Bandeira()
explosoes = pg.sprite.Group()
scoreboard = Scoreboard()

game_started = False
instrucoes = pg.transform.scale(pg.image.load('tela_instrucoes.png'), (LARGURA, ALTURA))
pg.mixer.music.play(-1)

while True:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
        # Verificar se o jogador pressionou Enter para iniciar o jogo
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                game_started = True

    if not game_started:
        # Exibir as instruções do jogo
        janela.blit(instrucoes, (0,0))
        pg.display.update()
        continue
    tempo.tick(60)
    keys = pg.key.get_pressed()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

    janela.fill((255, 255, 255))

    personagem.movimento(keys)
    if colisao(personagem, bandeira):
        # Reposicionar a bandeira quando o personagem a toca
        bandeira.y = -bandeira.altura / 2
        bandeira.x = random.randint(100, LARGURA - 100)
        scoreboard.ganha_ponto()

    if scoreboard.pontos == 5:
        # Verificar se o jogador alcançou a pontuação necessária para vencer o jogo
        janela.blit(you_win, (0,0))
        pg.display.update()
        pg.time.wait(3000)  # Esperar 3 segundos
        pg.quit()

    if pg.sprite.spritecollide(personagem, carros, False, colisao):
        personagem.reset_pos()
        x, y = personagem.rect.center
        explosoes.add(Explosao(x, y))
        scoreboard.perde_vida()

        if personagem.perde_vida() < 0:
            # Verificar se o jogador perdeu todas as vidas
            janela.blit(game_over, (0,0))
            pg.display.update()
            pg.time.wait(3000)  # Esperar 3 segundos
            pg.quit()

    janela.blit(personagem.image, personagem.rect)
    carros.draw(janela)
    janela.blit(bandeira.image, bandeira.rect)

    personagem.update()
    carros.update()
    bandeira.update()
    explosoes.update()
    explosoes.draw(janela)

    scoreboard.draw(janela)

    pg.display.update()