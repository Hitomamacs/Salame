#%%importiamo le librerie Tutto questo con la partecipazione di Marco De vellis, for commercial use macsdeve@gmail.com eleggetelo presidente e fategli un bocchino che se lo merita!
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
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

#%%Normalizziamo il resto dei dati:
#qui abbiamo normalizzato la Depth
Data_scaled = Data
scaler_1 = MinMaxScaler()
Depth_sk = np.array(Data.iloc[:,1])
Depth_sk = Depth_sk.reshape(-1,1)
Depth_sk = scaler_1.fit_transform(Depth_sk)
Data_scaled.iloc[:,1] = Depth_sk
Data_scaled.head()
#%% Depth Error 4.993115
import math
Deptherr_sk = list(Data.iloc[:,2])
Deptherr_sk = [4.993115 if math.isnan(x) else x for x in Deptherr_sk]
scaler_2 = MinMaxScaler()
Deptherr_sk = np.array(Deptherr_sk)
Deptherr_sk = Deptherr_sk.reshape(-1,1)
Deptherr_sk = scaler_2.fit_transform(Deptherr_sk)
print(Deptherr_sk)
Data_scaled.iloc[:,2] = Deptherr_sk
Data_scaled.head()

#%%Dss 275.364098
Data.drop(Data.columns[2], axis=1, inplace=True)
Data_scaled.drop(Data_scaled.columns[2], axis=1, inplace=True)
Data.drop(Data.columns[3], axis=1, inplace=True)
Data_scaled.drop(Data_scaled.columns[3], axis=1, inplace=True)
Data.drop(Data.columns[5], axis=1, inplace=True)
Data_scaled.drop(Data_scaled.columns[5], axis=1, inplace=True)
Data.dtypes

#%%Magnitude
Magnitude = list(Data.iloc[:,2])
Magnitude = [5.8825 if math.isnan(x) else x for x in Magnitude]
scaler_3 = MinMaxScaler()
Magnitude = np.array(Magnitude)
Magnitude = Magnitude.reshape(-1,1)
Magnitude = scaler_3.fit_transform(Magnitude)
print(Magnitude)
Data_scaled.iloc[:,2] = Magnitude
Data_scaled.head()

#%%Azimuthal Gap
Data_scaled.describe()
AZgap = list(Data.iloc[:,3])
AZgap = [44.163532 if math.isnan(x) else x for x in AZgap]
scaler_4 = MinMaxScaler()
AZgap = np.array(AZgap)
AZgap = AZgap.reshape(-1,1)
AZgap = scaler_4.fit_transform(AZgap)
print(AZgap)
Data_scaled.iloc[:,3] = AZgap
