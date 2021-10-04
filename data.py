import pygame
import classes

pygame.mixer.init()
music_channel = pygame.mixer.Channel(1)

icon = pygame.image.load("files/enemies/golden_ajeaje.png")
pygame.display.set_icon(icon)

Scene = 0
# 0 - main menu
# 1 - game


#slots:
# 0 -> 10 : empty space
# 11: money

currentFade = None
currentQuote = None
pregame_timer = 0
pregame_timer_max = 200
defaultX = 480
defaultY = 272
screen = pygame.display.set_mode((480, 272), pygame.RESIZABLE)


pygame.display.set_caption("Escape The Vault V1.0")

clock = pygame.time.Clock()
obstacles = []
currentText = None

items_left = []

loading_image = pygame.image.load("files/misc/loading_screen.png")

scaleX = screen.get_width() / defaultX
scaleY = screen.get_height() / defaultY
screen.blit(pygame.transform.scale(loading_image, (int(defaultX * scaleX), int(defaultY * scaleY))), (0, 0))
pygame.display.update()

head_png = pygame.image.load("files/player/head.png")
body_forward_png = pygame.image.load("files/player/body_forward.png")
body_side_png = pygame.image.load("files/player/body_side.png")

menu_screen = pygame.image.load("files/misc/menu_screen.png")
death_screen = pygame.image.load("files/misc/death_screen.png")

pygame.font.init()

top = pygame.image.load("files/map/top.png")
bot = pygame.image.load("files/map/bot.png")
left = pygame.image.load("files/map/left.png")
right = pygame.image.load("files/map/right.png")

electrocute_png = pygame.image.load("files/misc/electrocute.png")
harvest_png = pygame.image.load("files/misc/harvest.png")
conqueror_png = pygame.image.load("files/misc/conqueror.png")
tempo_png = pygame.image.load("files/misc/tempo.png")

map_empty = pygame.image.load("files/misc/map_empty.png")
map_item = pygame.image.load("files/misc/map_item.png")
map_boss = pygame.image.load("files/misc/map_boss.png")

electrocute_sound = pygame.mixer.Sound("files/sounds/electrocute.mp3")
harvest_sound = pygame.mixer.Sound("files/sounds/dark_harvest.mp3")
conqueror_sound = pygame.mixer.Sound("files/sounds/conqueror.mp3")
tempo_sound = pygame.mixer.Sound("files/sounds/lethal_tempo.mp3")
grasp_sound = pygame.mixer.Sound("files/sounds/grasp.mp3")

boss_angry = pygame.mixer.Sound("files/sounds/boss_angry.mp3")

boss_salt = pygame.image.load("files/bosses/boss_salt.png")
boss_salt2 = pygame.image.load("files/bosses/boss_salt_2.png")
boss_spood = pygame.image.load("files/bosses/boss_spood.png")
boss_speed = pygame.image.load("files/bosses/boss_speed.png")
boss_glebu = pygame.image.load("files/bosses/boss_glebu.png")
boss_cat = pygame.image.load("files/bosses/boss_cat.png")



boss_salt_death = pygame.mixer.Sound("files/sounds/salt_boss_death.mp3")
#boss_glebu_death = pygame.mixer.Sound("files/sounds/glebu_death.mp3")
#aboss_glebu_angry = pygame.mixer.Sound("files/sounds/glebu_angry.mp3")

heart = pygame.image.load("files/misc/heart.png")
half_heart = pygame.image.load("files/misc/half_heart.png")

glass_break_sound = pygame.mixer.Sound("files/sounds/glass_break.mp3")
hit_marker_sound = pygame.mixer.Sound("files/sounds/hit_marker.mp3")
item_pickup_sound = pygame.mixer.Sound("files/sounds/item_pickup.mp3")
player_hit_sound = pygame.mixer.Sound("files/sounds/player_hit.mp3")

main_menu_music = pygame.mixer.Sound("files/sounds/main_menu.mp3")
music_level_1 = pygame.mixer.Sound("files/sounds/music_level_1.mp3")
music_level_2 = pygame.mixer.Sound("files/sounds/music_level_2.mp3")
music_level_3 = pygame.mixer.Sound("files/sounds/music_level_3.mp3")
music_level_4 = pygame.mixer.Sound("files/sounds/music_level_4.mp3")
music_level_5 = pygame.mixer.Sound("files/sounds/music_level_5.mp3")
boss_music = pygame.mixer.Sound("files/sounds/boss_music.mp3")

obstacles.append(pygame.image.load("files/obstacles/obstacle_0.png"))
obstacles.append(pygame.image.load("files/obstacles/obstacle_1.png"))
obstacles.append(pygame.image.load("files/obstacles/obstacle_2.png"))

item_count = 100
available_items = 28

items_png = pygame.image.load("files/items/items_png.png")

door_top = pygame.image.load("files/map/door_top.png")
door_bot = pygame.image.load("files/map/door_bot.png")
door_left = pygame.image.load("files/map/door_left.png")
door_right = pygame.image.load("files/map/door_right.png")

door_top_closed = pygame.image.load("files/map/door_top_closed.png")
door_bot_closed = pygame.image.load("files/map/door_bot_closed.png")
door_left_closed = pygame.image.load("files/map/door_left_closed.png")
door_right_closed = pygame.image.load("files/map/door_right_closed.png")

item_door_top = pygame.image.load("files/map/item_door_top.png")
item_door_bot = pygame.image.load("files/map/item_door_bot.png")
item_door_left = pygame.image.load("files/map/item_door_left.png")
item_door_right = pygame.image.load("files/map/item_door_right.png")

item_door_top_closed = pygame.image.load("files/map/item_door_top_closed.png")
item_door_bot_closed = pygame.image.load("files/map/item_door_bot_closed.png")
item_door_left_closed = pygame.image.load("files/map/item_door_left_closed.png")
item_door_right_closed = pygame.image.load("files/map/item_door_right_closed.png")

boss_door_top = pygame.image.load("files/map/boss_door_top.png")
boss_door_bot = pygame.image.load("files/map/boss_door_bot.png")
boss_door_left = pygame.image.load("files/map/boss_door_left.png")
boss_door_right = pygame.image.load("files/map/boss_door_right.png")

boss_door_top_closed = pygame.image.load("files/map/boss_door_top_closed.png")
boss_door_bot_closed = pygame.image.load("files/map/boss_door_bot_closed.png")
boss_door_left_closed = pygame.image.load("files/map/boss_door_left_closed.png")
boss_door_right_closed = pygame.image.load("files/map/boss_door_right_closed.png")

hatch = pygame.image.load("files/map/hatch.png")

floor = pygame.image.load("files/map/map.png")

tear = pygame.image.load("files/projectiles/tear.png")
enemy_tear = pygame.image.load("files/projectiles/enemy_tear.png")

win_screen = pygame.image.load("files/misc/winning_screen.png")

come = pygame.image.load("files/projectiles/come.png")

movementKeyDown = False

body_offsetX = 5
body_offsetY = 21

projectile_offsetX = 14
projectile_offsetY = 19

gameObjects = []

global player
player = classes.Player()

enemy_count = 9

enemy_health = [6, 7, 5, 6, 8, 8, 5, 6, 6, 6]
enemy_attackspeed = [1, 1.5, 1, 0.8, 1, 0.5, 2, 2, 1, 1]

enemy_png = []
head = []
body_forward = []
body_side = []
items = []

for i in range(0, 7):
    head.append(head_png.subsurface((i * head_png.get_width() / 8, 0, head_png.get_width() / 8, head_png.get_height())))

for i in range(0, 9):
    body_forward.append(body_forward_png.subsurface(
        (i * body_forward_png.get_width() / 10, 0, body_forward_png.get_width() / 10, body_forward_png.get_height())))

for i in range(0, 9):
    body_side.append(body_side_png.subsurface(
        (i * body_side_png.get_width() / 10, 0, body_side_png.get_width() / 10, body_side_png.get_height())))

for i in range(0, item_count):
    items.append(items_png.subsurface((i % 10) * 24, (int(i / 10)) * 24, 24, 24))

for i in range(0, enemy_count):
    enemy_png.append(pygame.image.load("files/enemies/enemy_" + str(i) + ".png"))
enemy_png.append((pygame.image.load("files/enemies/golden_ajeaje.png")))




    # screen.blit(pygame.transform.scale(body_side[i], (int(body_side[i].get_width() * scaleX), int(body_side[i].get_height() * scaleY))), (i * 40 * scaleX, y * scaleY))

quotes = ["Help us",
          "He promised greatness",
          "I want to be free",
          "The pain",
          "The arrows",
          "There is no escape",
          "There's no hope",
          "There's no point",
          "It's too late",
          "Don't even try",
          "Can't let it happen again",
          "Anything to not experience it again",
          "Merciless",
          "Why?"]

boss_names = ["Natural Salt", "Spood", "DubstepCatOwO", "Speed", "Glebu"]

item_names = ["Berserker's Greaves",
              "Boots of swiftness",
              "Statikk shiv",
              "Bloodedge's blessing",
              "Doran's blade",
              "Runaan's hurricane",
              "Infinity edge",
              "Guinsoo's rageblade",
              "Rylai's scepter",
              "Rod of ages",
              "Paprika chips",
              "Hextech Gunblade",
              "Kingdom Come",
              "Electrocute",
              "Dark Harvest",
              "Conqueror",
              "Lethal Tempo",
              "Grasp of the Undying",
              "Wit's end",
              "Rapid Fire Cannon",
              "Warmog's armor",
              "Thornmail",
              "Spirit visage",
              "Black cleaver",
              "Rabadon's Deathcap",
              "Essence reaver",
              "Pickaxe",
              "Guardian angel",
              "Broken sunglasses"]

item_descriptions = ["movement and attack speed up",
                     "movement speed up",
                     "cats love it",
                     "you are worthy enough",
                     "slight damage up",
                     "everything is black",
                     "damage and crit up",
                     "attack speed up",
                     "slow them down",
                     "hp and damage up",
                     "most nutritious meal",
                     "damage up",
                     "This is my come",
                     "lightning in your hands",
                     "harvest their souls",
                     "conquer",
                     "not enough attack speed",
                     "grow stronger",
                     "attack speed up",
                     "projectile and attack speed up",
                     "no it doesn't regen hp",
                     "damage attackers",
                     "healing amplified",
                     "damage and hp up",
                     "double damage",
                     "damage and crit up",
                     "damage up",
                     "Cheat death",
                     "Maybe there's hope?"]

# ANIMATIONS
# ID
# 0 - body side right
# 1 - body side flip
# 2 - body forward
animations = []
# test = 2
#
# temp = pygame.image.load("files/player/body_side.png")
# animations.append(classes.Animation(player, temp, 10, 50, False, body_offsetX, body_offsetY))
# animations.append(classes.Animation(player, temp, 10, 50, True, body_offsetX, body_offsetY))
# temp = pygame.image.load("files/player/body_forward.png")
# animations.append(classes.Animation(player, temp, 10, 50, False, body_offsetX, body_offsetY))
