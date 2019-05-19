#%%importiamo le librerie
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn.preprocessing
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Flatten, Bidirectional

#%%carichiamo il file e lo suddividiamo in test e train
Raw_data = pd.read_csv('database.csv')
#Non possiamo utilizzare il .describe perché ci andrebbe solo a descrivere colonne che hanno float come dtype
Raw_data.shape
Raw_data.describe()
Raw_data.head()
Raw_data.dtypes
#Andremo ad esludere la data dell'evento in quanto il suo valore è inutile.
#Il valore da noi cercato è quanti giorni sono passati dal terremoto precedente
#avvenuto nel raggio di 100 km.
Raw_data.iloc[:,4].unique()
#cosa vogliamo fare con i dati che non sono Eathquake né Nuclear Explosion?

#%%cerchiamo di capire quanti Type Earthquake ci sono con un semplice ciclo if:
Type = Raw_data.iloc[:,4]
Type = np.array(Type)
Earthquake = 0

for x in range(Type.size):
    if Type[x] == 'Earthquake':
        Earthquake = Earthquake+1

Earthquake
#dovremo one-hot encodare questa feature

#%%Occupiamoci della magnitude type:
Raw_data.iloc[:,9].unique()

# ML: magnitudo locale (Richter)

# MS: Surface wave magnitude scale

# MB: Body wave magnitude scale: "body-wave magnitude" developed to
# overcome the distance and magnitude limitations of the ML scale inherent
# in the use of surface waves. maximum amplitude of P waves in the first 10 seconds.

# MW: Moment magnitude scale: rigidità della Terra moltiplicata per il momento
# medio di spostamento della faglia e la dimensione dell'area dislocata.
# misurare le dimensioni dei terremoti in termini di energia liberata.

# MD: Duration magnitude signal

# li one-hot encodiamo per evitare di rovinare i dati.

# per fillare i nan metto MW.

#time da id a status non vengono utilizzati.

#train 75 percento, y differenza in giorni

#%%encodiamo la data:
date = Raw_data.iloc[:,0]
Raw_data['Date'] = pd.to_datetime(Raw_data['Date'], infer_datetime_format = 'True')
Raw_data.head()
Raw_data.dtypes
