import pygame as py
import numpy as np
import sys
import os, re

import global_var as gb


Folder_animazione = "animations/Senex/idle"
Folder_occhi = "animations/Senex/eyes"

animazione = []
occhi = []

def riempi(percorso):
    FileNames = os.listdir(percorso)

    # Ordino i file e gli appendo ad una lista, in modo che le animazioni siano lineari e ordinate
    FileNames.sort(key=lambda f: int(re.sub('\D', '', f)))
    sorted(FileNames)

    for filename in FileNames:
        if percorso == Folder_animazione:
            immagine = py.image.load(Folder_animazione + "/" + filename).convert_alpha()
            animazione.append(immagine)
            
        if percorso == Folder_occhi:
            immagine = py.image.load(Folder_occhi + "/" + filename).convert_alpha()
            occhi.append(immagine)

riempi(Folder_animazione)
riempi(Folder_occhi)


def get_font(size):
    return py.font.Font("font/font.ttf", size)

class Computer():
    def __init__(self):
        self.x = gb.width/2
        self.y = gb.height/2 - 60 * gb.mult
        
        self.delay_an0 = 0.1
        self.delay_an1 = 0.1
        
        self.image = animazione[0]
        self.image_eye = occhi[2]
        
        self.m = 2
        
        self.sbatti_occhi = False
        
        self.cards = []
        self.scelta = 1
        
    def render(self):
        
        
        if self.delay_an0 > len(animazione):
            self.delay_an0 = 0
            

        self.image = animazione[int(self.delay_an0)]
        self.image = py.transform.scale(self.image, (self.image.get_width() * gb.mult * self.m, self.image.get_height() * gb.mult * self.m))
            
        self.delay_an0 += 0.03
        
        rand = np.random.randint(0, 150)
        if rand == 0:
            self.sbatti_occhi = True
            
        if self.delay_an1 >= len(occhi):
            self.delay_an1 = 0
            self.sbatti_occhi = False
        
        self.image_eye = occhi[int(self.delay_an1)]
        self.image_eye = py.transform.scale(self.image_eye, (self.image_eye.get_width() * gb.mult * self.m, self.image_eye.get_height() * gb.mult * self.m))
        
        if self.sbatti_occhi:
            self.delay_an1 += np.random.randint(1, 8)/10
            
            
        
        gb.screen.blit(self.image, (self.x - self.image.get_width()/2, self.y - self.image.get_height()/2))
        gb.screen.blit(self.image_eye, (self.x - self.image.get_width()/2, self.y - self.image.get_height()/2))

class Player():
    def __init__(self, name):
        
        self.name = name
        self.cards = []
        self.scelta = 3
   
        
class Bancone():
    def __init__(self):
        self.segni = {
            
                        "picche": py.image.load("animations/cards/picche.png").convert_alpha(), 
                        "quadri": py.image.load("animations/cards/quadri.png").convert_alpha(),
                        "fiori": py.image.load("animations/cards/fiori.png").convert_alpha(),
                        "cuori": py.image.load("animations/cards/cuori.png").convert_alpha()
                    }
        
        self.reali = {
                        "re": py.image.load("animations/cards/re.png").convert_alpha(), 
                        "regina": py.image.load("animations/cards/regina.png").convert_alpha(),
                        "fante": py.image.load("animations/cards/fante.png").convert_alpha()
            
                    }
        
        
        self.bancone = py.image.load("assets/bancone.png").convert_alpha()
        
        
        self.image = self.segni["picche"]
        
        self.x = gb.width/2 + 4 * gb.mult
        self.y = gb.height/2 + 10 * gb.mult
        
    def render_desk(self):
        m = 3
        
        immagine = py.transform.scale(self.bancone, (self.bancone.get_width() * gb.mult * m, self.bancone.get_height() * gb.mult * m))
        gb.screen.blit(immagine, (self.x - immagine.get_width()/2, self.y - immagine.get_height()/2))
        
        
        
    def render_cards(self, carta):
        
        immagine = py.transform.scale(self.segni[carta], (self.segni[carta].get_width() * gb.mult, self.segni[carta].get_height() * gb.mult))
        
        gb.screen.blit(immagine, (gb.width/2 - immagine.get_width()/2, gb.height/2 - immagine.get_height()/2))
        
        

class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color, scale):

        if image != None:
            self.image_w, self.image_h = image.get_width()*gb.mult/scale, image.get_height()*gb.mult/scale
            self.image = py.transform.scale(image, (self.image_w, self.image_h))
        else:
            self.image = image

        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

    def changeScale(self, position, value):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.image = py.transform.scale(self.image, (self.image_w * value, self.image_h * value))
            self.x_pos -= value
            self.y_pos -= value
        else:
            self.image = py.transform.scale(self.image, (self.image_w, self.image_h))
            self.x_pos += value
            self.y_pos += value
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))


class Dialoghi():
    def __init__(self, personaggio, descrizione, text_speed):
        self.personaggio = personaggio
        self.full_description = descrizione
        self.descr = descrizione

		
        self.descr = self.descr.split(" ")
        self.descr = " ".join(self.descr)

        
        self.delay = 0

        self.descrizione = ""
        self.descrizione1 = ""
        self.descrizione2 = ""
        self.descrizione3 = ""

        self.r0 = False
        self.r1 = False
        self.r2 = False
        self.r3 = False

        self.value = 64
        self.valore = 0
        self.flag_capo = True

        self.cooldown_interm = 0
        self.interm = 0

        if text_speed == 1:
            self.text_speed = 0.1
        elif text_speed == 2:
            self.text_speed = 0.2
        elif text_speed == 3:
            self.text_speed = 0.25
        elif text_speed == 4:
            self.text_speed = 0.5
        elif text_speed == 5:
            self.text_speed = 1
        else:
            self.text_speed = 0.1

        self.contatore = 0

        self.ritardo = 0

        self.CanIplay_sound = True
        self.play_sound = False
        self.cooldown_suono = 0
        self.MaxCooldwon_suono = 0

        self.descr = [self.descr[i:i+1] for i in range(0, len(self.descr), 1)]
        #print(self.descr)
            
        self.Nome_TEXT = get_font(7*int(gb.mult)).render(self.personaggio, True, "Black")
        self.Nome_RECT = self.Nome_TEXT.get_rect(center=(70*gb.mult, gb.height-10*gb.mult))

        self.vignetta = py.image.load("Dialoghi/Characters/"+self.personaggio+".png").convert_alpha()
        self.vignetta = py.transform.scale(self.vignetta, (self.vignetta.get_width()*gb.mult*2, self.vignetta.get_height()*gb.mult*2))

        self.sfondo = py.image.load("assets/Dialoghi.png").convert_alpha()
        self.sfondo = py.transform.scale(self.sfondo, (self.sfondo.get_width()*gb.mult, self.sfondo.get_height()*gb.mult))

        self.keySound = py.mixer.Sound("suoni/char-sound.wav")
        self.keySound.set_volume(0.04)
        
        self.color = "Black"
        
        self.flag_skippa = True
        self.iFinished = False
        
        self.Nome_TEXT = get_font(7*int(gb.mult)).render(self.personaggio, True, "Black")
        self.Nome_RECT = self.Nome_TEXT.get_rect(center=(70*gb.mult, gb.height-10*gb.mult))

        self.vignetta = py.image.load("Dialoghi/Characters/"+self.personaggio+".png").convert_alpha()
        self.vignetta = py.transform.scale(self.vignetta, (self.vignetta.get_width()*gb.mult*2, self.vignetta.get_height()*gb.mult*2))
        
        self.comp = Computer()
        self.bancone = py.image.load("assets/bancone.png").convert_alpha()
        
        self.val_oggetto_max = 12
        self.val_oggetto = self.val_oggetto_max + 1
        self.flag_sali = True
        self.flag_scendi = False
        
        val = 1.2
        
        if gb.last_card[2] != "":
            self.reale = py.image.load("animations/cards/"+ gb.last_card[2] + ".png").convert_alpha()
            self.reale = py.transform.scale(self.reale, (self.reale.get_width() * gb.mult * val, self.reale.get_height() * gb.mult * val))

        self.ogg = py.image.load("animations/cards/"+gb.last_card[0]+".png").convert_alpha()
        self.ogg = py.transform.scale(self.ogg, (self.ogg.get_width()*gb.mult*val, self.ogg.get_height()*gb.mult*val))
        
        
        self.test_ogg = get_font(4*int(gb.mult)).render(str(gb.last_card[1]), True, "Black")

    def __effetto_testo(self):
            
        self.condition0 = self.contatore < self.value
        self.condition1 = self.contatore >= self.value and self.contatore < self.value * 2
        self.condition2 = self.contatore >= self.value * 2 and self.contatore < self.value * 3
        self.condition3 = self.contatore >= self.value * 3 and self.contatore < self.value * 4
            
        max = not int((self.delay+1)) > len(self.descr)

        valuex, valuey = 70, 50
        distanza_righe = 12.5

        def Condition(event):
            return self.descr[self.value*event-self.valore] != " " and self.descr[self.value*event-self.valore] != "." and (self.contatore >= self.value*event-self.valore and self.contatore < self.value*event)

        def Cerca(event):
            for value in range(len(self.descr)):
                if self.descr[self.value*event-1-value] == " " and self.flag_capo:
                    #print("Trovato buco: ",value)
                    self.flag_capo = False
                    self.valore = value
            

        def ScriviTesto(val):
                
            if val == 1:
                self.descrizione += self.descr[int(round(self.delay, 1))]

                self.Descrizione_TEXT = get_font(4*int(gb.mult)).render(self.descrizione, True, self.color)
                self.Descrizione_RECT = self.Descrizione_TEXT.get_rect(center=(gb.width/2+valuex*gb.mult, gb.height-(valuey)*gb.mult))

                self.r0 = True

            elif val == 2:
                self.descrizione1 += self.descr[int(round(self.delay, 1))]

                self.Descrizione1_TEXT = get_font(4*int(gb.mult)).render(self.descrizione1, True, self.color)
                self.Descrizione1_RECT = self.Descrizione1_TEXT.get_rect(center=(gb.width/2+valuex*gb.mult, gb.height-(valuey-distanza_righe)*gb.mult))

                self.r1 = True
            elif val == 3:
                self.descrizione2 += self.descr[int(round(self.delay, 1))]

                self.Descrizione2_TEXT = get_font(4*int(gb.mult)).render(self.descrizione2, True, self.color)
                self.Descrizione2_RECT = self.Descrizione2_TEXT.get_rect(center=(gb.width/2+valuex*gb.mult, gb.height-(valuey-distanza_righe*2)*gb.mult))

                self.r2 = True
            elif val == 4:
                self.descrizione3 += self.descr[int(round(self.delay, 1))]

                self.Descrizione3_TEXT = get_font(4*int(gb.mult)).render(self.descrizione3, True, self.color)
                self.Descrizione3_RECT = self.Descrizione3_TEXT.get_rect(center=(gb.width/2+valuex*gb.mult, gb.height-(valuey-distanza_righe*3)*gb.mult))

                self.r3 = True

        # vado a confrontare se il delay corisponde ad un numero intero e non decimale e anche se non ha superato il valore massimo della lista

        if int(self.delay+0.1) == round(self.delay, 1) and max and self.ritardo == 0:

            # CoolDown indicato per eseguire il suono		
            if self.MaxCooldwon_suono != 0:
                if self.cooldown_suono >= 0 and self.cooldown_suono <= self.MaxCooldwon_suono:
                    self.cooldown_suono +=1
                    self.play_sound = False
                else:
                    self.play_sound = True
                    self.cooldown_suono = 0
            else:
                self.play_sound = True

            if self.play_sound and self.CanIplay_sound:
                self.keySound.play()

            # Prima riga

            if self.condition0:
                if len(self.descr) >= self.value:
                
                    Cerca(1)

                    if Condition(1):
                        ScriviTesto(2)
                    else:
                        ScriviTesto(1)
                else:
                    ScriviTesto(1)

                self.flag_capo = True

            # Seconda riga
            
            elif self.condition1:
                if len(self.descr) >= self.value*2:
                    
                    Cerca(2)

                    if Condition(2):
                        ScriviTesto(3)
                    else:
                        ScriviTesto(2)
                else:
                    ScriviTesto(2)
                self.flag_capo = True

            # Terza riga

            elif self.condition2:
                if len(self.descr) >= self.value*3:
                    
                    Cerca(3)

                    if Condition(3):
                        ScriviTesto(3)
                    else:
                        ScriviTesto(3)
                else:
                    ScriviTesto(3)
                self.flag_capo = True

            elif self.condition3:
                ScriviTesto(4)

            self.contatore += 1

        # Delay aggiuntivo per dei caratteri particolari indicati
        if max and self.descr[int(round(self.delay, 1))] != "." and self.descr[int(round(self.delay, 1))] != "?" and self.descr[int(round(self.delay, 1))] != "!" or self.ritardo == 1:
            self.delay += self.text_speed / gb.Delta_Time
            self.ritardo = 0
        else:
            self.ritardo += self.text_speed / gb.Delta_Time


        if self.contatore >= len(self.full_description):
            self.iFinished = True
            self.flag_skippa = False

    
    def __object_animation(self):
    
        if int(self.val_oggetto) <= -self.val_oggetto_max:
            self.flag_sali = False
            self.flag_scendi = True

        elif int(self.val_oggetto) >= self.val_oggetto_max:
            self.flag_sali = True
            self.flag_scendi = False

        if self.flag_scendi:
            self.flag_sali = False
            self.val_oggetto += 0.1 * gb.mult

        elif self.flag_sali:
            self.flag_scendi = False
            self.val_oggetto -= 0.1 * gb.mult
        #print("Delay: "+str(round(self.delay, 1))+" | Intero: "+str(int(self.delay+0.1))+" | Lunghezza: "+str(len(self.descr))+" | Contatore: "+str(self.contatore)+" | Max: "+str((self.delay+1)))

    def stampa(self):

        clock = py.time.Clock()
        
        possoIniziare = False

        while not possoIniziare:
            
            self.__effetto_testo()
            
            gb.screen.fill(gb.bg_color)
            
            self.__object_animation()
            
            gb.screen.blit(gb.punteggioP_testo, gb.punteggioP_rect)
            
            if gb.flag_pc:
                gb.screen.blit(gb.punteggioC_testo, gb.punteggioC_rect)
            
            if "picche" in gb.last_card[0] or "fiori" in gb.last_card[0]:
                colore = "Black"
            else:
                colore = "Red"
                
            self.test_ogg = get_font(4*int(gb.mult)).render(str(gb.last_card[1]), True, colore)
            
            rett = self.test_ogg.get_rect(center=(self.test_ogg.get_width()/2 + (83 * gb.mult)/2, self.val_oggetto + 89 * gb.mult))
            
            pos_ogg = (20 * gb.mult, gb.height/2 - self.ogg.get_height()/2 + self.val_oggetto - 28 * gb.mult)
            gb.screen.blit(self.ogg, pos_ogg)
            gb.screen.blit(self.test_ogg, (rett[0], rett[1]))
            
            if gb.last_card[2] != "" and gb.last_card[1] == 10:
                gb.screen.blit(self.reale, (pos_ogg[0], pos_ogg[1] - 2 * gb.mult))
            
            self.comp.render()
            
            m = 3
        
            immagine = py.transform.scale(self.bancone, (self.bancone.get_width() * gb.mult * m, self.bancone.get_height() * gb.mult * m))
            gb.screen.blit(immagine, (gb.width/2 + 4 * gb.mult - immagine.get_width()/2, gb.height/2 + 10 * gb.mult- immagine.get_height()/2))

            gb.screen.blit(self.sfondo, (0, gb.height - self.sfondo.get_height()))
            gb.screen.blit(self.vignetta, (42.5*gb.mult, gb.height - self.vignetta.get_height() - 18*gb.mult))
            gb.screen.blit(self.Nome_TEXT, self.Nome_RECT)
            
            if self.r0:
                gb.screen.blit(self.Descrizione_TEXT, self.Descrizione_RECT)

            if self.r1:
                gb.screen.blit(self.Descrizione1_TEXT, self.Descrizione1_RECT)

            if self.r2:
                gb.screen.blit(self.Descrizione2_TEXT, self.Descrizione2_RECT)

            if self.r3:
                gb.screen.blit(self.Descrizione3_TEXT, self.Descrizione3_RECT)

            avanza = Button(image=py.image.load("assets/tasello.png").convert(), pos=(132*gb.mult,  gb.height-12*gb.mult), 
                                text_input="", font=py.font.Font("font/font.ttf", (8*int(gb.mult))), base_color="White", hovering_color="#d7fcd4", scale=1.8)

            if self.interm == 0 or self.cooldown_interm != gb.fps / 10:
                avanza.update(gb.screen)
                self.cooldown_interm += 0.25

            self.interm += 1
            
            if self.interm >= gb.fps and self.cooldown_interm == gb.fps / 10:
                self.interm = 0
                self.cooldown_interm = 0

            for event in py.event.get():

                if event.type == py.QUIT:
                    py.quit()
                    sys.exit()

                    
                if event.type == py.KEYDOWN:
        
                    if event.key == py.K_SPACE or event.key == py.K_RETURN:
        
                        if self.flag_skippa and not self.iFinished:
                            self.__init__(self.personaggio, self.full_description, 5)
                            self.flag_skippa = False
                            self.CanIplay_sound = False
                        
                        elif not self.flag_skippa and self.iFinished:
                            possoIniziare = True
        
                    if event.key == py.K_ESCAPE:
                        py.quit()
                        sys.exit()


            py.display.flip() # ti permette di aggiornare una area dello schermo per evitare lag e fornire piu' ottimizzazione

            clock.tick(gb.fps) # setto i FramesPerSecond


    # risposte (risposta1, risposta2, risposta3)
class Domanda():
    def __init__(self, personaggio, oggetto, descrizione, soluzione, risposte, text_speed):
        self.oggetto = oggetto

        self.personaggio = personaggio
        # self.oggetto = "Narratore"

        self.full_description = descrizione


        self.descr = descrizione.split("\n")
        self.risposte = risposte

        self.number_solution = soluzione - 1
        self.number_selection = 0
        self.number_selected = 0

        self.flag_Tabella = False

        try:

            self.flag_Tabella = True

        except FileNotFoundError:
            pass



        self.soluzione = self.risposte[soluzione-1]
        self.descr = "".join(self.descr)

        self.descr = descrizione.split(" ")	
        for var in range(len(self.descr)):
            if self.descr[var] == "VAR":
                self.descr[var] = gb.scelta_char
        self.descr = " ".join(self.descr)

        self.delay = 0

        self.descrizione = ""
        self.descrizione1 = ""
        self.descrizione2 = ""
        self.descrizione3 = ""

        self.r0 = False
        self.r1 = False
        self.r2 = False
        self.r3 = False

        self.value = 86
        self.valore = 0
        self.flag_capo = True
        self.isFinished = False

        self.cooldown_interm = 0
        self.interm = 0

        if text_speed == 1:
            self.text_speed = 0.1
        elif text_speed == 2:
            self.text_speed = 0.2
        elif text_speed == 3:
            self.text_speed = 0.25
        elif text_speed == 4:
            self.text_speed = 0.5
        elif text_speed == 5:
            self.text_speed = 1
        else:
            self.text_speed = 0.1

        self.contatore = 0

        self.ritardo = 0

        self.CanIplay_sound = True
        self.play_sound = False
        self.cooldown_suono = 0
        self.MaxCooldwon_suono = 0

        self.descr = [self.descr[i:i+1] for i in range(0, len(self.descr), 1)]
        #print(self.descr)

        val = 1.2

        self.ogg = py.image.load("animations/cards/"+self.oggetto+".png").convert_alpha()
        self.ogg = py.transform.scale(self.ogg, (self.ogg.get_width()*gb.mult*val, self.ogg.get_height()*gb.mult*val))

        self.scelte = py.image.load("assets/vignetta-risposta.png").convert_alpha()
        self.scelte = py.transform.scale(self.scelte, (self.scelte.get_width()*gb.mult, self.scelte.get_height()*gb.mult))

        self.sfondo = py.image.load("assets/Dialoghi.png").convert_alpha()
        self.sfondo = py.transform.scale(self.sfondo, (self.sfondo.get_width()*gb.mult, self.sfondo.get_height()*gb.mult))
        
        self.val_oggetto_max = 12
        self.val_oggetto = self.val_oggetto_max + 1
        self.flag_sali = True
        self.flag_scendi = False

        self.risultato = None
        self.suggerimento = False
        self.BeenSuggested = False

        self.suggerimento_sfondo = py.Surface((gb.width, gb.height))
        
        self.keySound = py.mixer.Sound("suoni/char-sound.wav")
        self.keySound.set_volume(0.04)
        
        self.Nome_TEXT = get_font(7*int(gb.mult)).render(self.personaggio, True, "Black")
        self.Nome_RECT = self.Nome_TEXT.get_rect(center=(70*gb.mult, gb.height-10*gb.mult))

        self.vignetta = py.image.load("Dialoghi/Characters/"+self.personaggio+".png").convert_alpha()
        self.vignetta = py.transform.scale(self.vignetta, (self.vignetta.get_width()*gb.mult*2, self.vignetta.get_height()*gb.mult*2))
        
        self.comp = Computer()
        self.bancone = py.image.load("assets/bancone.png").convert_alpha()
        
        self.color = "Black"


    def __effetto_testo(self):
            
        self.condition0 = self.contatore < self.value
        self.condition1 = self.contatore >= self.value and self.contatore < self.value * 2
        self.condition2 = self.contatore >= self.value * 2 and self.contatore < self.value * 3
        self.condition3 = self.contatore >= self.value * 3 and self.contatore < self.value * 4
            
        max = not int((self.delay+1)) > len(self.descr)

        valuex, valuey = 45, 55
        distanza_righe = 12.5

        def Condition(event):
            return self.descr[self.value*event-self.valore] != " " and self.descr[self.value*event-self.valore] != "." and (self.contatore >= self.value*event-self.valore and self.contatore < self.value*event)

        def Cerca(event):
            for value in range(len(self.descr)):
                if self.descr[self.value*event-1-value] == " " and self.flag_capo:
                    #print("Trovato buco: ",value)
                    self.flag_capo = False
                    self.valore = value
            

        def ScriviTesto(val):
                
            if val == 1:
                self.descrizione += self.descr[int(round(self.delay, 1))]

                self.Descrizione_TEXT = get_font(4*int(gb.mult)).render(self.descrizione, True, self.color)
                self.Descrizione_RECT = self.Descrizione_TEXT.get_rect(center=(gb.width/2+valuex*gb.mult, gb.height-(valuey)*gb.mult))

                self.r0 = True

            elif val == 2:
                self.descrizione1 += self.descr[int(round(self.delay, 1))]

                self.Descrizione1_TEXT = get_font(4*int(gb.mult)).render(self.descrizione1, True, self.color)
                self.Descrizione1_RECT = self.Descrizione1_TEXT.get_rect(center=(gb.width/2+valuex*gb.mult, gb.height-(valuey-distanza_righe)*gb.mult))

                self.r1 = True
            elif val == 3:
                self.descrizione2 += self.descr[int(round(self.delay, 1))]

                self.Descrizione2_TEXT = get_font(4*int(gb.mult)).render(self.descrizione2, True, self.color)
                self.Descrizione2_RECT = self.Descrizione2_TEXT.get_rect(center=(gb.width/2+valuex*gb.mult, gb.height-(valuey-distanza_righe*2)*gb.mult))

                self.r2 = True
            elif val == 4:
                self.descrizione3 += self.descr[int(round(self.delay, 1))]

                self.Descrizione3_TEXT = get_font(4*int(gb.mult)).render(self.descrizione3, True, self.color)
                self.Descrizione3_RECT = self.Descrizione3_TEXT.get_rect(center=(gb.width/2+valuex*gb.mult, gb.height-(valuey-distanza_righe*3)*gb.mult))

                self.r3 = True


        # vado a confrontare se il delay corisponde ad un numero intero e non decimale e anche se non ha superato il valore massimo della lista

        if int(self.delay+0.1) == round(self.delay, 1) and max and self.ritardo == 0:

            # CoolDown indicato per eseguire il suono		
            if self.MaxCooldwon_suono != 0:
                if self.cooldown_suono >= 0 and self.cooldown_suono <= self.MaxCooldwon_suono:
                    self.cooldown_suono +=1
                    self.play_sound = False
                else:
                    self.play_sound = True
                    self.cooldown_suono = 0
            else:
                self.play_sound = True

            if self.play_sound and self.CanIplay_sound:
                self.keySound.play()

            # Prima riga

            if self.condition0:
                if len(self.descr) >= self.value:
                
                    Cerca(1)

                    if Condition(1):
                        ScriviTesto(2)
                    else:
                        ScriviTesto(1)
                else:
                    ScriviTesto(1)

                self.flag_capo = True

            # Seconda riga
            
            elif self.condition1:
                if len(self.descr) >= self.value*2:
                    
                    Cerca(2)

                    if Condition(2):
                        ScriviTesto(3)
                    else:
                        ScriviTesto(2)
                else:
                    ScriviTesto(2)
                self.flag_capo = True

            # Terza riga

            elif self.condition2:
                if len(self.descr) >= self.value*3:
                    
                    Cerca(3)

                    if Condition(3):
                        ScriviTesto(4)
                    else:
                        ScriviTesto(3)
                else:
                    ScriviTesto(3)
                self.flag_capo = True

            elif self.condition3:
                ScriviTesto(4)

            # contatore che serve a controllare quanti caratteri sono stati inseriti
            self.contatore += 1
            
        # Delay aggiuntivo per dei caratteri particolari indicati
        if max and self.descr[int(round(self.delay, 1))] != "." and self.descr[int(round(self.delay, 1))] != "?" and self.descr[int(round(self.delay, 1))] != "!" or self.ritardo == 1:
            self.delay += self.text_speed / gb.Delta_Time
            self.ritardo = 0
        else:
            self.ritardo += self.text_speed / gb.Delta_Time

    def __object_animation(self):

        if int(self.val_oggetto) <= -self.val_oggetto_max:
            self.flag_sali = False
            self.flag_scendi = True

        elif int(self.val_oggetto) >= self.val_oggetto_max:
            self.flag_sali = True
            self.flag_scendi = False

        if self.flag_scendi:
            self.flag_sali = False
            self.val_oggetto += 0.1 * gb.mult

        elif self.flag_sali:
            self.flag_scendi = False
            self.val_oggetto -= 0.1 * gb.mult


    def stampa(self):

        clock = py.time.Clock()
        
        possoIniziare = False

        while not possoIniziare:
            
            self.__effetto_testo()
            
            gb.screen.fill(gb.bg_color)
            
            gb.screen.blit(gb.punteggioP_testo, gb.punteggioP_rect)
            
            if gb.flag_pc:
                gb.screen.blit(gb.punteggioC_testo, gb.punteggioC_rect)


            self.__object_animation()

            if self.contatore == len(self.descr):
                self.isFinished = True
                
            
            self.comp.render()
            
            m = 3
        
            immagine = py.transform.scale(self.bancone, (self.bancone.get_width() * gb.mult * m, self.bancone.get_height() * gb.mult * m))
            gb.screen.blit(immagine, (gb.width/2 + 4 * gb.mult - immagine.get_width()/2, gb.height/2 + 10 * gb.mult- immagine.get_height()/2))
                
            gb.screen.blit(self.sfondo, (0, gb.height-self.sfondo.get_height()))
            gb.screen.blit(self.vignetta, (42.5*gb.mult, gb.height-self.vignetta.get_height()-18*gb.mult))
            gb.screen.blit(self.Nome_TEXT, self.Nome_RECT)
            gb.screen.blit(self.ogg, (20 * gb.mult, gb.height/2 - self.ogg.get_height()/2 + self.val_oggetto - 28 * gb.mult))
            
            if self.r0:
                gb.screen.blit(self.Descrizione_TEXT, self.Descrizione_RECT)

            if self.r1:
                gb.screen.blit(self.Descrizione1_TEXT, self.Descrizione1_RECT)

            if self.r2:
                gb.screen.blit(self.Descrizione2_TEXT, self.Descrizione2_RECT)

            if self.r3:
                gb.screen.blit(self.Descrizione3_TEXT, self.Descrizione3_RECT)


            if self.isFinished:
                gb.Enigma = False
                
                if not self.suggerimento:
                    gb.screen.blit(self.scelte, (390*gb.mult, 40 * gb.mult))
                    
                distanza_righe = 23
                valuex, valuey = 181, 50

                font_size = 4
                # print(self.risposte)

                default_color = "#c2c2c2"
                selected_color = "Black"

                def imposta_colore(num_risposta):
                    if self.number_selection == num_risposta:
                        return selected_color	
                    else:
                        return default_color


                self.RISPOSTA_TEXT = get_font(font_size*int(gb.mult)).render(self.risposte[0], True, imposta_colore(0))
                self.RISPOSTA_RECT = self.RISPOSTA_TEXT.get_rect(center=(gb.width/2+valuex*gb.mult, (valuey+distanza_righe)*gb.mult))

                self.RISPOSTA1_TEXT = get_font(font_size*int(gb.mult)).render(self.risposte[1], True, imposta_colore(1))
                self.RISPOSTA1_RECT = self.RISPOSTA1_TEXT.get_rect(center=(gb.width/2+valuex*gb.mult, (valuey+distanza_righe*2)*gb.mult))

                gb.screen.blit(self.RISPOSTA_TEXT, self.RISPOSTA_RECT)
                gb.screen.blit(self.RISPOSTA1_TEXT, self.RISPOSTA1_RECT)
                

            avanza = Button(image=py.image.load("assets/tasello.png").convert(), pos=(120*gb.mult,  gb.height-12*gb.mult), 
                                text_input="", font=py.font.Font("font/font.ttf", (8*int(gb.mult))), base_color="White", hovering_color="#d7fcd4", scale=1.8)
            

            if self.interm == 0 or self.cooldown_interm != gb.fps / 10:
                avanza.update(gb.screen)
                self.cooldown_interm += 0.25

            self.interm += 1
            
            if self.interm >= gb.fps and self.cooldown_interm == gb.fps / 10:
                self.interm = 0
                self.cooldown_interm = 0


            for event in py.event.get():
                keys_pressed = py.key.get_pressed()

                if event.type == py.QUIT or keys_pressed[py.K_ESCAPE]:
                    py.quit()
                    sys.exit()


                if keys_pressed[py.K_SPACE] and not self.isFinished:
                    if self.CanIplay_sound:
                        self.__init__(personaggio = self.personaggio, oggetto = self.oggetto, descrizione = self.full_description, risposte = self.risposte, soluzione = self.number_solution + 1, text_speed = 5)
                        self.CanIplay_sound = False

                if keys_pressed[py.K_DOWN] or keys_pressed[py.K_RIGHT]:
                    self.number_selection += 1

                    if self.number_selection > len(self.risposte) - 1:
                        self.number_selection = 0


                if keys_pressed[py.K_UP] or keys_pressed[py.K_LEFT]:
                    self.number_selection -= 1

                    if self.number_selection < 0:
                        self.number_selection = len(self.risposte) - 1


                if keys_pressed[py.K_RETURN] and self.isFinished:
                    self.number_selected = self.number_selection
                    # print(gb.tentativo)

                    try:

                        if self.number_selected == self.number_solution:
                            # print("Risposta Esatta!!")
                            self.risultato = True
                        else:
                            # print("-- Risposta Errata --")
                            self.risultato = False

                    except KeyError:
                        pass

                    possoIniziare = True
                    return self.risultato
                    

                #delay.ActualState()


            py.display.flip() # ti permette di aggiornare una area dello schermo per evitare lag e fornire piu' ottimizzazione

            clock.tick(gb.fps) # setto i FramesPerSecond

class Timer():	
    def __init__(self, minutes, seconds, molt_sec, event):
        self.__max = minutes
        self.__minimal = 0
        self.__minutes = minutes
        self.__seconds = seconds * gb.fps
        self.__decrement = molt_sec
        self.__function = event
        self.__flag = True
        self.__color = "Black"

        self.__testo1 = ""
        self.__testo2 = ":"

    #print(self.min, self.max, self.increment, self.function)

    def Start(self):
        if self.__flag:
            self.__seconds -= self.__decrement

            if self.__seconds <= 0:
                self.__seconds = 60 * gb.fps
                self.__minutes -= 1

            if self.__seconds/gb.fps < 10:
                self.__testo2 = ":0"
            else:
                self.__testo2 = ":"

            if self.__minutes < 10:
                self.__testo1 = "0"
            else:
                self.__testo1 = ""

            if int(self.getMinutes()) < self.__minimal:
                self.__minutes = self.__minimal
                self.__function()
                self.Pause()

    def ReStart(self):
        if not self.__flag:
            self.__flag = True
            self.__minutes = self.__max

    def Pause(self):
        self.__flag = False

    def DePause(self):
        self.__flag = True

    def AddSeconds(self, value):
        if (self.getSeconds() + value) >= 60 or (self.getSeconds() + value) <= 0:
            if value < 0:
                parse_value = -0.9999
            else:
                parse_value = +0.9999

            self.__minutes += int(value/60 + parse_value)
            
            m =  value//gb.fps

            var = value - (m * 60)
            d = self.getSeconds() + var - 60
            
            self.__seconds += var * gb.fps

            if self.getSeconds() >= 59:
                self.__seconds = d * gb.fps

            # if value != (m * 60):
            # 	self.__minutes -= 1

        else:
            self.__seconds += value * gb.fps
        
        gb.score_seconds = 0

    def Stop(self):
        self.__init__(self.__max_sec, self.__molt_sec, self.__function)

    def Show(self):
        testo = get_font(8*int(gb.mult)).render((self.__testo1+str(self.__minutes)+str(self.__testo2)+str(int(self.__seconds/gb.fps))), True, self.__color)
        gb.screen.blit(testo, (gb.width/2 - testo.get_width()/2, 35 * gb.mult))

    def ChangeColor(self, v):
        self.__color = v

    def getSeconds(self):
        return self.__seconds / gb.fps
        
    def getMinutes(self):
        return self.__minutes

    def ActualState(self):
        if self.__flag:
            print("| Current Second: %d | Min Seconds: %d | Function: %s |" %(self.getSeconds() * self.getMinutes() * 60, self.__minimal/gb.fps, self.__function))


class Delay():
    def __init__(self, sec, event):
        self.__min = 0
        self.__max = sec * gb.fps
        self.__increment = 1
        self.__function = event
        self.__flag = True
        self.__times = 0

    # | Avvia il delay -> Poi si interromperà |
    def Start(self):
        if self.__flag:
            self.__min += self.__increment

            if int(self.__min) >= self.__max:
                self.__function()
                self.__flag = False

    # | Restarta il delay |
    def ReStart(self):
        if not self.__flag:
            self.__min = 0
            self.__flag = True
            
    def Stop(self):
        if self.__flag:
            self.__flag = False
            self.__min = 0

    # | Imposta il delay a infinito |
    def Infinite(self):
        self.ReStart()
        self.Start()

    def TotTimes(self, val):
        if self.__times <= val:
            self.ReStart()
            self.Start()
            self.__times += 1

    # | Stampa lo stato attuale del delay |
    def ActualState(self):
        print("| Current Second: %d | Max Seconds: %d | Function: %s |" %(self.__min/gb.fps, self.__max/gb.fps, self.__function))
