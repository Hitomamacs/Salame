
#%% importo numpy per una prova
import numpy as np
#%% avremo inizialmente 7 vite
vite = 7
#%% ho scoperto che le lettere in una stringa si possono selezionare
parola = str(input('quale parola vuoi mettere?'))
lettere = 0
for x in parola:
    lettere += 1
grafica = ""
for x in range(lettere):
    grafica = grafica + "_" + " "
grafica
#%%
gioco_finito = 0
def control():
    for x in range(lettere*2):
        if grafica[x] == '_':
            break
        elif x == int((lettere*2)-1):
            gioco_finito=1
def lettere_usate(input):
    for x in range(lettere*2):
        if grafica[x] == input:
            print('avevi già usato questa lettera!')
            vite = vite - 1
            if vite > 0:
                print('hai ancora',vite'mosse sbagliate da poter fare')
            else:
                gioco_finito = 1
parole_messe = 0
def aggiungi_lettera(input):
    for x in range(lettere):
        if parola[x] == input:

            numero = int((2*x)+1)
            grafica[numero] = input
            parole_messe = 1
        elif x == int((lettere*2)-1):
            gioco_finito = 1
#%%
            gioco_finito=1
while gioco_finito = 0:
    input = input('quale lettera vuoi usare?')
    lettere_usate(input)
    lettere
    control()
