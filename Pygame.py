import pygame as pg
import time
import random

class Personagem(pg.sprite.Sprite):
    personagem1 = pg.image.load('personagem1.png')
    personagem2 = pg.image.load('personagem2.png')

    def _init_(self):
        super()._init_()
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

    def _init_(self, numero):
        super()._init_()
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

    def _init_(self):
        super()._init_()
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
    def _init_(self, x, y):
        super()._init_()
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
    def _init_(self):
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


