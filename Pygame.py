import pygame as pg
class Personagem(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 50
        self.y = ALTURA/2
        self.vel = 4
        self.largura = 100
        self.altura = 50
        self.personagem1 = pg.image.load('personagem1.png')
        self.personagem2 = pg.image.load('personagem2.png')
        self.personagem1 = pg.transform.scale(self.personagem1, (self.largura, self.altura))
        self.personagem2 = pg.transform.scale(self.personagem2, (self.largura, self.altura))
        self.image = self.personagem1
        self.rect = self.image.get_rect()

    def update(self):
        self.movment
        self.movment()
        self.correcao()
        self.rect.center = (self.x, self.y)

    def movment(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.x -= self.vel
            self.image = self.personagem2

        elif keys[pg.K_RIGHT]:
            self.x += self.vel
            self.image = self.personagem1

        if keys[pg.K_UP]:
            self.y -= self.vel
        elif keys[pg.K_DOWN]:
            self.y += self.vel


    def correcao(self):
        if self.x - self.largura /2<0:
            self.x = self.largura/2

        elif self.x + self.largura / 2  > LARGURA:
            self.x = LARGURA - self.largura / 2


        if self.y - self.altura /2 < 0:
            self.y = self.altura/2

        elif self.y + self.altura / 2 > ALTURA:
            self.y = ALTURA - self.altura / 2




class carro(pg.sprite.Sprite):
    def __init__(self, numero):
        super().__init__()
        if numero == 1:
            self.x =190
            self.image =pg.image.load('band_vermelha.png')
            self.image = -4


        else:
            self.x = 460
            self.image = pg.image.load('band_azul.png')
            self.vel = 5

        self.y = ALTURA / 2
        self.largura = 100
        self.altura = 150
        self.image = pg.transform.scale(self.image, (self.largura, self.altura))
        self.rect = self.image.get_rect()


    def atualizacao(self):
        self.movimento()
        self.rect.center += (self.x, self.y)


    def movimento(self):
        self.y += self.vel

        if self.y - self.altura / 2 < 0 :
            self.y = self.altura / 2
            self.vel *= -1

        elif self.y + self.altura / 2 > ALTURA:
            self.y = ALTURA - self.altura / 2
            self.vel *= -1








LARGURA = 640
ALTURA = 480

pg.init()
ganha = pg.display.set_mode((LARGURA, ALTURA))
pg.display.set_caption("Atravessando a Rua")
tempo = pg.time.Clock()
personagem = Personagem()
grupo_personagem = pg.sprite.Group()
grupo_personagem.add(personagem)



band_vermelha = carro(1)
band_azul = carro(2)
grupo_band = pg.sprite.Group()
grupo_band.add(band_vermelha,band_azul)

corrida = True
while corrida:
    tempo.tick(60)
    for e  in pg.event.get():
        if e.type == pg.QUIT:
            corrida = False
    ganha.fill((255, 255, 255))

    grupo_personagem.draw(ganha)
    grupo_personagem.update
    grupo_band.draw(ganha)

    grupo_personagem.update()

    grupo_band.update()

    pg.display.update()

pg.quit()