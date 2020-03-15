# coding=utf-8
#!/usr/bin/env python
import vrep
import sys
import math
import time

#Variables
clientID = -1
#Ruedas
leftMotor = -1
rightMotor = -1
#Sensores
proximitySensors = [-1, -1, -1, -1, -1, -1, -1, -1]
#Colisionador
collision = 0

#Conexion al servidor
def conexion_a_servidor():
	global clientID
	#Solo en caso, detiene todas las conexiones abiertas
	vrep.simxFinish(-1)
	#ID de cliente del servidor
	clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
	#Verifica si el id del cliente es valido
	if clientID != -1:
		print("Conctado a un Servidor Remoto API")
		vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot_wait)
	else:
		print("Fallo la conexion con el servidor remoto API")
		sys.exit("No se puede conectar")

#Obtiene los puntos para cada motor por su nombre en el simulador VREP
def obtener_punteros_a_actuadores():
	global leftMotor, rightMotor, proximitySensors, collision
	#Motores, rotores, ruedas
	errorCode, leftMotor = vrep.simxGetObjectHandle(clientID, 'ePuck_leftJoint', vrep.simx_opmode_oneshot_wait)
	errorCode, rightMotor = vrep.simxGetObjectHandle(clientID, 'ePuck_rightJoint', vrep.simx_opmode_oneshot_wait)
	#Evento de Collision
	errorCode, collision = vrep.simxGetCollisionHandle(clientID, 'Collision', vrep.simx_opmode_oneshot_wait)
	#Vector de sensores
	for i in range(0, 8):
		errorCode, proximitySensors[i] = vrep.simxGetObjectHandle(clientID, 'ePuck_proxSensor' + str(i + 1), vrep.simx_opmode_oneshot_wait)


#Genera el movimiento valocidad, en el motor especificado
def move_motor(motor, velocity):
	if motor == 'L':
		vrep.simxSetJointTargetVelocity(clientID, leftMotor, velocity, vrep.simx_opmode_oneshot_wait)
	elif motor == 'R':
		vrep.simxSetJointTargetVelocity(clientID, rightMotor, velocity, vrep.simx_opmode_oneshot_wait)
	else:
		print("Usé L o R (uppercase) para especificar el motor.")


#Obtiene los datos para cada sensor
def readProximitySensor():

	valores_1 = vrep.simxReadProximitySensor(clientID, proximitySensors[0], vrep.simx_opmode_oneshot_wait)
	#print(valores_1)

	valores_2 = vrep.simxReadProximitySensor(clientID, proximitySensors[1], vrep.simx_opmode_oneshot_wait)
	valores_3 = vrep.simxReadProximitySensor(clientID, proximitySensors[2], vrep.simx_opmode_oneshot_wait)
	valores_4 = vrep.simxReadProximitySensor(clientID, proximitySensors[3], vrep.simx_opmode_oneshot_wait)
	valores_5 = vrep.simxReadProximitySensor(clientID, proximitySensors[4], vrep.simx_opmode_oneshot_wait)
	valores_6 = vrep.simxReadProximitySensor(clientID, proximitySensors[5], vrep.simx_opmode_oneshot_wait)
	valores_7 = vrep.simxReadProximitySensor(clientID, proximitySensors[6], vrep.simx_opmode_oneshot_wait)
	valores_8 = vrep.simxReadProximitySensor(clientID, proximitySensors[7], vrep.simx_opmode_oneshot_wait)

	sensores_detectados = [valores_1[1]*1,valores_2[1]*1,valores_3[1]*1,valores_4[1]*1,valores_5[1]*1,valores_6[1]*1,valores_7[1]*1,valores_8[1]*1]
	#print(sensores_detectados)

	return sensores_detectados


def detectar_colision():
	errorCode, value = vrep.simxReadCollision(clientID, collision, vrep.simx_opmode_oneshot_wait)
	#print("--------------->Colision", value)
	if value == True: return 1;
	else: return 0;

#Red neuronal
def red_neuronal():

	#Funcion de activacion
	def Sigmoid(x):
		return 1.0 / (1.0 + math.exp(-x))

	#Entradas de red neuronal
	X_entradas = readProximitySensor()

	#PESOS Y BIAS DE RED NEURONAL
	x_1pesos = [1.3938398361,-0.6264979243,-1.6290367842,-0.3243882954,-0.9883259535,1.2461699247,-0.6211453080,-0.0382302813,1.3795541525,-1.1297724247]
	x_2pesos = [1.4166938066,-0.2124705464,-2.5407421589,-0.5493214130,-0.5820290446,0.8738359809,-1.6477568150,0.6057857275,2.2263391018,-0.9918686152]
	x_3pesos = [-0.0583946332,-1.7542599440,-1.5623576641,0.6932736635,1.6037040949,-0.5207472444,-1.5845406055,1.5206800699,0.6171860695,-1.1381900311]
	x_4pesos = [-0.6267380118,1.2858476639,1.8887029886,-0.9917637706,2.1060373783,-2.5542857647,-0.2871953845,-1.3511992693,-1.3712074757,1.7733919621]
	x_5pesos = [-1.3469693661,0.7019736767,1.5565010309,0.8445140719,-0.7978339791,1.4383741617,1.7578314543,-1.2781608105,-2.0728657246,1.0134986639]
	x_6pesos = [-1.4657834768,-0.2065136284,0.7099407911,0.7974766493,-0.1229428127,0.8319663405,1.4539290667,-0.1155052036,-0.3422167897,-0.1271577775]
	x_7pesos = [1.2533580065,1.5530157089,1.2434841394,-1.3415987492,-0.7019926906,-0.7452464700,-0.7739377022,-1.8503683805,-0.2745518982,1.2911701202]
	x_8pesos = [0.3868831694,0.0731571242,-1.0699008703,-0.9381039143,-1.0165928602,1.1099907160,-0.6299777627,0.4891840518,1.2617181540,-0.8473164439]

	bias_capa_oculta = [-0.6660405397,-0.4451506436,-0.0533072092,0.6542299390,0.8349362016,-0.3337975442,-0.3050000072,0.2315034121,-0.8491144776,0.0557236858]

	neurona_1_pesos_capa_oculta_1_salida = [-0.2904030681,-1.6309013367,1.6927438974,-2.0016269684,-1.0667397976,1.6152234077]
	neurona_2_pesos_capa_oculta_1_salida = [-2.8007223606,0.2402695566,0.7810007334,0.7834934592,-1.0205895901,-0.1425531209]
	neurona_3_pesos_capa_oculta_1_salida = [-2.8226308823,2.3022019863,-0.9937397838,2.1922829151,0.2418479919,-2.2034854889]
	neurona_4_pesos_capa_oculta_1_salida = [0.6908535957,-0.0976108313,-1.4423187971,-0.1277932525,1.3715802431,-1.1729278564]
	neurona_5_pesos_capa_oculta_1_salida = [1.7291048765,-1.6734671593,-0.8147674799,1.7541098595,-2.5065712929,-0.5831801295]
	neurona_6_pesos_capa_oculta_1_salida = [-0.1229747087,0.5328510404,-0.7540578842,-2.8105812073,2.3138628006,0.4237969220]
	neurona_7_pesos_capa_oculta_1_salida = [-1.2959350348,1.9939429760,-1.6681058407,-0.1707301140,1.3787775040,-0.7545670271]
	neurona_8_pesos_capa_oculta_1_salida = [2.9433979988,-1.0971208811,-1.7632560730,-0.7278521061,-0.2024826258,0.6769304276]
	neurona_9_pesos_capa_oculta_1_salida = [1.1174783707,-1.9957975149,1.2060033083,-2.0927672386,-1.2656511068,2.1685514450]
	neurona_10_pesos_capa_oculta_1_salida = [-2.2539470196,1.5568972826,0.6709018946,1.5455685854,-0.2623748779,-1.4636383057]

	bias_capa_salida = [-0.0634169206,-0.8182433248,-0.3021243811,-0.4722496271,-1.0465153456,-0.0387647226]
	#PESOS Y BIAS DE RED NEURONAL


	capa_oculata_1_salidas_1 = [0,0,0,0,0,0,0,0,0,0]
	for i in range(0, 10):
		capa_oculata_1_salidas_1[i] += X_entradas[0] * x_1pesos[i]
		capa_oculata_1_salidas_1[i] += X_entradas[1] * x_2pesos[i]
		capa_oculata_1_salidas_1[i] += X_entradas[2] * x_3pesos[i]
		capa_oculata_1_salidas_1[i] += X_entradas[3] * x_4pesos[i]
		capa_oculata_1_salidas_1[i] += X_entradas[4] * x_5pesos[i]
		capa_oculata_1_salidas_1[i] += X_entradas[5] * x_6pesos[i]
		capa_oculata_1_salidas_1[i] += X_entradas[6] * x_7pesos[i]
		capa_oculata_1_salidas_1[i] += X_entradas[7] * x_8pesos[i]

	capa_oculata_1_salidas = [0,0,0,0,0,0,0,0,0,0]
	for  i in range(0, 10):
		sumatoria = capa_oculata_1_salidas_1[i] + bias_capa_oculta[i]
		capa_oculata_1_salidas[i] = Sigmoid(sumatoria)

	salidas_sumadas_finales = [0,0,0,0,0,0]
	for i in range(0, 6):
		salidas_sumadas_finales[i] += capa_oculata_1_salidas[0] * neurona_1_pesos_capa_oculta_1_salida[i]
		salidas_sumadas_finales[i] += capa_oculata_1_salidas[1] * neurona_2_pesos_capa_oculta_1_salida[i]
		salidas_sumadas_finales[i] += capa_oculata_1_salidas[2] * neurona_3_pesos_capa_oculta_1_salida[i]
		salidas_sumadas_finales[i] += capa_oculata_1_salidas[3] * neurona_4_pesos_capa_oculta_1_salida[i]
		salidas_sumadas_finales[i] += capa_oculata_1_salidas[4] * neurona_5_pesos_capa_oculta_1_salida[i]
		salidas_sumadas_finales[i] += capa_oculata_1_salidas[5] * neurona_6_pesos_capa_oculta_1_salida[i]
		salidas_sumadas_finales[i] += capa_oculata_1_salidas[6] * neurona_7_pesos_capa_oculta_1_salida[i]
		salidas_sumadas_finales[i] += capa_oculata_1_salidas[7] * neurona_8_pesos_capa_oculta_1_salida[i]
		salidas_sumadas_finales[i] += capa_oculata_1_salidas[8] * neurona_9_pesos_capa_oculta_1_salida[i]
		salidas_sumadas_finales[i] += capa_oculata_1_salidas[9] * neurona_10_pesos_capa_oculta_1_salida[i]

	salidas_finales_definitivas = [0,0,0,0,0,0]
	for i in range(0,6):
		salida_no_sigmoide = salidas_sumadas_finales[i] + bias_capa_salida[i]
		salidas_finales_definitivas[i] = Sigmoid(salida_no_sigmoide)

	print(X_entradas)
	print(salidas_finales_definitivas)
	valor = -10; indice = 0
	for i in range(0, len(salidas_finales_definitivas)):
		if valor < salidas_finales_definitivas[i]:
			valor = salidas_finales_definitivas[i]
			indice = i
	valor2 = -10; indice2 = 0
	for i in range(0, len(salidas_finales_definitivas)):
		if valor2 < salidas_finales_definitivas[i] and salidas_finales_definitivas[i] < salidas_finales_definitivas[indice] :
			valor2 = salidas_finales_definitivas[i]
			indice2 = i

	#print(indice, indice2)
	salidas_finales_definitivas[indice] = 1
	salidas_finales_definitivas[indice2] = 1
	for i in range(0, len(salidas_finales_definitivas)):
		if salidas_finales_definitivas[i] < 1:
			salidas_finales_definitivas[i] = 0

	#print(salidas_finales_definitivas)

	velocidad_right = 0
	velocidad_left = 0

	if salidas_finales_definitivas[0] == 1:
		velocidad_right = 1
	elif salidas_finales_definitivas[1] == 1:
		velocidad_right = 2
	elif salidas_finales_definitivas[2] == 1:
		velocidad_right = 3

	if  salidas_finales_definitivas[3] == 1:
		velocidad_left = 1
	elif salidas_finales_definitivas[4] == 1:
		velocidad_left = 2
	elif salidas_finales_definitivas[5] == 1:
		velocidad_left = 3

	move_motor('R', velocidad_right)
	move_motor('L', velocidad_left)

	pass

def main():
	conexion_a_servidor()
	obtener_punteros_a_actuadores()

	for i in range(0, 3):

		for i in range(1, 100):
			red_neuronal()

			if detectar_colision() == 1:
				break

		vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot_wait)
		time.sleep(2)
		vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot_wait)

	vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot_wait)
	vrep.simxFinish(clientID)


if __name__ == '__main__':
	main()























	#
