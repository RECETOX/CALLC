from trainl1 import train_l1_func
from applyl1 import apply_models
from initial_train import cv_to_fold
import pandas as pd
from random import shuffle
from sklearn.model_selection import KFold
from sklearn.preprocessing import maxabs_scale

import pickle
import numpy as np
import matplotlib.pyplot as plt


def main(infilen,featfilen,sys):
	infile = pd.read_csv(infilen)
	keep_f = [x.strip() for x in open(featfilen).readlines()]
	keep_f.remove('system') 

# XXX: call initial_train.sel_features instead?
	selected_set = infile[keep_f].dropna()

	models = [ 'lasso', 'adaboost','xgb','SVM','brr' ]
	n_all = [ 20, 40, 60, 80, 100 ]
	runs = 5

	best = pd.DataFrame({'corr' : [ -1.]*5, 'run' : ['']*5})
	best.index = models

	for n in n_all:
		for run in range(runs):
			k = f"{sys}_{n}_{run}"
			select_index = list(range(len(selected_set.index)))
			if n > len(selected_set.index):
				raise ValueError(f"n ({n}) > set size")

			shuffle(select_index)
			train = selected_set.iloc[select_index[0:n],]
			test = selected_set.iloc[select_index[n:],]
			result = test[['time']]

			if len(select_index[n:]) < 10:
				raise ValueError(f"test size too small")

			cv = KFold(n_splits=10,shuffle=True)
			cv = list(cv.split(train.index))
			cv_list = cv_to_fold(cv,len(train.index))

			print(f"Training n={n}, run={run}")
			try:
				preds_own = train_l1_func(train,names=[k]*8,adds=['']*8,cv=cv)
			except ValueError as e:
				print("Oops: ",e)
				continue


			for mn in models:
				model = 0
				with open(f"mods_l1/{k}_{mn}.pickle","rb") as mf:
					model = pickle.load(mf,encoding='latin1')
				test2 = test.drop(["time","IDENTIFIER"],axis=1)
				if mn == "SVM":
					test2 = maxabs_scale(test2)
				try:
					preds = model.predict(test2)
				except ValueError as e:
					print("Oops: ",e)
					continue

				result.insert(len(result.columns),mn,preds)

			print(k)
			corres = result.corr()['time']
			print(corres)

			for mn in models:
				try:
					if best['corr'][mn] < corres[mn]:
						best['corr'][mn] = corres[mn]
						best['run'][mn] = k
				except (TypeError,KeyError) as e:
					print(f"Oops ({mn}): ",e)
					continue


	print('Final results')
	print(best)
			
'''
#			preds_l1_test,skipped_test = apply_models(test.drop(["time","IDENTIFIER"],axis=1),known_rt=test["time"],row_identifiers=test["IDENTIFIER"])

				preds[np.abs(preds) > 1e4] = 0.
				plt.plot(test['time'].values)
#				plt.plot(preds)
#				plt.scatter(test['time'].values,preds)
				plt.savefig('plot.png')
				print(preds)
				print(test["time"])
				raise RuntimeError("shit")
'''




import sys
import random

if __name__ == "__main__":
	random.seed(42)

	if len(sys.argv) != 4:
		raise RuntimeError(f"usage: {sys.argv[0]} input features system")
	main(*sys.argv[1:4])
	
	

