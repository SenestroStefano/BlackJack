import random as rand
import time

MAX = 21

def genera_carte():
    global carte
    
    c = rand.choice(carte)
    carte.remove(c)
    nomi_carte.remove(rand.choice(nomi_carte))
    
    if c == 10:
        nomi_reali.remove(rand.choice(nomi_reali))
        
    return c


def controlla_asso():
    global totale, carta, carte_giocatore
    if totale > MAX:
        for carta in carte_giocatore:
            if carta == 11:
                carte_giocatore.remove(carta)
                carte_giocatore.append(1)
                print("Avevi un asso che adesso vale 1")

Flag_continuare = True


while Flag_continuare:
    
    carte = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
    nomi_carte = ["♣️ fiori", "♥️ cuori", "♠️ picche", "♦️ quadri"] * 10
    nomi_reali = ["♚ re", "♛ regina", "⛃ fante"] * 4
    
    carte_banco = []
    carte_giocatore = []
    scelta = 1
    
    # BANCO
    
    # 2 carte
    carte_banco.append(genera_carte())
    carte_banco.append(genera_carte())
    
    # 2 carte
    carte_giocatore.append(genera_carte())
    carte_giocatore.append(genera_carte())
    totale = sum(carte_giocatore)
    
    while scelta:
        
        totale = sum(carte_giocatore)
        print("\n\n🃏 Hai un totale di "+str(totale)+" 🃏")
        
        if totale == MAX:
            print("♠️ - BlackJack!1!1! - ♠️\n\n")
            scelta = 0
        
        controlla_asso()
                
        if totale < MAX:
    
            scelta = int(input(
                
"""
 |   Desideri:   |

  - 0 Restare 0 -
 - 1 Rischiare 1 -
    
___________________        

"""
                        
                        ))
            print()
            if scelta:
                carte_giocatore.append(genera_carte())
                
                if sum(carte_giocatore) > MAX:
                    controlla_asso()
                
                if carte_giocatore[-1] == 10:
                    print("Hai pescato: un/una " +str(rand.choice(nomi_reali)))
                
                elif carte_giocatore[-1] == 11:
                    print("Hai pescato: un asso di " +str(rand.choice(nomi_carte)))
                
                else:
                    
                    print("Hai pescato: "+str(carte_giocatore[-1])+" di "+str(rand.choice(nomi_carte)))
                    
                totale = sum(carte_giocatore)
                
                print("- La tua somma e':",totale,"-")
                print("---------------------")
                
                
        if totale > MAX:
            print("\nHai perso -_-")
            scelta = 0
            
        
    print("🎰 Ora il banco sta per girare le carte!! 🃏\n")
    
    countdown = 3
    
    for i in range(0, 3):
        print("-",(3-i),"-")
        time.sleep(1)

    print("\nIl bancone ha un "+str(carte_banco[0])+" e un "+str(carte_banco[1]))
    
    scelta_banco = 1
    
    while sum(carte_banco) <= MAX and scelta_banco:
        if sum(carte_banco) < MAX - 3:
            carte_banco.append(genera_carte())
            
            if sum(carte_banco) > MAX:
                for carta in carte_banco:
                    if carta == 11:
                        carte_banco.remove(carta)
                        carte_banco.append(1)
            
            if carte_banco[-1] == 10:
                print("Il bancone pesca: un " +str(rand.choice(nomi_reali)))
            
            elif carte_banco[-1] == 11:
                print("Il bancone pesca: un asso di " +str(rand.choice(nomi_carte)))
            
            else:
                
                print("Il bancone pesca: "+str(carte_banco[-1])+" "+str(rand.choice(nomi_carte)))
                
        else:
            
            scelta_banco = 0
    
    print("----------------")   
    print("\n🧰 La somma del bancone e':",sum(carte_banco))
    print("💰 La tua somma invece e':",totale,"\n")
                    
                    
    # CONDIZIONE VITTORIA
                    
    if (totale > sum(carte_banco) and totale <= MAX) or (totale <= MAX and sum(carte_banco) > MAX):
        print("Hai vinto!")
        
    elif totale == sum(carte_banco) or (totale > MAX and sum(carte_banco) > MAX):
        print("Pareggio...")
    
    else:
        
        print("Hai perso!")
            
        
        
    # CONTINUARE
    
    risposta = input("\nVuoi continuare? ")
    
    if "n" in risposta.lower():
        Flag_continuare = False
    
    print("-------------------\n")