import argparse
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import os
#from simplepreprocessor import *
#from simpledatasetloader import *
#from simpleflattenpreprocessor import *
import numpy as np
import cv2


class SimplePreprocessor:
	def __init__(self, width, height, inter=cv2.INTER_AREA):#INTER_AREA and similar functions like INTER_LINEAR, INTER_CUBE groups some pixels together
		self.width = width
		self.height = height
		self.inter = inter

	def preprocess(self, image):
		return cv2.resize(image, (self.width, self.height), interpolation=self.inter)


class SimpleFlattenPreprocessor:
	def __init__(self):
		pass

	def preprocess(self, image):
		return image.flatten()



class SimpleDatasetLoader:
	def __init__(self, preprocessors=None):#some functions which you want to apply in a given order
		self.preprocessors = preprocessors

		if self.preprocessors is None:
				self.preprocessors = []

	def load(self, imagePaths, verbose=-1):
		data = []
		labels = []

		for (i, imagePath) in enumerate(imagePaths):
			image = cv2.imread(imagePath)
			label = imagePath.split(os.path.sep)[-2]#using the folder name to sort

			if self.preprocessors is not None:
				for p in self.preprocessors:
					image = p.preprocess(image)
					print("preprocess image shape", image.shape)
			data.append(image)
			# append the corresponding label to the labels list
			labels.append(label)

		if verbose > 0 and i > 0 and (i + 1)%verbose == 0:
				print("[INFO] processed {}/{}".format(i+1, len(imagePaths)))

		return (np.array(data), np.array(labels))



ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", help="path to the image dataset", required=True, type=str)
ap.add_argument("-k", "--neighbors", help="# of nearest neighbors for classification", type=int, default=1)
ap.add_argument("-p", "--preprocess", help="height followed by width to resize", default=[32, 32], nargs='+', type=int) # nargs ='+', and type=int makes ap.preprocess as a list #https://stackoverflow.com/questions/33564246/passing-a-tuple-as-command-line-argument
cmdDict = vars(ap.parse_args())
print("----------Passed arguments printed as dictionary----------")
print(cmdDict)

dataset_path=cmdDict['dataset']
imagePaths=[]

validExtensions = ['jpg', 'jpeg', 'png', 'bmp']
for pathName, folderNames, fileNames in os.walk(dataset_path):
	for fileName in fileNames:
		if fileName.split(".")[-1] in validExtensions:
			imagePaths.append(pathName+"/"+fileName)

new_width = cmdDict['preprocess'][1]
new_height = cmdDict['preprocess'][0]
sp = SimplePreprocessor(new_width, new_height)
sfp = SimpleFlattenPreprocessor()
sdl = SimpleDatasetLoader(preprocessors = [sp,sfp])#ordered processes


(data, labels) = sdl.load(imagePaths, verbose=500)
print("data.shape", data.shape)
print("Example string labels",labels[0:5])

print("[INFO] feature matrix : {:.3f}MB".format(data.nbytes/(1024*1000.0)))

le = LabelEncoder()
labels = le.fit_transform(labels)

(trainX, testX, trainY, testY) = train_test_split(data, labels, test_size=0.25, random_state = 42)#splitting 75% training and 25% testing,random state is just a seed value

print("trainX", trainX.shape)
print("trainY", trainY.shape)

print("[INFO] evaluating k-NN classifier...")

model = KNeighborsClassifier(n_neighbors = cmdDict["neighbors"])
model.fit(trainX, trainY)


y_cap = model.predict(testX)
y = testY
print(classification_report(y, y_cap, target_names = le.classes_))
