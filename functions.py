import math
from random import randint
import pygame
import data
import classes
import os
import json


def initialize():
    data.player = classes.Player()
    data.gameObjects.append(data.player)
    for i in range(0, data.available_items):
        data.items_left.append(i)
    floor = classes.Floor()
    floor.randomizeFloor()
    data.player.room = floor.layout[7][7]
    data.player.floor = floor

    data.animations = []

    temp = pygame.image.load("files/player/body_side.png")
    data.animations.append(classes.Animation(data.player, temp, 10, 50, False, data.body_offsetX, data.body_offsetY))
    data.animations.append(classes.Animation(data.player, temp, 10, 50, True, data.body_offsetX, data.body_offsetY))
    temp = pygame.image.load("files/player/body_forward.png")
    data.animations.append(classes.Animation(data.player, temp, 10, 50, False, data.body_offsetX, data.body_offsetY))


def draw_image(image, x, y):
    scaleX = data.screen.get_width() / data.defaultX
    scaleY = data.screen.get_height() / data.defaultY
    data.screen.blit(pygame.transform.scale(image, (int(image.get_width() * scaleX), int(image.get_height() * scaleY))), (x * scaleX, y * scaleY))

def add_random_enemy(x, y, room):
    enemy_id = randint(0, data.enemy_count - 1)
    random = randint(0, 20)
    if random == 0:
        enemy_id = 9
    data.gameObjects.append(classes.Enemy(x, y, room, enemy_id))
    return

def draw_text(text, x, y, size, mode="normal"):


    font = pygame.font.Font("files/IsaacGame.ttf", size)


    temp = font.render(text, False, (0, 0, 0))

    if mode == "normal":
        draw_image(temp, x+3, y+3)
    elif mode == "centered":
        #scaleX = data.screen.get_width() / data.defaultX
        #draw_image(temp, data.screen.get_width() / 2 - (temp.get_rect()[2] * scaleX) / 2, y)

        scaleX = data.screen.get_width() / data.defaultX
        scaleY = data.screen.get_height() / data.defaultY
        data.screen.blit(
            pygame.transform.scale(temp, (int(temp.get_width() * scaleX), int(temp.get_height() * scaleY))),
            (data.screen.get_width()/2 - (temp.get_width() - 3) * scaleX / 2, (y+3) * scaleY))



    temp = font.render(text, False, (255, 255, 255))
    if mode == "normal":
        draw_image(temp, x, y)
    elif mode == "centered":
        #scaleX = data.screen.get_width() / data.defaultX
        #draw_image(temp, data.screen.get_width() / 2 - (temp.get_rect()[2] * scaleX) / 2, y)

        scaleX = data.screen.get_width() / data.defaultX
        scaleY = data.screen.get_height() / data.defaultY
        data.screen.blit(
            pygame.transform.scale(temp, (int(temp.get_width() * scaleX), int(temp.get_height() * scaleY))),
            (data.screen.get_width()/2 - temp.get_width() * scaleX / 2, y * scaleY))







    #data.screen.blit(font.render(text, True, (255,0,0)), (x,y))

def get_angle(x, y, x2, y2):
    return math.atan2(y2 - y, x2 - x)

def get_item_id():

    if len(data.items_left) <= 0:
        print("ran out of items")
        for i in range(0, data.available_items):
            data.items_left.append(i)


    r = randint(0, len(data.items_left)-1)
    id = data.items_left[r]
    data.items_left.remove(id)
    return id


#door top 217 17

#door bot 217 225

#door left 25 113

#door right 427 113


def isSlotOccupied(floor, room, direction):
    if room.floorX + direction[0] < 0 or room.floorX + direction[0] > 14 or room.floorY + direction[1] < 0 or room.floorY + direction[1] > 14:
        return True
    if floor.layout[room.floorY + direction[1]][room.floorX + direction[0]] is not None:
        return True
    return False

def leavingRoom(room):
    for i in data.gameObjects:
        if i.type == "projectile":
            data.gameObjects.remove(i)
            del i


def drawBox(box):
    pygame.draw.rect(data.screen, (255,0,0), (box.x, box.y, box.w, box.h))

def are_enemies_in_room(room):
    if room.boss is not None:
        return True
    for i in data.gameObjects:
        if i.type == "enemy" and i.room == room:
            return True
    return False

def draw_map():
    # draw_image(data.top, 0, 0)
    # draw_image(data.bot, 0, 216)
    # draw_image(data.left, 0, 56)
    # draw_image(data.right, 387, 56)
    # draw_image(data.floor, 91, 56)
    draw_image(data.floor, 0, 0)


def box_collision(x1, y1, w1, h1, x2, y2, w2, h2):
    return (x1 + w1 >= x2 and x1 <= x2 + w2 and y1 + h1 >= y2 and y1 <= y2 + h2)


def box_collision2(box1, box2):
    return box_collision(box1.x, box1.y, box1.w, box1.h, box2.x, box2.y, box2.w, box2.h)


def damage(attacker, victim, bonus = 1):
    bonus_damage = 0

    if "conqueror" in data.player.effects:
        bonus_damage += data.player.conquerorStacks * 0.25

    if victim == data.player and data.player.invincibility == True:
        return
    if victim is not data.player:
        victim.health -= (attacker.damage + bonus_damage) * bonus
        if victim.health <= 0 and "bloodedge" in data.player.effects:
            data.player.damage += 0.10
    if victim == data.player:
        data.player.invincibility = True
        data.player_hit_sound.play()
        data.player.health -= 0.5


def testPosition(player, x, y):
    for i in player.room.collisionBoxes:
        if box_collision(player.collisionBox.x + x, player.collisionBox.y + y, player.collisionBox.w, player.collisionBox.h,
                                   i.x, i.y, i.w, i.h):
            return True

    for i in player.room.doorCollisionBoxes:
        if box_collision(player.collisionBox.x + x, player.collisionBox.y + y, player.collisionBox.w, player.collisionBox.h,
                                   i.x, i.y, i.w, i.h):
            return True

    for i in player.room.obstacles:
        if box_collision(player.collisionBox.x + x, player.collisionBox.y + y, player.collisionBox.w,
                         player.collisionBox.h,
                         i.collisionBox.x, i.collisionBox.y, i.collisionBox.w, i.collisionBox.h):
            return True
    return False

def add_wall(room, direction):
    if direction == [1,0]:
        room.collisionBoxes.append(classes.CollisionBox(427,128, 52, 15))
    if direction == [-1,0]:
        room.collisionBoxes.append(classes.CollisionBox(0, 129, 51, 15))
    if direction == [0,1]:
        room.collisionBoxes.append(classes.CollisionBox(230, 226, 16, 45))
    if direction == [0,-1]:
        room.collisionBoxes.append(classes.CollisionBox(230, 0, 16, 46))


def add_door_wall(room, direction):
    if direction == [1,0]:
        room.doorCollisionBoxes.append(classes.CollisionBox(427,128, 52, 15))
    if direction == [-1,0]:
        room.doorCollisionBoxes.append(classes.CollisionBox(0, 129, 51, 15))
    if direction == [0,1]:
        room.doorCollisionBoxes.append(classes.CollisionBox(230, 226, 16, 45))
    if direction == [0,-1]:
        room.doorCollisionBoxes.append(classes.CollisionBox(230, 0, 16, 46))

def events():
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
        if e.type == pygame.VIDEORESIZE:
            pass
        if e.type == pygame.KEYDOWN:

            if e.key == pygame.K_f:
                #pygame.display.set_mode((data.screen.get_width(), data.screen.get_height()), pygame.NOFRAME)
                pass

            if e.key == pygame.K_1:
                for y in range(0,15):
                    string = ""
                    for x in range(0,15):
                        if data.player.room == data.player.floor.layout[y][x]:
                            string += "P "
                        elif data.player.floor.layout[y][x] == None:
                            string += "  "
                        else:
                            string += "X "
                    print(string)

                for y in range(0,15):
                    for x in range(0,15):
                        if data.player.floor.layout[y][x] is not None:
                            if data.player.floor.layout[y][x].boss is not None:
                                data.player.room = data.player.floor.layout[y][x]


            #data.movementKeyDown = e.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
            #print(data.body_offsetX, data.body_offsetY)


def pickupItem(player, item):

    if item.id == 28:

        if data.player.health == data.player.maxHealth:
            return


        data.player.health += 1
        if "visage" in data.player.effects:
            data.player.health += 1


        if data.player.health > data.player.maxHealth:
            data.player.health = data.player.maxHealth

        player.room.items.remove(item)
        return





    data.item_pickup_sound.play()

    if item.id == 0:
        player.attackSpeed += 0.3
        player.speed += 0.3

    if item.id == 1:
        player.speed += 0.5

    if item.id == 2:
        player.effects.append("statikk")

    if item.id == 3:
        player.effects.append("bloodedge")

    if item.id == 4:
        player.damage += 0.25

    if item.id == 5:
        player.effects.append("runaan")

    if item.id == 6:
        player.damage += 0.75
        player.critChance += 15

    if item.id == 7:
        player.attackSpeed += 0.3

    if item.id == 8:
        player.damage += 0.5
        player.effects.append("rylai")

    if item.id == 9:
        player.maxHealth += 1
        player.health += 1
        player.damage += 0.25

    if item.id == 10:
        player.maxHealth += 1.5
        player.health += 1.5

    if item.id == 11:
        player.damage += 0.5

    if item.id == 12:
        player.effects.append("come")

    if item.id == 13:
        player.effects.append("electrocute")

    if item.id == 14:
        player.effects.append("harvest")

    if item.id == 15:
        player.effects.append("conqueror")

    if item.id == 16:
        player.effects.append("tempo")

    if item.id == 17:
        player.effects.append("grasp")

    if item.id == 18:
        player.attackSpeed += 0.3

    if item.id == 19:
        player.attackSpeed += 0.3
        player.critChance += 10
        player.projectileSpeed += 1

    if item.id == 20:
        player.maxHealth += 2
        player.health += 2

    if item.id == 21:
        player.maxHealth += 1
        player.health += 1
        player.effects.append("thornmail")

    if item.id == 22:
        player.maxHealth += 1
        player.health += 1
        player.effects.append("visage")

    if item.id == 23:
        player.maxHealth += 1
        player.damage += 0.5

    if item.id == 24:
        player.damage *= 2

    if item.id == 25:
        player.damage += 0.75
        player.critChance += 20

    if item.id == 26:
        player.damage += 0.5

    if item.id == 27:
        player.maxHealth += 1
        player.health += 1



    data.currentText = classes.Text(data.item_names[item.id], data.item_descriptions[item.id])

    player.currentItems.append(item.id)
    player.room.items.remove(item)
    del item


def draw_hud():
    scaleX = data.screen.get_width() / data.defaultX
    scaleY = data.screen.get_height() / data.defaultY

    for i in range(0, int(data.player.health)):
        draw_image(data.heart, 2+i*11, 2)
    if data.player.health != int(data.player.health):
        draw_image(data.half_heart, int(data.player.health*11)-3, 2)

    if data.player.room.boss is not None:
        pygame.draw.rect(data.screen, (0,0,0), (118*scaleX, 29*scaleY, 240*scaleX, 12*scaleY))


        if data.player.room.boss.health > 0:
            percentage = data.player.room.boss.health / data.player.room.boss.maxHealth
        else:
            percentage = 0

        data.screen.fill((255, 0, 0), (119*scaleX, 30*scaleY, 239*percentage*scaleX, 11*scaleY))

        draw_text(data.boss_names[data.player.room.boss.id], 240, 10, 15, "centered")

    #pygame.draw.rect(data.screen, (255, 0, 0), (386*scaleX, 2*scaleY, 92*scaleX, 92*scaleY))
    for y in range(0, 15):
        for x in range(0, 15):
            #pygame.draw.rect(data.screen, (255, 0, 0), ((388 + (6*x)) * scaleX, (4 + (6*y)) * scaleY, 5*scaleX, 5*scaleY))
            if data.player.floor.layout[y][x] is not None:
                if data.player.floor.layout[y][x].visited:
                    #pygame.draw.rect(data.screen, (255, 0, 0),
                                     #((388 + (6 * x)) * scaleX, (4 + (6 * y)) * scaleY, 5 * scaleX, 5 * scaleY))
                    draw_image(data.map_empty, 388 + (6 * x), (4 + (6 * y)))

                    if data.player.floor.layout[y][x].bossRoom:
                        #pygame.draw.rect(data.screen, (0, 0, 255),
                                         #((388 + (6 * x)) * scaleX, (4 + (6 * y)) * scaleY, 5 * scaleX, 5 * scaleY))
                        draw_image(data.map_boss, 388 + (6 * x), (4 + (6 * y)))

                    if data.player.floor.layout[y][x].itemRoom:
                        draw_image(data.map_item, 388 + (6 * x), (4 + (6 * y)))

                    if data.player.room == data.player.floor.layout[y][x]:
                        pygame.draw.rect(data.screen, (0, 255, 0),
                                         ((389 + (6 * x)) * scaleX, (3 + (6 * y)) * scaleY, 5 * scaleX, 5 * scaleY))


                elif data.player.floor.layout[y][x].vision:
                    pygame.draw.rect(data.screen, (0, 0, 0),
                                     ((388 + (6 * x)) * scaleX, (4 + (6 * y)) * scaleY, 5 * scaleX, 5 * scaleY), 1)
                    if data.player.floor.layout[y][x].itemRoom:
                        pygame.draw.rect(data.screen, (255, 216, 0),
                                     ((388 + (6 * x)) * scaleX, (4 + (6 * y)) * scaleY, 5 * scaleX, 5 * scaleY), 1)
                    if data.player.floor.layout[y][x].bossRoom:
                        pygame.draw.rect(data.screen, (255, 0, 0),
                                     ((388 + (6 * x)) * scaleX, (4 + (6 * y)) * scaleY, 5 * scaleX, 5 * scaleY), 1)




def go_next_floor():
    data.player.floorCount += 1

    if data.player.floorCount == 5:
        data.Scene = 4
        draw_image(data.win_screen, 0, 0)
        data.currentFade = classes.Fade()
        data.music_channel.stop()
        return


    data.player.floor = classes.Floor()
    data.player.floor.randomizeFloor()
    data.player.room = data.player.floor.layout[7][7]
    data.player.x = 240
    data.player.y = 136
    data.music_channel.stop()
    data.currentFade = classes.Fade()
    data.Scene = 2


def do_fade():
    data.currentFade = classes.Fade()


def main_menu():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        data.Scene = 2
        do_fade()
        initialize()
        data.music_channel.stop()
    draw_image(data.menu_screen, 0, 0)


def get_json_data(slot):
    jsonFile = open("files/misc/data.json", "r")
    temp = json.load(jsonFile)
    jsonFile.close()
    return temp[str(slot)]

def write_data(slot, temp_data):
    jsonFile = open("data.json", "r")
    temp = json.load(jsonFile)
    jsonFile.close()

    temp[str(slot)] = temp_data

    jsonFile = open("data.json", "w+")
    jsonFile.write(json.dumps(temp))
    jsonFile.close()