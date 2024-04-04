
import pygame as pg
from config import *
import os

pg.init()
pg.mixer.init()
pg.font.init()

class Song:
    def __init__(self, rect, color, outlinecolor, text, textcolor, textpos, font):
        self.rect:pg.Rect = rect
        self.color = color
        self.origcolor = color
        self.outlinecolor = outlinecolor

        self.text = text
        self.textcolor = textcolor
        self.textpos = textpos
        self.font = font


class App:
    def __init__(self):
        self.screen = pg.display.set_mode((SCREEN_W, SCREEN_H))
        self.songs = os.listdir("songs")
        self.songso:list | Song = []
        self.font = pg.font.Font(None, 20)
        self.playing = False
        self.playingmusicname = ""

        self.scrollY = 0

        ## colors ##

        self.bgc = (25,25,25)
        self.songc = (40,40,40)
        self.songcselected = (10,10,10)
        self.textc = (255,255,255)

        
        self.updsong()
        self.run()

    def draw(self):
        self.screen.fill(self.bgc)

        for song in self.songso:

            pg.draw.rect(self.screen, song.color, song.rect)
            pg.draw.rect(self.screen, song.outlinecolor, song.rect, 2)

            text = song.font.render(song.text, True, song.textcolor)
            self.screen.blit(text, song.textpos)

        pg.display.flip()


    def update(self):
        for song in self.songso:
            if song.rect.collidepoint(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]):
                song.color = self.songcselected
                if pg.mouse.get_pressed()[0] and not self.playing:
                    pg.mixer.music.load(f"songs/{song.text}")
                    pg.mixer.music.play()
                    self.playing = True
                    self.playingmusicname = song.text
                elif pg.mouse.get_pressed()[0] and self.playing:
                    if self.playingmusicname == song.text:
                        self.playing = False
                        pg.mixer.music.stop()
                    else:
                        pg.mixer.music.load(f"songs/{song.text}")
                        self.playing = True
            else:
                song.color = song.origcolor

    def updsong(self):
        y = 5
        self.songso.clear()
        for s in self.songs:
            rect = pg.Rect(0, y, SCREEN_W, SONG_H)
            
            song = Song(rect, self.songc, (0,0,0), s, self.textc, [5,y+5], self.font)

            self.songso.append(song)
            y += SONG_H

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    self.songs = os.listdir("songs")
                    self.updsong()
            if event.type == pg.MOUSEWHEEL:
                if event.y == 1:
                    if self.scrollY > 0:
                        self.scrollY -= 1
                        for s in self.songso:
                            s.rect.y += SONG_H
                            s.textpos[1] += SONG_H
                    
                if event.y == -1:
                    if self.scrollY < len(self.songs)-1:
                        self.scrollY += 1
                        for s in self.songso:
                            s.rect.y -= SONG_H
                            s.textpos[1] -= SONG_H


    def run(self):
        while True:
            self.update()
            self.draw()
            self.event()

if __name__ == "__main__":
    App()