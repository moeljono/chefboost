import pandas as pd
import numpy as np

import imp

from commons import functions
from training import Preprocess, Training

def regressor(df, config, header, dataset_features):
	
	debug = config['debug'] 
	algorithm = config['algorithm']
	
	enableRandomForest = config['enableRandomForest']
	num_of_trees = config['num_of_trees']
	enableMultitasking = config['enableMultitasking']

	enableGBM = config['enableGBM']
	epochs = config['epochs']
	learning_rate = config['learning_rate']

	enableAdaboost = config['enableAdaboost']
	
	#------------------------------
	
	base_df = df.copy()
	
	root = 1
	file = "outputs/rules/rules0.py"
	if debug == False:
		functions.createFile(file, header)
	
	Training.buildDecisionTree(df,root,file, config, dataset_features) #generate rules0
	
	df = base_df.copy()
	
	#------------------------------
	
	for index in range(1,epochs):	
		#run data(i-1) and rules(i-1), save data1
		
		#dynamic import
		moduleName = "outputs/rules/rules%s" % (index-1)
		fp, pathname, description = imp.find_module(moduleName)
		myrules = imp.load_module(moduleName, fp, pathname, description) #rules0
		
		new_data_set = "outputs/data/data%s.csv" % (index)
		f = open(new_data_set, "w")
		
		#put header in the following file
		columns = df.shape[1]
		
		for i, instance in df.iterrows():
			params = []
			line = ""
			for j in range(0, columns-1):
				params.append(instance[j])
				if j > 0:
					line = line + ","
				line = line + str(instance[j])
			
			prediction = int(myrules.findDecision(params)) #apply rules(i-1) for data(i-1)
			actual = instance[columns-1]
			
			#print(prediction)
			
			#loss was ((actual - prediction)^2) / 2
			#partial derivative of loss function with respect to the prediction is prediction - actual
			#y' = y' - alpha * gradient = y' - alpha * (prediction - actual) = y' = y' + alpha * (actual - prediction)
			#whereas y' is prediction and alpha is learning rate
			
			gradient = int(learning_rate)*(actual - prediction)
			
			instance[columns-1] = gradient
			
			df.loc[i] = instance
		
		df.to_csv(new_data_set, index=False)
		#data(i) created
		#---------------------------------
		
		file = "outputs/rules/rules"+str(index)+".py"
		
		if debug == False:
			functions.createFile(file, header)
		
		current_df = df.copy()
		Training.buildDecisionTree(df,root,file, config, dataset_features)
		df = current_df.copy() #numeric features require this restoration to apply findDecision function
		
		#rules(i) created
		#---------------------------------

def classifier(df, config, header, dataset_features):
	print("gradient boosting for classification")
	
	debug = config['debug']
	epochs = config['epochs']
	
	temp_df = df.copy()
	original_dataset = df.copy()
	worksheet = df.copy()
	
	classes = df['Decision'].unique()
	
	boosted_predictions = np.zeros([df.shape[0], len(classes)])
	
	for epoch in range(0, epochs):
		for i in range(0, len(classes)):
			current_class = classes[i]
			
			if epoch == 0:
				temp_df['Decision'] = np.where(df['Decision'] == current_class, 1, 0)
				worksheet['Y_'+str(i)] = temp_df['Decision']
			else:
				temp_df['Decision'] = worksheet['Y-P_'+str(i)]
			
			predictions = []
			
			#change data type for decision column
			temp_df[['Decision']].astype('int64')
			
			root = 1
			file = "outputs/rules/rules-for-"+current_class+".py"
			
			if debug == False: functions.createFile(file, header)
			
			Training.buildDecisionTree(temp_df,root,file, config, dataset_features)
			#decision rules created
			#----------------------------
			
			#dynamic import
			moduleName = "outputs/rules/rules-for-"+current_class
			fp, pathname, description = imp.find_module(moduleName)
			myrules = imp.load_module(moduleName, fp, pathname, description) #rules0
			
			num_of_columns = df.shape[1]
			
			for row, instance in df.iterrows():
				features = []
				for j in range(0, num_of_columns-1): #iterate on features
					features.append(instance[j])
				
				actual = temp_df.loc[row]['Decision']
				prediction = myrules.findDecision(features)
				predictions.append(prediction)
					
			#----------------------------
			if epoch == 0:
				worksheet['F_'+str(i)] = 0
			else:
				worksheet['F_'+str(i)] = pd.Series(predictions).values
			
			boosted_predictions[:,i] = boosted_predictions[:,i] + worksheet['F_'+str(i)].values.astype(np.float32)
			
			worksheet['P_'+str(i)] = 0
			
			#----------------------------
			temp_df = df.copy() #restoration
		
		for row, instance in worksheet.iterrows():
			f_scores = []
			for i in range(0, len(classes)):
				f_scores.append(instance['F_'+str(i)])
							
			probabilities = functions.softmax(f_scores)
							
			for j in range(0, len(probabilities)):
				instance['P_'+str(j)] = probabilities[j]
			
			worksheet.loc[row] = instance
		
		for i in range(0, len(classes)):
			worksheet['Y-P_'+str(i)] = worksheet['Y_'+str(i)] - worksheet['P_'+str(i)]
		
		print("round ",epoch+1)