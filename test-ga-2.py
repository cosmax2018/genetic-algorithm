
# test-ga-2.py : esegue degli esempi utilizzando la libreria sugli algoritmi genetici

#	(c) Copyright 2020 by ....@_°° Lumachina SW
#    Massimiliano Cosmelli (massimiliano.cosmelli@gmail.com)

import time,sys,random

# from init_lib import *
# add_path_to_lib('genetic algorithms')
from ga import Simple_GA

def randomize(): random.seed(time.time())

def fitness_test(individual,target):
	# valuta la fitness contando quanti caratteri corrispondono nelle due stringhe
	fit = 0
	for i in range(1,len(individual)):
		if individual[i] == target[i-1]:
			fit += 1
	return 100*fit/len(individual)
	
def objective_test(individual):
	# usa il calcolo della fitness appropriato
	target = list('1234000000000000000000000012343210000000000000000000000000004321')
	return fitness_test(individual,target)	

def main(argv):			  
	#		py test-ga-2.py 1000 100 6 0.25 0 20
	randomize()
	try:
		maxIterations = int(argv[0])	# numero massimo di iterazioni/generazioni
		populationSize = int(argv[1])   # dimensione della popolazione
		tournamentSize = int(argv[2])   # numero di partecipanti alla selezione
		mutationRate = float(argv[3])   # rateo di mutazione
		threshold = float(argv[4])		# soglia sotto la quale sostituisc2 gli individui peggiori con nuovi individui (se zero non fa nulla!)
		m = int(argv[5])				# stampa i primi m individui della popolazione
	except IndexError:
		maxIterations	= 1000
		populationSize	= 100
		tournamentSize	= 6
		mutationRate	= 0.25
		threshold		= 0
		m				= 20
	finally:
		print(f'Numero massimo di iterazioni: {maxIterations}')
		print(f'Dimensione della popolazione: {populationSize}')
		print(f'Dimensione della selezione: {tournamentSize}')
		print(f'Rateo di mutazione: {mutationRate}')
		if threshold != 0:
			print(f'Rimpiazza i peggiori sotto la soglia: {threshold}')
	
	alphabet			= list('0123456789')
	target				= list('1234000000000000000000000012343210000000000000000000000000004321')
	chromosomeLength 	= len(target)
	
	population = Simple_GA(populationSize, tournamentSize, mutationRate, alphabet, chromosomeLength, objective_test)	# initialize GA
	population.newRndPopulation()		# genera gli individui casualmente
	
	starttime = time.time()
	population.runGa(maxIterations,threshold,m)
	
	print('That took {} seconds'.format(time.time() - starttime))
	bestFitness,bestIndividual = population.getResults()
	print('Best fitness {}'.format(bestFitness))
		
if __name__ == "__main__":
	main(sys.argv[1:])