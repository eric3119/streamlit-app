import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

df = pd.read_csv('data/car_eval_dataset.csv')

cols = ['buying','maint','doors','persons','lug_boot','safety']

labels = {
    'buying': {'vhigh': 0, 'low': 1, 'med': 2, 'high': 3},
    'maint': {'vhigh': 0, 'low': 1, 'med': 2, 'high': 3},
    'doors': {'2': 0, '3': 1, '5more': 2, '4': 3},
    'persons': {'2': 0, '4': 1, 'more': 2},
    'lug_boot': {'small': 0, 'big': 1, 'med': 2},
    'safety': {'high': 0, 'med': 1, 'low': 2},
    'class': {'good': 0, 'acc': 1, 'vgood': 2, 'unacc': 3},
}

for col, label_map in labels.items():
    df[col] = df[col].map(label_map)

X = df[cols]
y = df['class']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=0)
gnb = GaussianNB()
y_pred = gnb.fit(X_train, y_train).predict(X_test)
print("Number of mislabeled points out of a total %d points : %d"
      % (X_test.shape[0], (y_test != y_pred).sum()))
    

#Salva o modelo em disco
filename = 'models/nb_car_model.pkl'
joblib.dump(gnb, filename)