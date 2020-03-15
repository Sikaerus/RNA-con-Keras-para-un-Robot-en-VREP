#SO==Linux, Ubuntu 16.04 LTS
#Python==3.5, Back End:TensorFlow==1.5, Front End: Keras==2.2.0, numpy==1.17.3, Pandas==0.24.2
from keras.models import Sequential
from keras.layers.core import Dense
from keras.optimizers import SGD#Se llama este optimizador
import keras
import numpy as np
import pandas as pd
import time
import os

def main():
	data_set = pd.read_csv("dataset.csv")
	X = data_set[['1','2','3','4','5','6','7','8']]
	y = data_set[['vr1','vr2','vr3','vl1','vl2','vl3']]

	model = Sequential()
	model.add(Dense(10, input_dim=8, activation='sigmoid'))
	model.add(Dense(6, activation='sigmoid'))
	#MODELO: Input = 8, Hidden 1 capa 10:10_b,30_w neuronas, Output = 6:6_b,60_w
	#Stochastic Gradient Descent optimizer
	sgd = SGD(lr=0.1, momentum=0.0, nesterov=False)
	model.compile(optimizer=sgd, loss='binary_crossentropy', metrics=['accuracy'])
	#Verbose = 1; Barra de progreso
	#Batch X.len; epoch=2500
	#Batch 1; epoch 2-5
	model.fit(X.values, y.values, batch_size=1, epochs=46, verbose=1)
	beep()
	imprime_prediccion(model.predict_proba(X.values), 1)
	#imprime_capas_pesos_bias(model)
	crear_archivo_de_estructura_de_red_neuronal(model)
def imprime_prediccion(prediccion, metodo):
	if metodo == 1:
		#Metodo 1
		print(" ")
		for i in range(0, len(prediccion)):
			print(i," ", end=" ")
			for j in range(0, len(prediccion[0])):
				print( '{0:0.5f}'.format(prediccion[i][j]), end=" ")
			print(" ")
			time.sleep(0.05)
		print(" ")
	elif metodo == 2:
		# Metodo 2
		print(prediccion)
def imprime_capas_pesos_bias(model):
	for i in range(0, len(model.layers)):
		print("Capa: ",i)
		print("Pesos: ", model.layers[i].get_weights()[0])#weights
		print("Bias: ", model.layers[i].get_weights()[1])#biases
def crear_archivo_de_estructura_de_red_neuronal(model):
	rne = open("red_neuronal_estructura.txt", "w")
	rne.write(str(len(model.layers)))
	rne.write("\n")
	rne.write("#")
	rne.write("\n")
	for i in range(0, len(model.layers)):
		nd_array_pesos = model.layers[i].get_weights()[0]
		#print(nd_array_pesos)
		#print(len(model.layers[i].get_weights()[0]))
		for w, peso in zip( range(0, len(model.layers[i].get_weights()[0])) , model.layers[i].get_weights()[0] ):
			rne.write("[")
			#print(peso)
			x = 0
			for neurona in range(0, len(peso)):
				rne.write( str( '{0:0.10f}'.format(nd_array_pesos[w][neurona]) ) )
				#rne.write(str(nd_array_pesos[w][neurona]))
				if x < len(peso)-1 :
					rne.write(",")
					x += 1
			rne.write("]\n")
		rne.write("&")
		rne.write("\n")

		nd_array_bias = model.layers[i].get_weights()[1]
		#print(nd_array_bias)
		#print(len(model.layers[i].get_weights()[1]))
		x = 0
		rne.write("[")
		for bias in range(0, len( model.layers[i].get_weights()[1] ) ):
			rne.write( str( '{0:0.10f}'.format(nd_array_bias[bias]) ) )
			#rne.write( str( nd_array_bias[bias] ))
			if x != len(model.layers[i].get_weights()[1])-1 :
				rne.write(",")
				x += 1
		rne.write("]\n")
		rne.write("#")
		rne.write("\n")
	rne.close()
def beep():
	duracion = 1#Segundos
	freq = 440#Hz
	os.system('play -nq -t alsa synth {} sine {}'.format(duracion, freq))
	#os.system('spd-say "Tu programa ha terminado"')
if __name__ == '__main__':
	main()
	#Es posible que ocurra una excepción ocacional al final.
