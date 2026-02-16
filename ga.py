
# ga.py : simple GA v.2 written in Python (slow version)
#
#	(c) Copyright 2020-21 by ....@_°° Lumachina SW
#    Massimiliano Cosmelli (massimiliano.cosmelli@gmail.com)

from population import Population
# from population_multiprocessing import Population	# multi-processes version. (anche se riesce a saturare tutti i cores della cpu sembra molto più lenta della versione non multiprocessing)
import time

def timer(function):						# prende come parametro la funzione di cui misurare il tempo di esecuzione
	def timed(*args):						# args sono i parametri passati alla funzione da misurare
		start_time = time.time()			# Ti
		result = function(*args)			# esegue la funzione
		elapsed = time.time() - start_time	# Tf
		print('Function "{name}" took {time} seconds to complete.'.format(name=function.__name__, time=elapsed))
		return result						# restituisce il risultato dell'esecuzione della funzione
	return timed
	
class Simple_GA:
	# classe di inizializzazione o costruttore
	def __init__(self,populationSize, tournamentSize, mutationRate, alphabet, chromosomeLength, objectiveFunction):
        # ------------------------------------------
        self.maxIterations      = 1000
        self.threshold          = 0
        self.printEvery         = 20
		self.replaceEvery		= 100
        # ------------------------------------------
		self.populationSize		= populationSize
		self.tournamentSize		= tournamentSize
		self.mutationRate		= mutationRate
		self.alphabet 			= alphabet
		self.chromosomeLength	= chromosomeLength
		self.objectiveFunction	= objectiveFunction
		# ------------------------------------------
		self.population			= Population(populationSize,tournamentSize,mutationRate,alphabet,chromosomeLength,objectiveFunction)	# una popolazione di individui

	def getResults(self):				return self.population.getResults()
    
    def setMaxIterations(self,maxIter): self.maxIterations = maxIter
    
    def getMaxIterations(self):         return self.maxIterations
    
    def setThreshold(self,value):       self.threshold = value
    
    def getThreshold(self):             return self.threshold
    
    def setPrintEvery(self,m):          self.printEvery = m
    
    def getPrintEvery(self):            return self.printEvery
    
    def setReplaceEvery(self,n):        self.replaceEvery = n
    
    def getReplaceEvery(self):          return self.replaceEvery
	
	def savePopulation(self,file_name):	return self.population.savePopulation(file_name)	
	
	def loadPopulation(self,file_name):	return self.population.loadPopulation(file_name)
	
	def replaceWhorst(self,threshold):	return self.population.replaceWhorst(threshold)
	
	def newRndPopulation(self):			return self.population.rndPopulation()
	
	def sortPopulation(self):			return self.population.sortPopulation()
	
	def evaluatePopulation(self):		return self.population.evaluatePopulation()
	
	def mutatePopulation(self):			return self.population.mutatePopulation()
	
	def evolvePopulation(self):			return self.population.evolvePopulation()
	
	def printPopulation(self,n=None):	return self.population.printPopulation(n)
	
	def evaluate_thread(self):			self.population.evaluatePopulation()	# evaluating population fitness
	
	def sort_thread(self):				self.population.sortPopulation()		# sorting population by fitness
	
	def evolve_thread(self):			self.population.evolvePopulation()		# evolving population
	
	def mutate_thread(self):			self.population.mutatePopulation()		# mutating population		

	def stepGa(self):															# execute one single step
		
		self.population.evaluatePopulation()

		self.population.sortPopulation()

		self.population.evolvePopulation()

		self.population.mutatePopulation()
		
	@timer
	def runGa(self):
		# esegue l'algoritmo genetico
		
		print("\033[1;1HITERATION: ")
		
		# the iterations
		for iterations in range(self.maxIterations):
			
			print("\033[1;12H" + str(iterations))
			
			self.stepGa()
			
			self.population.printPopulation(self.printEvery)		 # stampa i primi individui della popolazione
			
			if iterations % self.replaceEvery == 0: # ogni tot. iterazioni rimpiazza gli individui con fitness < fitness minima (Es threshold = 30) con nuovi individui creati a caso
				if self.threshold != 0:
					self.population.replaceWhorst(self.threshold)
					