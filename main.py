# attaques par vagues du héros que l'on voit du dessus.
# +1 mob à chaque vague
# Faire des mini boss (ex tous les 10 vagues)
import random as rd
import pyxel as px
from time import sleep
# SAlut


class Boss:
    def __init__(self, target: tuple) -> None:
        self.x = rd.choice([-5, 261])
        self.y = rd.choice([i for i in range(1, 260)])
        self.dx = 1
        self.dy = 1
        self.width = 16
        self.height = 16
        self.target = target
        self.gauche = False
        self.esquive = False

    def get_coo(self):
        return (self.x, self.y)

    def update(self):
        if self.x > self.target[0]:
            self.x -= self.dx
            self.gauche = True
        if self.x < self.target[0]:
            self.x += self.dx
            self.gauche = False

        if self.y > self.target[1]:
            self.y -= self.dy
        if self.y < self.target[1]:
            self.y += self.dy

    def draw(self):

        j = (px.frame_count*0.5)//4 % 3
        if self.gauche:
            px.blt(self.x, self.y, 0, 16*j, 136, -16, 16, 5)  # 0,16,32,48
        else:
            px.blt(self.x, self.y, 0, 16*j, 136, 16, 16, 5)
        if self.esquive:
            for i in range(30):
                px.text(self.x, self.y-8, "LOUPE", 0)
            self.esquive = False


class Tir:
    def __init__(self, x, y, target: 'Araigne') -> None:
        self.x = x+8
        self.y = y+8
        self.target = target
        self.dx = 4*(self.target[0]-self.x)/self.calcul_distance()
        self.dy = 4*(self.target[1]-self.y)/self.calcul_distance()
        self.trop_loin = False

    def calcul_distance(self):
        return ((self.x-self.target[0])**2 + (self.y-self.target[1])**2)**0.5

    def update(self):
        self.x += self.dx
        self.y += self.dy

        if self.calcul_distance() > 200:
            self.trop_loin = True

    def draw(self):
        px.circ(int(self.x), int(self.y), 2, 4)


class Player:
    def __init__(self) -> None:
        self.x = 80
        self.moving = False
        self.y = 80
        self.width = 16
        self.height = 16
        self.health = 10
        self.dx = 2
        self.dy = 2
        self.target = (80, 80)
        self.alive = True
        self.attack_speed = 30
        self.ded_animation = False

    def die(self):
        print("TEST")
        self.alive = False
        self.ded_animation = False

    def get_coo(self):
        return (self.x, self.y)

    def update(self):
        # Si le joueur est vivant il peut bouger.
        if self.alive:
            if self.x > 10:
                if px.btn(px.KEY_Q):
                    self.x -= self.dx
                    self.moving = True
            if self.x < 236:
                if px.btn(px.KEY_D):
                    self.x += self.dx
                    self.moving = True
            if self.y > 10:
                if px.btn(px.KEY_Z):
                    self.y -= self.dy
                    self.moving = True
            if self.y < 236:
                if px.btn(px.KEY_S):
                    self.y += self.dy
                    self.moving = True
            self.moving = False

    def draw(self):
        if self.alive:
            j = px.frame_count*0.5//3 % 2
            if px.btn(px.KEY_Q):
                px.blt(self.x, self.y, 0, 16*j, 24, -16, 16, 5)
            elif px.btn(px.KEY_D):
                px.blt(self.x, self.y, 0, 16*j, 24, 16, 16, 5)
            else:
                px.blt(self.x, self.y, 0, 16*j, 8, 16, 16, 5)
        else:
            if not self.ded_animation:
                a = px.frame_count // 15 % 3
                px.blt(self.x, self.y, 0, 16 * a, 88, 16, 16, 5)
                if a == 2:
                    self.ded_animation = True
            else:
                px.blt(self.x, self.y, 0, 16 * 2, 88, 16, 16, 5)


class Araigne:
    def __init__(self, target: tuple) -> None:
        self.x = rd.choice([-5, 261])
        self.y = rd.choice([i for i in range(-15, 260)])
        self.dx = 1
        self.dy = 1
        self.width = 16
        self.height = 16
        self.target = target
        self.gauche = False
        self.esquive = False

    def get_coo(self):
        return (self.x, self.y)

    def update(self):
        if self.x > self.target[0]:
            self.x -= self.dx
            self.gauche = True
        if self.x < self.target[0]:
            self.x += self.dx
            self.gauche = False

        if self.y > self.target[1]:
            self.y -= self.dy
        if self.y < self.target[1]:
            self.y += self.dy

    def draw(self):

        j = (px.frame_count*0.5)//4 % 3
        if self.gauche:
            px.blt(self.x, self.y, 0, 16*j, 136, -16, 16, 5)  # 0,16,32,48
        else:
            px.blt(self.x, self.y, 0, 16*j, 136, 16, 16, 5)
        if self.esquive:
            for i in range(30):
                px.text(self.x, self.y-8, "LOUPE", 0)
            self.esquive = False


class Game:
    def __init__(self) -> None:
        px.init(256, 256, fps=30)
        px.load("assets/3.pyxres")
        self.player = Player()
        self.araigne_list = [Araigne((80, 80))]
        self.tir_list = []
        self.max_health = 10
        self.waves = 1
        # suite fibonacci (0.1.1.2.3.5.8.13.21.34.55.89...)
        self.suite_fibo = [0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
        self.wave_arachnidee_number = self.suite_fibo[self.waves]
        self.spawnrate = 30
        self.counter = 0
        px.run(self.update, self.draw)

    def distance(self, arachnidee):
        self.arachnidee_x = arachnidee.get_coo()[0]
        self.arachnidee_y = arachnidee.get_coo()[1]
        return (((self.position_player[1] - self.arachnidee_y)**2 + (self.position_player[0]-self.arachnidee_x)**2)**0.5)

    def fibonacci(n):
        if n <= 1:
            return n
        else:
            return Game.fibonacci(n-1) + Game.fibonacci(n-2)

    def health_heart(self):
        x = 5
        for i in range(1, self.player.health):
            px.blt(x, 238, 0, 48, 200, 16, 16, 5)
            x += 16

    def add_araigne(self):
        if self.player.alive:
            self.araigne_list.append(Araigne(self.position_player))

    def add_tir(self):
        self.tir_list.append(
            Tir(self.position_player[0], self.position_player[1], self.plus_proche_araignee))

    def touche(box1, box2):
        return not (
            (box2.x >= box1.x + box1.width)
            or (box2.x + box2.width <= box1.x)
            or (box2.y >= box1.y + box1.height)
            or (box2.y + box2.height <= box1.y)
        )

    def collision_avec(self):
        for test in self.araigne_list:
            if Game.touche(self.player, test):
                self.player.health -= 1
                self.araigne_list.remove(test)

    def collision(self):
        # cette fonction gère la collision
        for ara in self.araigne_list:
            for tir in self.tir_list:

                if ara.x+8 > tir.x > ara.x-8 and ara.y+8 > tir.y > ara.y-8:
                    """
                    self.chance = rd.choice(
                        [True, True, True, True, True, False, False, False, False, False,])
                    print(self.chance)
                    if self.chance and not (ara.esquive):
                        print('Araigné tué')
                    else:
                        ara.esquive = True"""
                    self.tir_list.remove(tir)
                    self.araigne_list.remove(ara)

    def wave(self):
        self.waves += 1
        if self.waves % 2 == 0:
            self.player.attack_speed -= 1
        print(self.waves)

        print(Game.fibonacci(self.waves))
        if px.frame_count % self.spawnrate == 0:
            for i in range(Game.fibonacci(self.waves)):
                self.add_araigne()

    def update(self):
        # update player
        self.position_player = self.player.get_coo()
        self.player.update()
        # Check les collisions
        self.collision()
        self.collision_avec()
        # Système de vagues un peu pétée
        """
        if self.waves == 1:
            for i in range(self.wave_arachnidee_number):
                if px.frame_count % self.spawnrate == 0:
                    self.add_araigne()
        """
        if len(self.araigne_list) == 0 and px.frame_count % 30 == 0:
            self.wave()

        # Vérifie si le joueur est mort
        if self.player.health == 0:
            self.player.alive = False
        # Vérifie si le joueur peut tirer en regardant la liste des araignée n'est pas vide et qu'il ne bouge pas (Ne marche pas)
        if len(self.araigne_list) != 0:
            self.plus_proche_araignee = sorted(
                self.araigne_list, key=self.distance)[0].get_coo()
            if px.frame_count % self.player.attack_speed == 0 and self.player.moving == False and self.player.alive:
                self.add_tir()
        else:
            pass
        # Update les araignées
        for arachnidee in self.araigne_list:
            arachnidee.target = self.position_player
            arachnidee.update()

        # Update les tirs
        for tir in self.tir_list:
            if tir.trop_loin == True:
                self.tir_list.remove(tir)
            tir.update()

    def draw(self):
        px.cls(0)
        # bltm(x, y, tm, u, v, w, h, [colkey])
        # bltm(x, y, tm, u, v, w, h, [colkey])
        px.bltm(0, 0, 7, 0, 0, 256, 256)
        self.player.draw()
        if self.player.alive:
            for arachnidee in self.araigne_list:
                arachnidee.draw()
        for tir in self.tir_list:
            tir.draw()
        self.health_heart()
        px.text(20, 20, f'{self.waves}', 8)
        px.text(170, 20, f"Ennemi Restant : {len(self.araigne_list)}", 8)


Game()
