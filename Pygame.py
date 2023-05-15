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
        self.rect.center = (self.x, self.y)

    def movment(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.x -= self.vel

        elif keys[pg.K_RIGHT]:
            self.x += self.vel

        if keys[pg.K_UP]:
            self.y -= self.vel

        elif keys[pg.K_DOWN]:
            self.y += self.vel


LARGURA = 640
ALTURA = 480

pg.init()
ganha = pg.display.set_mode((LARGURA, ALTURA))
pg.display.set_caption("Atravessando a Rua")
tempo = pg.time.Clock()

personagem = Personagem()
grupo_personagem = pg.sprite.Group()
grupo_personagem.add(personagem)

corrida = True
while corrida:
    tempo.tick(60)
    for e  in pg.event.get():
        if e.type == pg.QUIT:
            corrida = False

    ganha.fill((255, 255, 255))

    grupo_personagem.draw(ganha)
    grupo_personagem.update

    pg.display.update()

pg.quit()



