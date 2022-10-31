import pygame as py
from pygame.locals import *
import screeninfo

language = "it"
sceltalingua = False

for i in screeninfo.get_monitors():
    def_width, def_height = i.width, i.height

f_width, f_height = 480, 270


def setScreen():
    global screen, mult
    global width, height
    global def_width, def_height
    global f_width, f_height
    global punteggioC_testo, punteggioP_testo
    
    if mult < 1:
        mult = 1
    
    if mult * f_width > def_width:
        mult -= 1
    
    width, height = 480 * mult, 270 * mult
    
    screen = py.display.set_mode((width, height))
    py.display.set_caption(title_screen)
    
    if width >= def_width:
        screen = py.display.set_mode((0, 0), py.FULLSCREEN)
    

def setDefault():
    global MAX
    global carte, nomi_carte, nomi_reali
    global tc_a, tnc_a, tcp_a
    global flag_pc
    
    MAX = 21
    
    tc_a, tnc_a, tcp_a = "", "", ""

    carte = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
    nomi_carte = ["fiori", "cuori", "picche", "quadri"] * 10
    nomi_reali = ["re", "regina", "fante", ""] * 4
    
    flag_pc = False


def updateStats(pc_stats, valore, tipo, reale):
    global last_card, dati
    global punteggioP_testo, punteggioP_rect
    global punteggioC_testo, punteggioC_rect
    
    x = 40 * mult
    y = 30 * mult

    punteggioP_testo = py.font.Font("font/font.ttf", 20 * mult).render(str(sum(giocatori[gioc_attualmente_giocando].cards)), True, "Black")
    punteggioP_rect = punteggioP_testo.get_rect(center=(x, y))
    
    punteggioC_testo = py.font.Font("font/font.ttf", 20 * mult).render(str(sum(pc_stats)), True, "Black")
    punteggioC_rect = punteggioC_testo.get_rect(center=(width - x, y))
    
    val = valore
    if val == 11:
        val = 1
    last_card = [tipo, val, reale]
    
    dati = [pc_stats, valore, tipo, reale]


fps = 60
mult = 2

Delta_Time = 1

bg_color = "White"

title_screen = "Black Jack"

picche = py.image.load("assets/picche.png")
py.display.set_icon(picche)

numero_giocatori = 1
giocatori = []

gioc_attualmente_giocando = 0

setScreen()

clock = py.time.Clock()

setDefault()
    