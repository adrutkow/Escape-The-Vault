import functions
import data
import pygame
import classes
from random import randint


print("DONE LOADING")

def main():
    functions.events()


    if data.music_channel.get_busy() == False:

        if data.Scene == 0:
            data.music_channel.play(data.main_menu_music)

        if data.Scene == 1:
            if data.player.floorCount == 0:
                data.music_channel.play(data.music_level_1)
            if data.player.floorCount == 1:
                data.music_channel.play(data.music_level_2)
            if data.player.floorCount == 2:
                data.music_channel.play(data.music_level_3)
            if data.player.floorCount == 3:
                data.music_channel.play(data.music_level_4)
            if data.player.floorCount == 4:
                data.music_channel.play(data.music_level_5)
            #if data.player.floorCount == 0:
            #    data.music_channel.play(data.music_level_1)


    if data.Scene == 3:
        e = pygame.event.wait()
        if e.type == pygame.KEYDOWN:
            data.Scene = 0
            return


    if data.Scene == 4:
        e = pygame.event.wait()
        if e.type == pygame.KEYDOWN:
            data.Scene = 0


    if data.Scene == 0:
        functions.main_menu()

    if data.Scene == 2:
        if data.currentFade is None:
            #data.currentQuote = data.quotes[randint(0, len(data.quotes)-1)]
            functions.draw_text(data.currentQuote, 240, 140, 8, "centered")
        data.pregame_timer += 1
        if data.pregame_timer >= data.pregame_timer_max:
            data.pregame_timer = 0
            data.Scene = 1
            data.currentFade = classes.Fade("out")


    if data.Scene == 1:

        # if data.music_channel.get_sound() != data.music_level_1 and data.player.room.boss is None:
        #     data.music_channel.stop()
        if data.player.room.boss is not None and data.music_channel.get_sound() != data.boss_music:
            data.music_channel.stop()
            data.music_channel.play(data.boss_music)




        data.player.room.draw()


        for i in data.gameObjects:
            if i.room == data.player.room:
                i.tick()

        if data.currentText is not None:
            data.currentText.tick()

        functions.draw_hud()



    if data.currentFade is not None:
        data.currentFade.tick()


    if data.Scene == 3:
        functions.draw_image(data.death_screen, 52, 35)

    data.clock.tick(60)
    pygame.display.update()


while True:
    main()