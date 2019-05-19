#%%importiamo le librerie
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn.preprocessing
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Flatten, Bidirectional

#%%carichiamo il file e lo suddividiamo in test e train
Raw_data = pd.read_csv('database.csv')
