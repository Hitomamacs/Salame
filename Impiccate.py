
#%% importo numpy
import numpy as np


#%% definisco diverse variabili
gioco_finito = 0
vite = 7
parola = input('quale parola scegli?')
lettere = 0
for x in parola:
    lettere += 1
grafica = ""
for x in range(lettere):
    grafica = grafica + "_" + " "
lettere_in_array = np.zeros(shape = (lettere), dtype='str')
for x in range(lettere*2):
    if grafica[x] != ' ':
        a = int(x/2)
        lettere_in_array[a] = grafica[x]


#%% questa funzione mi aggiorna la grafica, da un array numpy
def aggiorna_grafica(array):
    grafica = str()
    for x in range(lettere):
        grafica = grafica + array[x] + ' '
    return grafica


#%%questa funzione mi dice cosa accade ogni volta che aggiungo una lettera
def turno(input,arraydilett,grafic,vit):
    parole_messe = 0
    lettere_nonmesse = 0
    input_invalido = 0
    gioco_finito = 0
    for x in range(lettere*2):
        if grafic[x] == input:
            print('avevi già usato questa lettera!')
            vit = vit - 1
            input_invalido = 1
            if vit > 0:
                print('hai ancora',vite,'mosse sbagliate da poter fare')
            else:
                gioco_finito = 1
            break
    if input_invalido == 0:
        for x in range(lettere):
            if parola[x] == input:
                arraydilett[x] = input
                grafic = aggiorna_grafica(arraydilett)
                parole_messe =+ 1
        if parole_messe > 0:
            if parole_messe == 1:
                print('la tua lettera era presente nella parola 1 volta.')
            else:
                print('cerano',parole_messe,'delle tue lettere nella parola!')
            print(grafic)
            for x in range(lettere):
                if arraydilett[x] == '_':
                    lettere_nonmesse =+1
            if lettere_nonmesse == 0:
                print('hai vinto!')
                gioco_finito = 1
        else:
            print('questa lettera non è nella parola')
            vit = vit - 1
            if vit > 0:
                print('hai ancora',vit,'mosse sbagliate da poter fare')
            else:
                gioco_finito = 1
    return arraydilett, grafic, gioco_finito, vit

#%% facciamo il gioco
while gioco_finito == 0:
    lettere_in_array, grafica, gioco_finito, vite = turno(str(input('dimmi la lettera che vuoi usare')),lettere_in_array,grafica,vite)
