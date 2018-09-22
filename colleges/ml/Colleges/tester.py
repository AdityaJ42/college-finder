from django.core.cache import cache
import pandas as pd
import pickle
import os

settings_dir = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))

pathname = PROJECT_ROOT + '/Colleges'
files = os.listdir(pathname)

for datasheet in files:
	dataset = pd.read_csv(pathname + '/' + datasheet)
	X = dataset.iloc[:, :-1].values
	y = dataset.iloc[:, -1].values

	filename = ''
	i = 0
	while datasheet[i] != '.':
		filename += datasheet[i]
		i += 1

	from sklearn.model_selection import train_test_split
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.33, random_state = 0)

	from sklearn.linear_model import LinearRegression
	regressor = LinearRegression()
	regressor.fit(X_train, y_train)

	filename = filename + '.sav'
	pickle.dump(regressor, open(filename, 'wb'))
