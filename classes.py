import functions
import data
import pygame
import math
from random import randint, uniform


class Player:
    def __init__(self):
        # animations = []
        # temp = pygame.image.load("files/player/body_side.png")
        # data.animations.append(Animation(self, temp, 10, 50, False, data.body_offsetX, data.body_offsetY))
        # data.animations.append(Animation(self, temp, 10, 50, True, data.body_offsetX, data.body_offsetY))
        # temp = pygame.image.load("files/player/body_forward.png")
        # data.animations.append(Animation(self, temp, 10, 50, False, data.body_offsetX, data.body_offsetY))

        self.room = None
        self.floor = None
        self.floorCount = 0
        self.x = 240
        self.y = 136
        self.speed = 1.8
        self.velocityX = 0
        self.velocityY = 0
        self.acceleration = 1
        self.type = "player"
        self.facing = 0
        self.animationTimer = 0
        self.animationPhase = 0
        self.animationTimerLimit = 10
        self.animationPhaseLimit = 8
        self.invincibility = False
        self.invincibilityTimer = 60
        self.attackSpeed = 1.8
        self.projectileLifetime = 1
        self.projectileSpeed = 2.5
        self.effects = []
        self.damage = 1
        self.health = 3
        self.maxHealth = 3
        self.critChance = 0
        self.currentItems = []
        self.attackSpeedTimer = 0
        self.collisionBoxOffsetX = 13
        self.collisionBoxOffsetY = 25
        self.collisionBoxWidth = 15
        self.collisionBoxHeight = 12
        self.collisionBox = CollisionBox(self.x + 13, self.y + 25, 15, 12)
        self.comeTimer = 0
        self.electrocuteHit = 0
        self.electrocuteTimer = 0
        self.electrocuteAvailable = True
        self.electrocuteCooldown = 5
        self.direction = 0
        self.head_direction = 0
        self.darkharvestStacks = 0
        self.conquerorStacks = 0
        self.conquerorTimer = 0
        self.conquerorCooldown = 3
        self.tempoCooldown = 8
        self.tempoDuration = 6
        self.tempoTimer = 0
        self.tempoOn = False
        self.tempoAvailable = True
        self.graspCooldown = 30
        self.graspAvailable = True
        self.graspTimer = 0
        self.dead = False
        self.deadTimer = 0

    def draw(self):
        if self.invincibility == False or self.invincibility == True and self.invincibilityTimer % 4 == 0:
            #functions.draw_image(data.body_forward[self.animationPhase], self.x + data.body_offsetX, self.y + data.body_offsetY)
            #data.animations[data.test].tick()

            keys = pygame.key.get_pressed()

            if not (not keys[pygame.K_w] and not keys[pygame.K_s] and not keys[pygame.K_a] and not keys[
                    pygame.K_d]):
                    if self.direction == 0 or self.direction == 2:
                        data.animations[2].tick()
                    if self.direction == 1:
                        data.animations[0].tick()
                    if self.direction == 3:
                        data.animations[1].tick()
            else:
                functions.draw_image(data.body_forward[0], self.x + data.body_offsetX, self.y + data.body_offsetY)

            if self.conquerorStacks == 12:
                functions.draw_image(data.conqueror_png, self.x, self.y)

            if self.tempoOn:
                functions.draw_image(data.tempo_png, self.x, self.y+10)

            if not self.dead:
                functions.draw_image(data.head[self.head_direction * 2], self.x, self.y)
        #pygame.draw.rect(data.screen, (255,0,0), (self.x + self.collisionBoxOffsetX, self.y + self.collisionBoxOffsetY, self.collisionBoxWidth, self.collisionBoxHeight), 1)

    def shoot(self, direction):

        if self.attackSpeedTimer > (60 / self.attackSpeed):
            speedX = 0
            speedY = 0

            if direction == "left":
                speedX = -self.projectileSpeed
                angle = math.pi
            if direction == "right":
                speedX = self.projectileSpeed
                angle = 0
            if direction == "up":
                speedY = -self.projectileSpeed
                angle = math.pi*3/2
            if direction == "down":
                speedY = self.projectileSpeed
                angle = math.pi / 2

            data.gameObjects.append(Projectile(self.x + data.projectile_offsetX, self.y + data.projectile_offsetY, speedX, speedY, self))

            if "runaan" in self.effects:
                data.gameObjects.append(
                    Projectile(self.x + data.projectile_offsetX, self.y + data.projectile_offsetY, math.cos(angle+math.pi/8)*self.projectileSpeed, math.sin(angle+math.pi/8)*self.projectileSpeed,
                               self))
                data.gameObjects.append(
                    Projectile(self.x + data.projectile_offsetX, self.y + data.projectile_offsetY, math.cos(angle-math.pi/8)*self.projectileSpeed, math.sin(angle-math.pi/8)*self.projectileSpeed,
                               self))

            self.attackSpeedTimer = 0

    def move(self):
        keys = pygame.key.get_pressed()


        for i in self.room.items:
            if functions.box_collision2(self.collisionBox, i.collisionBox):
                functions.pickupItem(self, i)

        if keys[pygame.K_a]:
            self.direction = 3
            if not functions.testPosition(self, -self.speed, 0):
                self.x -= self.speed
        if keys[pygame.K_d]:
            self.direction = 1
            if not functions.testPosition(self, self.speed, 0):
                self.x += self.speed
        if keys[pygame.K_w]:
            self.direction = 2
            if not functions.testPosition(self, 0, -self.speed):
                self.y -= self.speed
        if keys[pygame.K_s]:
            self.direction = 0
            if not functions.testPosition(self, 0, self.speed):
                self.y += self.speed


        if keys[pygame.K_LEFT]:
            self.head_direction = 3
            self.shoot("left")
        if keys[pygame.K_RIGHT]:
            self.head_direction = 1
            self.shoot("right")
        if keys[pygame.K_UP]:
            self.head_direction = 2
            self.shoot("up")
        if keys[pygame.K_DOWN]:
            self.head_direction = 0
            self.shoot("down")

        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self.head_direction = 0

        self.collisionBox.x = self.x + 13
        self.collisionBox.y = self.y + 25

        # left x < 30
        # up y < 10
        # down y > 200
        # right x > 420

        if self.x < 30:
            self.room = self.floor.layout[self.room.floorY][self.room.floorX-1]
            functions.leavingRoom(self.room)
            #self.room = self.room.adjacentRooms[2]
            self.x = 394
            self.y = 100

        if self.x > 420:
            self.room = self.floor.layout[self.room.floorY][self.room.floorX+1]
            functions.leavingRoom(self.room)
            #self.room = self.room.adjacentRooms[3]
            self.x = 44
            self.y = 100

        if self.y < 10:
            self.room = self.floor.layout[self.room.floorY-1][self.room.floorX]
            functions.leavingRoom(self.room)
            #self.room = self.room.adjacentRooms[0]
            self.x = 218
            self.y = 184

        if self.y > 200:
            self.room = self.floor.layout[self.room.floorY+1][self.room.floorX]
            functions.leavingRoom(self.room)
            #dself.room = self.room.adjacentRooms[1]
            self.x = 218
            self.y = 22

    def invincibility_function(self):
        if self.invincibility:
            self.invincibilityTimer -= 1
        if self.invincibilityTimer <= 0:
            self.invincibilityTimer = 60
            self.invincibility = False

    def do_effects(self):
        if "come" in self.effects:
            self.comeTimer += 1
            if self.comeTimer > 8:
                self.comeTimer = 0
                data.gameObjects.append(Projectile(self.x+12+randint(0,6), self.y + 20 + randint(0,6), 0, 0, self, 4, "come"))

        if "electrocute" in self.effects:
            if self.electrocuteAvailable == False:
                self.electrocuteTimer += 1
            if self.electrocuteTimer > self.electrocuteCooldown * 60:
                self.electrocuteAvailable = True
                self.electrocuteTimer = 0

        if "conqueror" in self.effects:
            self.conquerorTimer += 1
            if self.conquerorTimer >= self.conquerorCooldown * 60:
                self.conquerorStacks = 0
                self.conquerorTimer = 0

        if "tempo" in self.effects:
            if self.tempoOn == False and self.tempoAvailable == False:
                self.tempoTimer += 1
                if self.tempoTimer >= self.tempoCooldown * 60:
                    self.tempoAvailable = True
                    self.tempoTimer = 0
            if self.tempoOn:
                self.tempoTimer += 1
                if self.tempoTimer >= self.tempoDuration * 60:
                    self.tempoTimer = 0
                    self.tempoAvailable = False
                    self.tempoOn = False

        if "grasp" in self.effects:
            if self.graspAvailable == False:
                self.graspTimer += 1
                if self.graspTimer > self.graspCooldown * 60:
                    self.graspAvailable = True



    def tick(self):

        if self.dead:
            self.deadTimer += 1

        if self.deadTimer >= 50:

            if "guardian" in self.effects:
                self.dead = False
                data.gameObjects.append(Sprite(self.x, self.y, self.room, data.items_png[27], 1, self, 0, -15))


            data.music_channel.stop()
            data.Scene = 3
            return

        if self.health <= 0:
            self.dead = True

        self.attackSpeedTimer += 1
        if self.tempoOn:
            self.attackSpeedTimer += 1
        if not self.dead:
            self.invincibility_function()
            self.do_effects()
            self.move()
        self.draw()

class Projectile:
    def __init__(self, x, y, speedX, speedY, owner, lifetime=1, special = None):
        self.x = x
        self.y = y
        self.speedX = speedX
        self.speedY = speedY
        self.owner = owner
        self.room = owner.room
        self.type = "projectile"
        self.lifetimeTimer = 0
        self.lifetime = lifetime
        self.collisionBox = CollisionBox(self.x, self.y, data.tear.get_width(), data.tear.get_height(), self)
        self.special = special

    def draw(self):
        if self.owner.type == "player":

            if self.special == "come":
                functions.draw_image(data.come, self.x, self.y)
            else:
                functions.draw_image(data.tear, self.x, self.y)
        else:
            functions.draw_image(data.enemy_tear, self.x, self.y)

    def tick(self):
        self.lifetimeTimer += 1

        if self.lifetimeTimer > (60 * self.lifetime):
            data.gameObjects.remove(self)
            del self
            return

        for i in self.room.collisionBoxes:
            if functions.box_collision2(i, self.collisionBox):
                data.gameObjects.remove(self)
                del self
                return

        for i in self.room.obstacles:
            if functions.box_collision2(i.collisionBox, self.collisionBox):
                if i.breakable:

                    if i.id == 2:
                        data.glass_break_sound.play()

                    self.room.obstacles.remove(i)
                    del i

                data.gameObjects.remove(self)
                del self
                return

        for i in data.gameObjects:
            if i.room != self.room:
                continue
            if i == self.owner or i.type != "player" and i.type != "enemy" and i.type != "boss":
                continue

            if self.owner.type == "enemy" and i.type == "enemy":
                continue

            if functions.box_collision2(i.collisionBox, self.collisionBox):

                if self.owner.type == "player" and (i.type == "enemy" or i.type == "boss"):

                    data.hit_marker_sound.play()

                    if "electrocute" in data.player.effects and data.player.electrocuteAvailable:
                        data.player.electrocuteHit += 1
                        if data.player.electrocuteHit >= 3:
                            data.player.electrocuteHit = 0
                            data.player.electrocuteAvailable = False
                            data.player.electrocuteTimer = 0

                            data.gameObjects.append(Sprite(i.x, i.y-data.electrocute_png.get_height()+10, i.room, data.electrocute_png, 0.3))
                            data.electrocute_sound.play()
                            functions.damage(data.player, i, 4)

                    if "harvest" in data.player.effects:
                        if i.maxHealth/2 >= i.health:
                            if i.harvested == False:
                                i.harvested = True
                                data.harvest_sound.play()
                                data.player.darkharvestStacks += 1
                                i.health -= 1 + data.player.darkharvestStacks * 0.25

                    if "conqueror" in data.player.effects:
                        if data.player.conquerorStacks == 11:
                            data.conqueror_sound.play()
                        data.player.conquerorStacks += 1
                        if data.player.conquerorStacks > 12:
                            data.player.conquerorStacks = 12
                        data.player.conquerorTimer = 0

                    if "tempo" in data.player.effects:
                        if data.player.tempoAvailable:
                            data.player.tempoOn = True
                            data.player.tempoAvailable = False
                            data.player.tempoTimer = 0
                            data.tempo_sound.play()

                    if "grasp" in data.player.effects:
                        if data.player.graspAvailable:
                            data.player.graspAvailable = False
                            data.player.graspTimer = 0
                            data.grasp_sound.play()
                            data.player.maxHealth += 0.5





                print(self.owner.type, "damaged", i.type)
                print(i == self.owner)

                functions.damage(self.owner, i)
                data.gameObjects.remove(self)
                del self
                return

        self.x += self.speedX
        self.y += self.speedY
        self.collisionBox.x = self.x
        self.collisionBox.y = self.y
        self.draw()


# 13 x 7


class CollisionBox:

    def __init__(self, x, y, w, h, owner=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.owner = owner


class Obstacle:
    def __init__(self, x, y, id):
        self.x = 50 + x*30
        self.y = 44 + y*30
        self.collisionBox = CollisionBox(self.x, self.y, 32, 32)
        self.id = id
        self.breakable = False
        if self.id == 2:
            self.breakable = True

    def draw(self):
        functions.draw_image(data.obstacles[self.id], self.x, self.y)

class Floor:
    def __init__(self):
        self.layout = []

        for _ in range(0,15):
            self.layout.append([None,None,None,None,None,None,None,None,None,None,None,None,None,None,None])

    def randomizeFloor(self, size=5, roomCount = 10):
        self.layout[7][7] = Room(7, 7, self)
        roomCount = 10 + data.player.floorCount * 7
        directions_numbers = [[0, -1], [0, 1], [-1, 0], [1, 0]]

        for _ in range(0, roomCount):
            # get all rooms in a list
            rooms = []

            for i in self.layout:
                for j in i:
                    if j is not None:
                        rooms.append(j)

            # select a random room
            targetRoom = rooms[randint(0, len(rooms)-1)]

            # add neighbour in random direction

            directions = ["up", "down", "left", "right"]

            if functions.isSlotOccupied(self, targetRoom, [0, -1]):
                directions.remove("up")
            if functions.isSlotOccupied(self, targetRoom, [0, 1]):
                directions.remove("down")
            if functions.isSlotOccupied(self, targetRoom, [-1, 0]):
                directions.remove("left")
            if functions.isSlotOccupied(self, targetRoom, [1, 0]):
                directions.remove("right")

            try:
                chosen_direction = directions[randint(0, len(directions)-1)]
            except:
                print("cannot make room at ", targetRoom.floorX, targetRoom.floorY)
                continue
            if chosen_direction == "up":
                self.layout[targetRoom.floorY - 1][targetRoom.floorX] = Room(targetRoom.floorY - 1, targetRoom.floorX, self)
            if chosen_direction == "down":
                self.layout[targetRoom.floorY + 1][targetRoom.floorX] = Room(targetRoom.floorY + 1, targetRoom.floorX, self)
            if chosen_direction == "left":
                self.layout[targetRoom.floorY][targetRoom.floorX - 1] = Room(targetRoom.floorY, targetRoom.floorX - 1, self)
            if chosen_direction == "right":
                self.layout[targetRoom.floorY][targetRoom.floorX + 1] = Room(targetRoom.floorY, targetRoom.floorX + 1, self)

        # make some rooms item rooms

        # get all rooms in a list
        rooms = []
        left = self.layout[7][7]
        right = self.layout[7][7]
        up = self.layout[7][7]
        down = self.layout[7][7]

        for i in self.layout:
            for j in i:
                if j is not None:
                    if j is not self.layout[7][7]:
                        rooms.append(j)
                        if j.floorX < left.floorX:
                            left = j
                        if j.floorX > right.floorX:
                            right = j
                        if j.floorY < up.floorX:
                            up = j
                        if j.floorX < down.floorX:
                            down = j

        targetRoom = rooms[randint(0, len(rooms) - 1)]

        targetRoom.items.append(Item(200, 200, functions.get_item_id()))
        targetRoom.itemRoom = True

        rooms.remove(targetRoom)

        r = randint(0, 5 - data.player.floorCount)

        if r == 0:
            targetRoom = rooms[randint(0, len(rooms) - 1)]

            targetRoom.items.append(Item(200, 200, functions.get_item_id()))
            targetRoom.itemRoom = True

            rooms.remove(targetRoom)



        # make boss room

        targetRoom = rooms[randint(0, len(rooms) - 1)]
        print(targetRoom)
        print("room", targetRoom.floorX, targetRoom.floorY, "is boss room")

        temp = Boss(targetRoom)
        data.gameObjects.append(temp)
        targetRoom.boss = temp
        targetRoom.bossRoom = True


        # add doors to rooms

        for i in self.layout:
            for j in i:
                if j is not None:
                    x = j.floorX
                    y = j.floorY
                    for k in directions_numbers:
                        if 0 <= x + k[0] < 15 and 0 <= y + k[1] < 15:
                            if self.layout[y + k[1]][x + k[0]] is not None:
                                j.adjacentRooms[directions_numbers.index(k)] = self.layout[y + k[1]][x + k[0]]
                                functions.add_door_wall(j, k)
                            else:
                                functions.add_wall(j, k)
                    j.generateWalls()

        # get all rooms in a list
        rooms = []

        for i in self.layout:
            for j in i:
                if j is not None:
                    rooms.append(j)

        # randomize all rooms
        for i in rooms:
            i.randomizeRoom()


class Boss:
    def __init__(self, room):
        self.id = data.player.floorCount
        self.x = 215
        self.y = 100
        self.health = 100 + self.id * 15
        self.maxHealth = self.health
        self.damage = 1
        self.room = room
        self.type = "boss"
        self.speed = 0.1
        self.floor = room.floor
        #self.id = data.player.floorCount
        self.image = data.boss_salt
        self.attackCooldown = 100
        self.attackCooldownTimer = 0
        self.harvested = False
        self.secondPhase = False
        self.value = 0

        if self.id == 2:
            self.speed = 0.5

        if self.id == 0:
            self.secondPhase = False

        if self.id == 1:
            self.image = data.boss_spood

        if self.id == 2:
            self.image = data.boss_cat

        if self.id == 3:
            self.image = data.boss_speed
            self.attackCooldown = 200

        if self.id == 4:
            self.image = data.boss_glebu
            self.y = 35

        self.collisionBox = CollisionBox(self.x, self.y, self.image.get_width(), self.image.get_height(), self)


    def draw(self):
        functions.draw_image(self.image, self.x, self.y)
        if "harvest" in data.player.effects and self.harvested == False and self.maxHealth/2 >= self.health:
            functions.draw_image(data.harvest_png, self.x + int(self.image.get_width()/2) - 10, self.y + int(self.image.get_height()/2) - 10)

    def ai(self):

        angle = functions.get_angle(self.x, self.y, data.player.x, data.player.y)

        if self.secondPhase == False and self.health < self.maxHealth / 2:
            data.boss_angry.play()
            self.secondPhase = True

        if self.id == 0:
            self.attackCooldownTimer += 1
            if self.secondPhase == True:
                self.attackCooldownTimer += 1

            if self.attackCooldownTimer > self.attackCooldown:
                self.attackCooldownTimer = 0
                attackCount = randint(12,18)
                for i in range(0, attackCount):
                    a = 2*math.pi/attackCount
                    data.gameObjects.append(Projectile(self.x + 25, self.y + 60, math.cos(a*i), math.sin(a*i), self, 20))

        if self.id == 1:
            self.attackCooldownTimer += 1
            if self.secondPhase == True:
                self.attackCooldownTimer += 1

            if self.attackCooldownTimer > self.attackCooldown:
                self.attackCooldownTimer = 0
                attackCount = 16
                for i in range(0, attackCount):
                    r = uniform(0, math.pi / 2)
                    ang = angle + r - r/2
                    data.gameObjects.append(Projectile(self.x + 25, self.y + 25, math.cos(ang), math.sin(ang), self, 20))

        if self.id == 2:
            self.attackCooldownTimer += 1
            if self.secondPhase == True:
                self.attackCooldownTimer += 1
                self.speed = 0.8

            if self.attackCooldownTimer > self.attackCooldown:
                self.attackCooldownTimer = 0
                data.gameObjects.append(Projectile(self.x + 25, self.y + 25, math.cos(angle), math.sin(angle), self, 20))
                if self.secondPhase == True:
                    data.gameObjects.append(Projectile(self.x + 25, self.y + 25, math.cos(angle)*2, math.sin(angle)*2, self, 20))
                    r = randint(0, 7)
                    if r == 0:
                        attackCount = randint(12, 18)
                        for i in range(0, attackCount):
                            a = 2 * math.pi / attackCount
                            data.gameObjects.append(
                                Projectile(self.x + 25, self.y + 25, math.cos(a * i), math.sin(a * i), self, 20))

        if self.id == 3:
            self.attackCooldownTimer += 1
            if self.secondPhase == True:
                self.attackCooldownTimer += 1

            if self.attackCooldownTimer > self.attackCooldown:
                self.attackCooldownTimer = 0
                attackCount = 8
                for i in range(0, attackCount):
                    a = 2*math.pi/attackCount
                    data.gameObjects.append(Projectile(self.x + 25, self.y + 25, math.cos(a*i), math.sin(a*i), self, 20))


                r = randint(0, 4)
                if r == 0 and self.value < 10:
                    functions.add_random_enemy(self.x + 50, self.y + 50, self.room)
                    self.value += 1


        if self.id == 4:
            self.attackCooldownTimer += 1
            if self.secondPhase == True:
                self.attackCooldownTimer += 1

            if self.attackCooldownTimer > self.attackCooldown:
                self.attackCooldownTimer = 0

                self.value += 1

                if self.value > 6:
                    self.value = 0
                    functions.add_random_enemy(60, 180, self.room)
                    functions.add_random_enemy(340, 180, self.room)

                r = randint(0, 1)

                if r == 0:
                    attackCount = randint(12,18)
                    for i in range(0, attackCount):
                        a = 2*math.pi/attackCount
                        data.gameObjects.append(Projectile(self.x + 75, self.y + 25, math.cos(a*i), math.sin(a*i), self, 20))

                if r == 1:
                    attackCount = 16
                    for i in range(0, attackCount):
                        r = uniform(0, math.pi / 2)
                        ang = angle + r - r / 2
                        data.gameObjects.append(
                            Projectile(self.x + 75, self.y + 25, math.cos(ang), math.sin(ang), self, 20))






    def follow(self):

        if self.id == 4:
            if self.x + 50 > data.player.x:
                self.x -= 0.5
            if self.x + 50 < data.player.x:
                self.x += 0.5

            self.collisionBox.x = self.x
            self.collisionBox.y = self.y

            return




        angle = functions.get_angle(self.x, self.y, data.player.x, data.player.y)
        speedX = math.cos(angle) * self.speed
        speedY = math.sin(angle) * self.speed

        self.x += speedX
        self.y += speedY

        self.collisionBox.x = self.x
        self.collisionBox.y = self.y

        if functions.box_collision2(self.collisionBox, data.player.collisionBox):
            functions.damage(self, data.player)


    def tick(self):
        if self.health <= 0:
            self.die()
        self.follow()
        self.ai()
        self.draw()


    def die(self):
        data.gameObjects.append(Hatch(self.room))
        if self.id == 0:
            data.boss_salt_death.play()

        data.music_channel.stop()
        self.room.boss = None
        data.gameObjects.remove(self)
        self.room.items.append(Item(228, 180, functions.get_item_id()))
        del self
        return


class Enemy:
    def __init__(self, x, y, room, id):
        self.x = x
        self.y = y
        self.id = id
        self.attackSpeed = data.enemy_attackspeed[self.id]
        self.attackSpeedTimer = 0
        self.maxHealth = data.enemy_health[self.id]
        self.health = self.maxHealth
        self.damage = 1
        self.floor = room.floor
        self.room = room
        self.speed = 0.5
        self.image = data.enemy_png[self.id]
        self.type = "enemy"
        self.collisionBox = CollisionBox(self.x, self.y, self.image.get_width(), self.image.get_height(), self)
        self.harvested = False

    def draw(self):
        functions.draw_image(self.image, self.x, self.y)
        if "harvest" in data.player.effects and self.harvested == False and self.maxHealth/2 >= self.health:
            functions.draw_image(data.harvest_png, self.x + int(self.image.get_width()/2) - 10, self.y + int(self.image.get_height()/2) - 10)

    def shoot(self):
        pi = math.pi
        angle = functions.get_angle(self.x, self.y, data.player.x + 10, data.player.y + 15)
        if self.attackSpeedTimer > (60 / self.attackSpeed):

            if self.id == 0:
                data.gameObjects.append(Projectile(self.x, self.y, math.cos(angle), math.sin(angle), self, 2.5))
            elif self.id == 1:
                for i in range(0, 4):
                    data.gameObjects.append(Projectile(self.x, self.y, math.cos(pi/4 + (pi/2)*i), math.sin(pi/4 + (pi/2)*i), self, 2.5))
            elif self.id == 2:
                for i in range(0, 4):
                    data.gameObjects.append(Projectile(self.x, self.y, math.cos((pi/2)*i), math.sin((pi/2)*i), self, 2.5))
            elif self.id == 3:
                for i in range(0, 4):
                    r = uniform(0, 2*pi)
                    data.gameObjects.append(Projectile(self.x, self.y, math.cos(r), math.sin(r), self, 2.5))
            elif self.id == 5:
                for i in range(0, 6):
                    r = uniform(0, pi/8)
                    r -= pi/16
                    data.gameObjects.append(Projectile(self.x, self.y, math.cos(angle + r), math.sin(angle + r), self, 1.5))
            elif self.id == 6:
                data.gameObjects.append(Projectile(self.x, self.y, math.cos(angle+pi/4), math.sin(angle+pi/4), self, 2.5))
                data.gameObjects.append(Projectile(self.x, self.y, math.cos(angle-pi/4), math.sin(angle-pi/4), self, 2.5))
            elif self.id == 7:
                data.gameObjects.append(Projectile(self.x, self.y, math.cos(angle), math.sin(angle), self, 2.5))
            elif self.id == 8:
                data.gameObjects.append(Projectile(self.x, self.y, math.cos(angle), math.sin(angle), self, 2.5))


            self.attackSpeedTimer = 0

    def die(self):
        if self.id == 9:
            self.room.items.append(Item(self.x, self.y, functions.get_item_id()))

        r = randint(0, 10)
        if r == 0:
            self.room.items.append(Item(self.x, self.y, 28))

        data.gameObjects.remove(self)
        del self

    def follow(self):
        angle = functions.get_angle(self.x, self.y, data.player.x, data.player.y)
        speedX = math.cos(angle) * self.speed
        speedY = math.sin(angle) * self.speed

        if not functions.testPosition(self, speedX, 0):
            self.x += speedX

        if not functions.testPosition(self, 0, speedY):
            self.y += speedY


    def move(self):
        self.follow()
        self.collisionBox.x = self.x
        self.collisionBox.y = self.y

        if functions.box_collision2(self.collisionBox, data.player.collisionBox):
            functions.damage(self, data.player)


    def tick(self):
        self.attackSpeedTimer += 1

        if self.health <= 0:
            self.die()
            return
        self.move()
        self.shoot()
        self.draw()
        #functions.drawBox(self.collisionBox)



class Room:
    def __init__(self, floorY = 2, floorX = 2, floor = None):
        self.collisionBoxes = []
        self.doorCollisionBoxes = []
        self.obstacles = []
        #                     Up,   Down, Left, Right
        self.adjacentRooms = [None, None, None, None]
        self.items = []
        self.boss = None
        self.floor = floor
        self.floorX = floorX
        self.floorY = floorY
        self.itemRoom = False
        self.bossRoom = False
        self.visited = False
        self.vision = False

    def draw(self):

        data.screen.fill((0, 0, 0))
        functions.draw_map()

        for i in self.adjacentRooms:
            if i is not None:
                i.vision = True

        self.visited = True

        closed = functions.are_enemies_in_room(self)

        if not closed:
            self.doorCollisionBoxes = []

        if self.adjacentRooms[0] is not None:
            if self.adjacentRooms[0].itemRoom:
                if closed:
                    functions.draw_image(data.item_door_top_closed, 217, 17)
                else:
                    functions.draw_image(data.item_door_top, 217, 17)
            elif self.adjacentRooms[0].bossRoom:
                if closed:
                    functions.draw_image(data.boss_door_top_closed, 217, 17)
                else:
                    functions.draw_image(data.boss_door_top, 217, 17)
            else:
                if closed:
                    functions.draw_image(data.door_top_closed, 217, 17)
                else:
                    functions.draw_image(data.door_top, 217, 17)


        if self.adjacentRooms[1] is not None:
            if self.adjacentRooms[1].itemRoom:
                if closed:
                    functions.draw_image(data.item_door_bot_closed, 217, 225)
                else:
                    functions.draw_image(data.item_door_bot, 217, 225)
            elif self.adjacentRooms[1].bossRoom:
                if closed:
                    functions.draw_image(data.boss_door_bot_closed, 217, 225)
                else:
                    functions.draw_image(data.boss_door_bot, 217, 225)
            else:
                if closed:
                    functions.draw_image(data.door_bot_closed, 217, 225)
                else:
                    functions.draw_image(data.door_bot, 217, 225)

        if self.adjacentRooms[2] is not None:
            if self.adjacentRooms[2].itemRoom:
                if closed:
                    functions.draw_image(data.item_door_left_closed, 25, 113)
                else:
                    functions.draw_image(data.item_door_left, 25, 113)
            elif self.adjacentRooms[2].bossRoom:
                if closed:
                    functions.draw_image(data.boss_door_left_closed, 25, 113)
                else:
                    functions.draw_image(data.boss_door_left, 25, 113)
            else:
                if closed:
                    functions.draw_image(data.door_left_closed, 25, 113)
                else:
                    functions.draw_image(data.door_left, 25, 113)

        if self.adjacentRooms[3] is not None:
            if self.adjacentRooms[3].itemRoom:
                if closed:
                    functions.draw_image(data.item_door_right_closed, 427, 113)
                else:
                    functions.draw_image(data.item_door_right, 427, 113)
            elif self.adjacentRooms[3].bossRoom:
                if closed:
                    functions.draw_image(data.boss_door_right_closed, 427, 113)
                else:
                    functions.draw_image(data.boss_door_right, 427, 113)
            else:
                if closed:
                    functions.draw_image(data.door_right_closed, 427, 113)
                else:
                    functions.draw_image(data.door_right, 427, 113)

        for i in self.obstacles:
            i.draw()

        for i in self.items:
            i.draw()

    # top left box 0 0, 230 46
    # top right box 246 0, 479 46

    # bot left box 0, 226, 230, 271
    # bot right box 246, 226, 479, 271

    # left 1 0 47, 51 129
    # left 2 0 144, 51 226

    # right 1 427 46, 479 128
    # right 2 427 143, 479 225



    #right door 427 128, 479, 143
    #left door 0 129, 51, 144
    #top door 246 46, 230 0
    #bot door 246 271, 230, 226

    def generateWalls(self):
        self.collisionBoxes.append(CollisionBox(0, 0, 220, 46))
        self.collisionBoxes.append(CollisionBox(260, 0, 479, 46))

        self.collisionBoxes.append(CollisionBox(0, 226, 220, 271))
        self.collisionBoxes.append(CollisionBox(260, 226, 479, 271))

        self.collisionBoxes.append(CollisionBox(0, 47, 51, 75))
        self.collisionBoxes.append(CollisionBox(0, 144, 51, 226))

        self.collisionBoxes.append(CollisionBox(427, 46, 479, 75))
        self.collisionBoxes.append(CollisionBox(427, 143, 479, 225))

    def randomizeRoom(self):

        if self.floorX == 7 and self.floorY == 7:
            return

        if self.boss is not None:
            self.obstacles.append(Obstacle(2, 2, 0))
            self.obstacles.append(Obstacle(10, 2, 0))
            return

        r = randint(0, 9)

        if r == 0:
            functions.add_random_enemy(53, 46, self)
            functions.add_random_enemy(398, 46, self)
            functions.add_random_enemy(53, 197, self)
            functions.add_random_enemy(398, 197, self)
            obs = [[1,0], [0,1], [10,0], [11,1], [0,4], [1,5], [11,4], [10,5]]
            for i in obs:
                self.obstacles.append(Obstacle(i[0], i[1], 2))


        if r == 1:
            functions.add_random_enemy(170, 120, self)
            functions.add_random_enemy(290, 120, self)

        if r == 2:
            self.obstacles.append(Obstacle(5, 2, 1))
            self.obstacles.append(Obstacle(6, 2, 1))
            self.obstacles.append(Obstacle(5, 3, 1))
            self.obstacles.append(Obstacle(6, 3, 1))
            self.obstacles.append(Obstacle(7, 2, 1))
            self.obstacles.append(Obstacle(7, 3, 1))

        if r == 3:
            self.obstacles.append(Obstacle(1, 1, 1))
            self.obstacles.append(Obstacle(2, 1, 1))
            self.obstacles.append(Obstacle(3, 1, 1))
            self.obstacles.append(Obstacle(1, 4, 1))
            self.obstacles.append(Obstacle(2, 4, 1))
            self.obstacles.append(Obstacle(3, 4, 1))
            self.obstacles.append(Obstacle(10, 1, 1))
            self.obstacles.append(Obstacle(9, 1, 1))
            self.obstacles.append(Obstacle(8, 1, 1))
            self.obstacles.append(Obstacle(10, 4, 1))
            self.obstacles.append(Obstacle(9, 4, 1))
            self.obstacles.append(Obstacle(8, 4, 1))
            functions.add_random_enemy(320, 120, self)
            functions.add_random_enemy(110, 120, self)

        if r == 4:
            self.obstacles.append(Obstacle(5, 2, 0))
            self.obstacles.append(Obstacle(6, 2, 0))
            self.obstacles.append(Obstacle(3, 3, 0))
            self.obstacles.append(Obstacle(4, 3, 1))
            self.obstacles.append(Obstacle(7, 3, 1))
            self.obstacles.append(Obstacle(8, 3, 1))
            functions.add_random_enemy(204, 140, self)
            functions.add_random_enemy(234, 140, self)
            functions.add_random_enemy(170, 107, self)
            functions.add_random_enemy(264, 107, self)

        if r == 5:
            for y in range(1, 5):
                for x in range(3, 10):
                    self.obstacles.append(Obstacle(x, y, 2))


        if r == 6:
            self.obstacles.append(Obstacle(5, 2, 0))
            self.obstacles.append(Obstacle(6, 2, 0))
            self.obstacles.append(Obstacle(5, 3, 0))
            self.obstacles.append(Obstacle(6, 3, 0))
            functions.add_random_enemy(144, 77, self)
            functions.add_random_enemy(294, 167, self)

        if r == 7:
            functions.add_random_enemy(222, 123, self)

        if r == 8:
            functions.add_random_enemy(53, 46, self)
            functions.add_random_enemy(398, 46, self)
            functions.add_random_enemy(53, 197, self)
            functions.add_random_enemy(398, 197, self)

        if r == 9:
            for x in range(3, 9):
                self.obstacles.append(Obstacle(x, 1, 2))
            for x in range(3, 9):
                self.obstacles.append(Obstacle(x, 3, 2))
            self.obstacles.append(Obstacle(3, 2, 2))
            self.obstacles.append(Obstacle(5, 2, 2))
            self.obstacles.append(Obstacle(6, 2, 2))
            self.obstacles.append(Obstacle(8, 3, 2))
            functions.add_random_enemy(174, 108, self)
            functions.add_random_enemy(264, 108, self)


class Item:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
        self.collisionBox = CollisionBox(self.x, self.y, 24, 24, self)

    def draw(self):
        functions.draw_image(data.items[self.id], self.x, self.y)


class Text:
    def __init__(self, text, description):
        self.timer = 0
        self.lifetime = 135
        self.text = text
        self.description = description

    def tick(self):
        self.timer += 1

        functions.draw_text(self.text, 50, 20, 35, "centered")
        functions.draw_text(self.description, 50, 50, 15, "centered")

        if self.timer > self.lifetime:
            data.currentText = None
            del self
            return

class Hatch:
    def __init__(self, room):
        self.x = 224
        self.y = 90
        self.room = room
        self.floor = room.floor
        self.type = "hatch"
        self.collisionBox = CollisionBox(self.x + 14, self.y + 16, 1, 1, self)

    def draw(self):
        functions.draw_image(data.hatch, self.x, self.y)

    def tick(self):
        self.draw()
        if functions.box_collision2(self.collisionBox, data.player.collisionBox):
            functions.go_next_floor()


class Fade:
    def __init__(self, type="in"):
        self.timer = 0
        self.timerLimit = 200
        self.fade_value = 0
        self.type = type
        if self.type == "out":
            self.fade_value = 255
        data.currentQuote = data.quotes[randint(0, len(data.quotes) - 1)]

    def tick(self):
        transparent_screen = pygame.Surface((data.screen.get_width(), data.screen.get_height()), pygame.SRCALPHA)
        transparent_screen.fill((0, 0, 0, self.fade_value))
        data.screen.blit(transparent_screen, (0,0))
        if self.type == "in":
            self.fade_value += 4
        else:
            self.fade_value -= 4

        if self.fade_value >= 255 or self.fade_value < 0:
            data.currentFade = None
            del self
            return

class Animation:
    def __init__(self, owner, image, framesCount, speed, flip = False, offsetX = 0, offsetY = 0):
        self.owner = owner
        self.timer = 0
        self.image = image
        self.frame = 0
        self.framesCount = framesCount
        self.speed = speed
        self.frames = []
        self.flip = flip
        self.offsetX = offsetX
        self.offsetY = offsetY

        for i in range(0, framesCount):
            self.frames.append(self.image.subsurface(i * self.image.get_width() / self.framesCount, 0, self.image.get_width() / self.framesCount, self.image.get_height()))

    def draw(self):
        functions.draw_image(pygame.transform.flip(self.frames[self.frame], self.flip, False), self.owner.x + self.offsetX, self.owner.y + self.offsetY)


    def tick(self):
        self.timer += self.speed
        if self.timer >= 100:
            self.frame += 1
            self.timer = 0
            if self.frame >= self.framesCount:
                self.frame = 0
        self.draw()

class Sprite:
    def __init__(self, x, y, room, image, lifetime=1, owner=None, owner_offset_x = 0, owner_offset_y = 0):
        self.x = x
        self.y = y
        self.room = room
        self.image = image
        self.lifetime = lifetime
        self.timer = 0
        self.owner = owner
        self.type = "sprite"
        self.owner_offset_x = owner_offset_x
        self.owner_offset_y = owner_offset_y

    def tick(self):
        self.timer += 1
        if self.timer >= self.lifetime * 60:
            data.gameObjects.remove(self)
            del self
            return

        self.draw()

    def draw(self):
        if self.room == data.player.room:
            if self.owner is None:
                functions.draw_image(self.image, self.x, self.y)
            else:
                functions.draw_image(self.image, self.owner.x + self.owner_offset_x, self.owner.y + self.owner_offset_y)
