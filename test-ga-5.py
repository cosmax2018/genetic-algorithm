
# test-ga-5.py : esegue degli esempi utilizzando la libreria sugli algoritmi genetici

#	(c) Copyright 2020-21 by ....@_°° Lumachina SW
#    Massimiliano Cosmelli (massimiliano.cosmelli@gmail.com)

# VEDI LA VERSIONE AGGIORNATA  ..\python\evoLisa\evoLisa.py

import time,os,sys,random,argparse, itertools
from PIL import Image

import numpy as np
import matplotlib.pyplot as plt

from ga import Simple_GA													# genetic algorithms
from images import SuperImposeNewRectangleRGBA,ColourDistanceSquaredRGBA	# graphics

def randomize(): random.seed(time.time())

def timer(function):						# prende come parametro la funzione di cui misurare il tempo di esecuzione
	def timed(*args):						# args sono i parametri passati alla funzione da misurare
		start_time = time.time()			# Ti
		result = function(*args)			# esegue la funzione
		elapsed = time.time() - start_time	# Tf
		print('Function "{name}" took {time} seconds to complete.'.format(name=function.__name__, time=elapsed))
		return result						# restituisce il risultato dell'esecuzione della funzione
	return timed
	
def plot(max_iter,fit):
	# disegna il grafico della fitness
	x = np.linspace(0,1,max_iter)
	plt.title("GA Fitness",size=24,weight='bold')
	plt.xlabel("ITERAZIONI")
	plt.ylabel("BEST FITNESS")
	plt.plot(x,fit)
	plt.show()
			
def decodeImage_test(individual,canvas_dim):
	# decodifica l'immagine originariamente presente in individual ora trasformato in un vettore di numeri x
	prev_image = Image.new('RGBA',canvas_dim)
	for i in range(0,len(individual),M):				# ciclo sui numeri che servono per definire tutti i rettangoli
		v = individual[i:i+M]							# M numeri interi che mi servono per definire un rettangolo
		# color = (v[0]%256,v[1]%256,v[2]%256,v[3]%256)	# colore R,G,B,A
		# rect = ((v[4],v[5]),(v[6],v[7]))				# ((x1,y1),(x2,y2))
		color = (v[0]%256,v[1]%256,v[2]%256,128)		# colore R,G,B,A e canale alfa A = 128 (trasparenza 50%)
		rect = ((v[3],v[4]),(v[5],v[6]))				# ((x1,y1),(x2,y2))
		image,rect = SuperImposeNewRectangleRGBA(prev_image,rect,color,canvas_dim)
		prev_image = image
	return prev_image
	
def fitness_test(individual):
	# utilizzando il metodo ColourDistanceSquared della libreria images.py
	# calcola quanto 'fitta' un immagine rispetto a un altra
	# la distanza di colore al quadrato varia fra i valori 8064.6 (=MIN_FITNESS) e 40704.5 (=MAX_FITNESS)
	# se l'immagine di riferimento (target) ha una trasparenza nulla 0% (A = 255)
	# e se l'immagine che approssima il target ha una trasparenza del 50% (A = 128)
	
	test_image = decodeImage_test(individual,(XRES,YRES))
	pixels = test_image.load()	# le due immagini devono avere la stessa dimensione!
	
	F = 0.0	# somma delle distanze
	
	for x,y in itertools.product(range(XRES),range(YRES)):
		F += (MAX_FITNESS - ColourDistanceSquaredRGBA(pixels[x,y],pixels_target[x,y]))/FITNESS_DIFF
				
	return F/AREA	# divido per il numero di punti contenuti nell'area dell'immagine per fare una media delle fitness
	
def objective_test(individual):
	# calcola la fitness rispetto all'obiettivo
	return fitness_test(individual)

def command_line_parser():
	parser = argparse.ArgumentParser(description='Approssima una immagine utilizzando gli algoritmi genetici')
	parser.add_argument("-nrect", help="numero di rettangoli utilizzati per l'approssimazione")
	parser.add_argument("-niter", help="numero massimo di iterazioni/generazioni")
	parser.add_argument("-psize", help="dimensione della popolazione")
	parser.add_argument("-tsize", help="numero di partecipanti alla selezione")
	parser.add_argument("-mrate", help="rateo di mutazione")
	parser.add_argument("-thrsd", help="soglia sotto la quale sostituisce gli individui peggiori con nuovi individui (se zero non fa nulla!)")
	parser.add_argument("-nlist", help="lista a video i primi n individui della popolazione")
	parser.add_argument("-nsave", help="salva il risultato intermedio dell'elaborazione dell'immagine ogni n iterazioni")
	# parser.add_argument("-wdir" , help="work directory ove risiede il file dell'immagine da approssimare")
	parser.add_argument("-tpic" , help="nome del file dell'immagine da approssimare")
	args = parser.parse_args()
	if args.nrect:
		numeroRettangoli = int(args.nrect)
	else:
		numeroRettangoli = 50
	if args.niter:
		maxIterations = int(args.niter)
	else:
		maxIterations = 10
	if args.psize:
		populationSize = int(args.psize)
	else:
		populationSize	= 100
	if args.tsize:
		tournamentSize = int(args.tsize)
	else:
		tournamentSize = 4
	if args.mrate:
		mutationRate = float(args.mrate)
	else:
		mutationRate = 0.25
	if args.thrsd:
		threshold = int(args.thrsd)
	else: 
		threshold = 0
	if args.nlist:
		m = int(args.nlist)
	else: 
		m = 20
	if args.nsave:
		saveEvery = int(args.nsave)
	else:
		saveEvery = maxIterations/10
	if args.tpic:
		fileName = args.tpic
	else:
		fileName = 'C:/Users/admin/Dropbox/images/Monnalisa/Monnalisa_160x200.png'
	targetPicture = os.path.basename(fileName)
	workDir = os.path.dirname(fileName)

	print(f'\nNumero di rettangoli utilizzati: {numeroRettangoli}')
	print(f'Numero massimo di iterazioni: {maxIterations}')
	print(f'Dimensione della popolazione: {populationSize}')
	print(f'Dimensione della selezione: {tournamentSize}')
	print(f'Rateo di mutazione: {mutationRate}')
	print(f'Rimpiazza i peggiori ogni {saveEvery} iterazioni: {threshold==1}')
	print(f'Salva ogni {saveEvery} iterazioni')
	print(f'Immagine da approssimare: \n{fileName}')
	
	if threshold != 0:
		print(f'Rimpiazza i peggiori sotto la soglia di fitness di {threshold}')
	
	return (numeroRettangoli,maxIterations,populationSize,tournamentSize,mutationRate,threshold,m,saveEvery,workDir,targetPicture,fileName)
	
@timer
def main():			  
	#
	# py test-ga-5.py -nrect 200 -niter 100000 -psize 100 -tsize 6 -mrate 0.25 -nsave 100 -tpic C:/Users/massimiliano.cosmell/Dropbox/images/Monnalisa/Monnalisa_160x200.png
		
	randomize()
	numeroRettangoli,maxIterations,populationSize,tournamentSize,mutationRate,threshold,m,saveEvery,workDir,targetPicture,fileName = command_line_parser()
	
	#test 5 - approssimazione di una immagine con 50 rettangoli (ognuno dei quali ha bisogno di 64 bits per essere definito)
	
	global MAX_FITNESS,MIN_FITNESS,FITNESS_DIFF
	MAX_FITNESS = 40704.5 #65025
	MIN_FITNESS = 8064.5
	FITNESS_DIFF = MAX_FITNESS-MIN_FITNESS
	
	global M
	M				= 7								# numeri che mi servono per definire un rettangolo
	alphabet 		= tuple([i for i in range(255)])# sistema piu furbo...
	chromosomeLength = M * numeroRettangoli			# mi servono M numeri per ogni rettangolo da disegnare
	
	global pixels_target
	image_target = Image.open(fileName)				# carica l'immagine target
	image_target.putalpha(255)						# aggiunge/sovrascrive il canale alfa della trasparenza con valore 255 (opaco al 100%)
	pixels_target = image_target.load()				# carica i pixels dell'immagine target
	
	global XRES,YRES,AREA
	XRES,YRES = image_target.size
	AREA = XRES*YRES
	
	# initialize GA:
	population = Simple_GA(populationSize, tournamentSize, mutationRate, alphabet, chromosomeLength, objective_test)
	
	population.newRndPopulation()		# genera gli individui casualmente
	
	# population.printPopulation()
	
	bestFitness	= []
	iteration = 0
	
	while True:
			
		t = time.time()

		population.stepGa()	# fai una iterazione
		
		Punteggio,bestIndividual = population.getResults()
		bestFitness.append(Punteggio)
		
		# ogni tot. iterazioni salva l'immagine che approssima nella maniera migliore l'immagine target e rimpiazza i peggiori individui
		if iteration % saveEvery == 0:
			image = decodeImage_test(bestIndividual,(XRES,YRES))
			image.save(workDir+'ITER_'+str(iteration)+'-POP_'+str(populationSize)+'-RECT_'+str(numeroRettangoli)+'-FIT_'+str(int(10000*bestFitness[iteration])/100)+'__'+targetPicture)
			
			if threshold != 0:
				population.replaceWhorst(threshold)
				
		print(f'ITERATION N.{iteration} Best Fitness is {bestFitness[iteration]} Time elapsed is {int(time.time()-t)} sec.')				
		
		iteration += 1
		
		if iteration == maxIterations:
			maxIterations = iteration
			break
					
	population.savePopulation(workDir + 'population' + '-ITER_'+str(maxIterations) + '.txt')
	plot(maxIterations,bestFitness)
		
if __name__ == "__main__":
	main()
	