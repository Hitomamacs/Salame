#%%importiamo le librerie Tutto questo con la partecipazione di Marco De vellis, for commercial use macsdeve@gmail.com eleggetelo presidente e fategli un bocchino che se lo merita!
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn.preprocessing
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Flatten, Bidirectional
from sklearn.cluster import KMeans

#%%carichiamo il file e diamogli una prima occhiata
Raw_data = pd.read_csv('database.csv')
print (Raw_data)
#Non possiamo utilizzare il .describe perché ci andrebbe solo a descrivere colonne che hanno float come dtype
Raw_data.shape
Raw_data.describe()
Raw_data.head()
#Andiamo ad analizzare le diverse colonne:
Raw_data.dtypes
#%%Partiamo dalle più semplici:
#Andremo ad esludere il Time e le ultime variabili in quanto il loro valore non è
#necessario per la rete:
Data = Raw_data
Data.drop(Data.columns[1], axis=1, inplace=True)
Data.drop(Data.columns[15:20], axis=1, inplace=True)
print(Data.dtypes)

#%% Encodiamo la Date:
#Dobbiamo trasformare per prima cosa l'object in datetime, per poi avere un modo
#per trasformarlo in giorni dal giorno 0 (primo terremoto).
from datetime import date
Data['Date'] = pd.to_datetime(Data['Date'], utc= 'True')
Data.dtypes
dummy_dates = list(Data.iloc[:,0])
for i in range(len(dummy_dates)):
    if i == 0:
        pass
    else:
        nanoseconds = dummy_dates[i] - dummy_dates[0]
        nanoseconds = nanoseconds.days
        dummy_dates[i] = nanoseconds
dummy_dates[0] = 0

Data['Date'] = dummy_dates
Data.head()

#%%Latitude e longitude

Dimensions = np.zeros((23412,2))
Dimensions[:,0] = Data.iloc[:,1]
Dimensions[:,1] = Data.iloc[:,2]

#%% Per trovare i centroidi
kmeans = KMeans(n_clusters=15, n_init=5, max_iter=50, precompute_distances=True).fit(Dimensions)
inertias = []
for i in range(10,40):
    clusters = i
    kmeans = KMeans(n_clusters=clusters, n_init=5, max_iter=280, verbose = 0, precompute_distances=True).fit(Dimensions)
    inertias.append(kmeans.inertia_)
print(len(inertias))
#comandi a mia disposizione:
#labels_: label di ogni punto
#cluter_centers_ coordinate centroidi
#inertia_: somma distanze al quadrato di ogni sample rispetto ad ogni centroide

#Printiamo le inertias, quelle necessarie sono 8
plt.plot(range(30),inertias)

#%% One-hot encodiamo tutto in Data
Data_labels = []
Data_kmeans = KMeans(n_clusters=8, n_init=5, max_iter=280, verbose = 0, precompute_distances=True).fit(Dimensions)
Data_labels = Data_kmeans.labels_
Data_labels = np.array(Data_labels)
print(Data_labels)
Data['coordlabels'] = pd.Series(Data_labels, index=Data.index)
Data['coordlabels'] = pd.Categorical(Data['coordlabels'])
Zone = pd.get_dummies(Data['coordlabels'], prefix = 'zona')
Data.drop(Data.columns[15], axis=1, inplace=True)
Data = pd.concat([Data, Zone], axis=1)
Data.drop(Data.columns[1:3], axis=1, inplace=True)
Data.dtypes

#%%Occupiamoci degli object data, gli altri one-hot encodabili
Data.iloc[:,1].unique()
#cosa vogliamo fare con i dati che non sono Eathquake né Nuclear Explosion?
#%%cerchiamo di capire quanti Type ci sono con un ciclo if:
Type = Data.iloc[:,4]
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
#train 75 percento, y differenza in giorni

#%% One-hot encodiamo i Types:
Data['Type'] = pd.Categorical(Data['Type'])
Type_encoded = pd.get_dummies(Data['Type'], prefix = 'tipologia')
Data = pd.concat([Data, Type_encoded], axis=1)
Data.drop(Data.columns[1], axis=1, inplace=True)

#%% One-hot encodiamo i Magnitude Type:
Data['Magnitude Type'] = pd.Categorical(Data['Magnitude Type'])
Magnitude_encoded = pd.get_dummies(Data['Magnitude Type'], prefix = 'tipo_magnitudo')
Data = pd.concat([Data, Magnitude_encoded], axis=1)
Data.drop(Data.columns[5], axis=1, inplace=True)
Data.dtypes

#Normalizziamo il resto dei dati:
