import pygame as py
import numpy as np
import sys
import classi as component
from classi import Dialoghi, Domanda

import global_var as gb

def get_font(size):
    return py.font.Font("font/font.ttf", size)

def genera_carte():
    
    c = np.random.choice(gb.carte)
    gb.carte.remove(c)
    gb.nomi_carte.remove(np.random.choice(gb.nomi_carte))
    
    if c == 10:
        gb.nomi_reali.remove(np.random.choice(gb.nomi_reali))
        
    return c

def inizializza():
    global computer, bancone
    computer = component.Computer()
    bancone = component.Bancone()
    
    for i in range(gb.numero_giocatori):
        giocatore = component.Player("Giocatore - "+str(i))
        gb.giocatori.append(giocatore)
    
    # print(gb.giocatori, len(gb.giocatori))
    
    
    # BANCO
    
    # 2 carte
    computer.cards.append(genera_carte())
    computer.cards.append(genera_carte())
    
    # 2 carte
    gb.giocatori[gb.gioc_attualmente_giocando].cards.append(genera_carte())
    gb.giocatori[gb.gioc_attualmente_giocando].cards.append(genera_carte())
    
    gb.updateStats(computer.cards, gb.giocatori[gb.gioc_attualmente_giocando].cards[-1], np.random.choice(gb.nomi_carte), "")
    
    
    segno = str(np.random.choice(gb.nomi_carte))
    testo1 = "un " + str(gb.giocatori[gb.gioc_attualmente_giocando].cards[0]) + " di " + str(np.random.choice(gb.nomi_carte))
    testo2 = "un " + str(gb.giocatori[gb.gioc_attualmente_giocando].cards[1]) + " di " + segno
    reale = str(np.random.choice(gb.nomi_reali))
    reale1 = str(np.random.choice(gb.nomi_reali))
    
    if gb.giocatori[gb.gioc_attualmente_giocando].cards[0] == 10 and reale != "":        
        if "regina" in reale and not "" in reale:
            testo2 = "una " + reale  + " di " + str(np.random.choice(gb.nomi_carte))
        else:
            testo2 = "un " + reale + " di " + str(np.random.choice(gb.nomi_carte))
        
    if gb.giocatori[gb.gioc_attualmente_giocando].cards[1] == 10 and reale != "":
        if "regina" in reale1 and not "" in reale1:
            testo2 = "una " + reale1 + " di " + segno
        else:
            testo2 = "un " + reale1 + " di " + segno
    
    if gb.giocatori[gb.gioc_attualmente_giocando].cards[0] == 11:
        testo1 = "un asso di " + str(np.random.choice(gb.nomi_carte))
        
    if gb.giocatori[gb.gioc_attualmente_giocando].cards[1] == 11:
        testo2 = "un asso di " + segno   
        
    for carta in gb.giocatori[gb.gioc_attualmente_giocando].cards:
        if carta == 11 and sum(gb.giocatori[gb.gioc_attualmente_giocando].cards) > gb.MAX:                        
            gb.giocatori[gb.gioc_attualmente_giocando].cards.remove(carta)
            gb.giocatori[gb.gioc_attualmente_giocando].cards.append(1)
    
    gb.updateStats(computer.cards, gb.giocatori[gb.gioc_attualmente_giocando].cards[-1], segno, reale)
    
        
    Dialoghi(   
            
            personaggio = "Senex", 
            descrizione = " Hai "+ testo1 + " e " + testo2,
            text_speed = 3
            
        ).stampa()


def quit():
    py.quit()
    sys.exit()
    
def comandi():
    
    for event in py.event.get():
        
        if event.type == py.QUIT:
            quit()
        
        if event.type == py.KEYDOWN:
            key = py.key.name(event.key)
        
            # print(key)
            if key == "escape":
                quit()
                


def stampa():
    gb.screen.fill(gb.bg_color)
    
    computer.render()
    
    bancone.render_desk()
                
                
def screen_update():
    gb.clock.tick(gb.fps)
    py.display.flip()


def player_recall():

    if sum(gb.giocatori[gb.gioc_attualmente_giocando].cards) == gb.MAX and gb.last_card[2] != "" and gb.last_card[1] == 10:
    
        Dialoghi(   
            
            personaggio = "Senex", 
            descrizione = "- BlackJack!1!1! -",
            text_speed = 3
            
        ).stampa()
        gb.giocatori[gb.gioc_attualmente_giocando].scelta = 0
            
    if sum(gb.giocatori[gb.gioc_attualmente_giocando].cards) < gb.MAX:
        
            gb.giocatori[gb.gioc_attualmente_giocando].scelta = Domanda(    

                personaggio = "Senex",
                descrizione = "Cosa vuoi fare?",
                oggetto = "retro",
                risposte = ("Resto", "Rischio"),
                soluzione = 2,
                text_speed = 3
            
                        
            ).stampa()
            
    if gb.giocatori[gb.gioc_attualmente_giocando].scelta == 0 or gb.giocatori[gb.gioc_attualmente_giocando].scelta == 1:
            
        if gb.giocatori[gb.gioc_attualmente_giocando].scelta:
            gb.giocatori[gb.gioc_attualmente_giocando].cards.append(genera_carte())
            
            reale = np.random.choice(gb.nomi_reali)
            tipo = np.random.choice(gb.nomi_carte)
            if gb.giocatori[gb.gioc_attualmente_giocando].cards[-1] == 10 and reale != "":
                if "regina" in reale and not "" in reale:
                    testo = "Hai pescato: una " + str(reale) + " di " + str(tipo)
                else:
                    testo = "Hai pescato: un " + str(reale) + " di " + str(tipo)
            
            elif gb.giocatori[gb.gioc_attualmente_giocando].cards[-1] == 11:
                valore = 1
                testo = "Hai pescato: un asso di " + str(tipo)
            
            else:
                valore = gb.giocatori[gb.gioc_attualmente_giocando].cards[-1]
                testo = "Hai pescato: "+ str(valore) +" di "+ str(tipo)
            
            for carta in gb.giocatori[gb.gioc_attualmente_giocando].cards:
                if carta == 11 and sum(gb.giocatori[gb.gioc_attualmente_giocando].cards) > gb.MAX:                        
                    gb.giocatori[gb.gioc_attualmente_giocando].cards.remove(carta)
                    gb.giocatori[gb.gioc_attualmente_giocando].cards.append(1)
                    
                    gb.updateStats(computer.cards, gb.giocatori[gb.gioc_attualmente_giocando].cards[-1], gb.last_card[0], gb.last_card[2])
                    
                    Dialoghi(   
                
                        personaggio = "Senex", 
                        descrizione = "Avevi un asso che adesso vale 1",
                        text_speed = 3
                        
                    ).stampa()
                    
                    
            gb.updateStats(computer.cards, gb.giocatori[gb.gioc_attualmente_giocando].cards[-1], tipo, reale)
            
                
                
            Dialoghi(   
            
                    personaggio = "Senex", 
                    descrizione =  testo,
                    text_speed = 3
                    
                ).stampa()
            
            
            if sum(gb.giocatori[gb.gioc_attualmente_giocando].cards) < gb.MAX and gb.giocatori[gb.gioc_attualmente_giocando].scelta:
            
                algoritmo()

def computer_recall():
        
    if sum(gb.giocatori[gb.gioc_attualmente_giocando].cards) <= gb.MAX:
        if sum(computer.cards) < gb.MAX and computer.scelta and sum(computer.cards) != sum(gb.giocatori[gb.gioc_attualmente_giocando].cards):
            computer.cards.append(genera_carte())
                        
            reale = str(np.random.choice(gb.nomi_reali))
            tipo = np.random.choice(gb.nomi_carte)
            testo = "Il bancone pesca: "+str(computer.cards[-1])+" di "+str(tipo)
            
            if computer.cards[-1] == 10 and reale != "":
                if "regina" in reale and not "" in reale:
                    testo = "Il bancone pesca: una " + reale + " di " + str(tipo)
                else:
                    testo = "Il bancone pesca: un " + reale + " di " + str(tipo)
            
            elif computer.cards[-1] == 11:
                testo = "Il bancone pesca: un asso di " + tipo
                
            gb.updateStats(computer.cards, computer.cards[-1], tipo, reale)
            
                
            Dialoghi(   
    
            personaggio = "Senex", 
            descrizione = testo,
            text_speed = 3
            
        ).stampa()
                
        else:
            
            computer.scelta = 0
                    
                    
    for carta in computer.cards:
        if carta == 11 and sum(computer.cards) > gb.MAX:
            computer.cards.remove(carta)
            computer.cards.append(1)
                
    if sum(computer.cards) < gb.MAX and computer.scelta and sum(gb.giocatori[gb.gioc_attualmente_giocando].cards) <= gb.MAX:
        computer_recall()
        

def algoritmo():    
    
    player_recall()
    
    gb.updateStats(computer.cards, "", "retro", "")
        
    Dialoghi(   
        
                personaggio = "Senex", 
                descrizione = "Ora il banco sta per girare le carte!!",
                text_speed = 3
                
            ).stampa()
    
        
    reale = str(np.random.choice(gb.nomi_reali))
    reale1 = str(np.random.choice(gb.nomi_reali))
    segno = str(np.random.choice(gb.nomi_carte))
    segno1 = np.random.choice(gb.nomi_carte)
    
    testo1 = "un " + str(computer.cards[0]) + " di " + segno
    testo2 = "un " + str(computer.cards[1]) + " di " + segno1
    
    gb.updateStats(computer.cards, computer.cards[-1], segno1, reale)
    
    if computer.cards[0]== 10 and reale != "":
        if "regina" in reale and not "" in reale:
            testo1 = "una " + reale + " di " + segno
        else:
            testo1 = "un " + reale + " di " + segno
        
    if computer.cards[1] == 10 and reale1 != "":
        if "regina" in reale1 and not "" in reale1:
            testo2 = "una " + reale1 + " di " + segno1
        else:
            testo2 = "un " + reale1 + " di " + segno1
    
    if computer.cards[0] == 11:
        testo1 = "un asso di " + segno
        
    if computer.cards[1] == 11:
        testo2 = "un asso di " + segno1
    
    Dialoghi(   
        
                personaggio = "Senex", 
                descrizione = "Il bancone ha " + testo1 +" e "+ testo2,
                text_speed = 3
                
            ).stampa()
    
    gb.updateStats(computer.cards, computer.cards[-1], segno1, reale)
    
    gb.flag_pc = True
    
    computer.scelta = 1
    
    computer_recall()

    Dialoghi(   
        
                personaggio = "Senex", 
                descrizione = "La somma del bancone e': "+str(sum(computer.cards)),
                text_speed = 3
                
            ).stampa()
    
    
    Dialoghi(   
        
                personaggio = "Senex", 
                descrizione = "La tua somma invece e': "+str(sum(gb.giocatori[gb.gioc_attualmente_giocando].cards)),
                text_speed = 3
                
            ).stampa()
                    
                    
    # CONDIZIONE VITTORIA
    
    testo = "Hai perso!"
                    
    if (sum(gb.giocatori[gb.gioc_attualmente_giocando].cards) > sum(computer.cards) and sum(gb.giocatori[gb.gioc_attualmente_giocando].cards) <= gb.MAX) or (sum(gb.giocatori[gb.gioc_attualmente_giocando].cards) <= gb.MAX and sum(computer.cards) > gb.MAX):
        testo = "Hai vinto!"
        
    elif sum(gb.giocatori[gb.gioc_attualmente_giocando].cards) == sum(computer.cards) or (sum(gb.giocatori[gb.gioc_attualmente_giocando].cards) > gb.MAX and sum(computer.cards) > gb.MAX):
        testo = "Pareggio..."
        
    Dialoghi(   

        personaggio = "Senex", 
        descrizione = testo,
        text_speed = 3
        
    ).stampa()
            
        
        
    # CONTINUARE
    gb.flag_pc = False
    
    risposta = Domanda(    

            personaggio = "Senex",
            descrizione = "Vuoi Continuare?",
            oggetto = "retro",
            risposte = ("Si", "No"),
            soluzione = 1,
            text_speed = 3
        
                    
    ).stampa()
    
    print("player:", gb.giocatori[gb.gioc_attualmente_giocando].cards, "pc:" ,computer.cards)
    
    if not risposta:
        quit()
        
    else:
        
        gb.giocatori[gb.gioc_attualmente_giocando].scelta = 3
        gb.setDefault()
        
        gb.giocatori[gb.gioc_attualmente_giocando].cards = []
        computer.cards = []
        
        inizializza()
        gb.updateStats(computer.cards, gb.giocatori[gb.gioc_attualmente_giocando].cards[-1], "retro", "")
        algoritmo()


def main():
        
    while True:
    
        # COMANDI
        comandi()
        
        # ALGORITMO
        algoritmo()
        
        # STAMPA
        stampa()
        
        # FPS
        screen_update()
        


# se volessi importare il file non verrebbe autoeseguito automaticamente
if __name__ == "__main__":
    py.init()
    inizializza()
    main()