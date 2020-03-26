import inspect
import numpy as np
import multiprocessing
import matplotlib as mpl 
import matplotlib.pyplot as plt
import testingStrategies as ts
from random import random

def pools(data, poolSize):
	if not isinstance(data, list):
		return data
	else:
		for n in range(int(len(data)/poolSize)+1):
			if data[n*poolSize:(n+1)*poolSize] == []:
				continue
			yield data[n*poolSize:(n+1)*poolSize]

class Tests(object):
	def __init__(self, falseNegativeRate=0):
		self.nTests = 0
		self.falseNegativeRate = falseNegativeRate
		if self.falseNegativeRate > 0:
			self.testErrors = True
		else:
			self.testErrors = False

	def test(self, pool):
		self.nTests += 1
		if self.testErrors:
			if random() < self.falseNegativeRate:
				return False

		if isinstance(pool, (list, np.ndarray)):
			return np.any(pool)
		else:
			return pool


def getStratErrorRate(strat, infectedIndividuals, poolSize, falseNegativeRate):
	# print("testing error of ", strat.__doc__,"with pool ",poolSize)
	testingMachine = Tests(falseNegativeRate=falseNegativeRate)
	testedPositive = strat(infectedIndividuals, poolSize, testingMachine)
	return np.sum([testedPositive[n]!=infectedIndividuals[n] for n in range(len(infectedIndividuals))])


def getStratTestCount(strat, infectedIndividuals, poolSize, *args):
	# print("Applying", strat.__doc__,"with pool ",poolSize)
	testingMachine = Tests()
	testedPositive = strat(infectedIndividuals, poolSize, testingMachine)
	assert(np.any([testedPositive[n]!=infectedIndividuals[n] for n in range(len(infectedIndividuals))])==False)
	return testingMachine.nTests

def applyAllStrategies(infectedIndividuals, poolSizes, pbar=None, falseNegativeRate=None):
	plt.figure(figsize=(15,9))

	if falseNegativeRate!=None:
		mode = getStratErrorRate
	else:
		mode = getStratTestCount

	results = []
	for strat in ts.getAllStrats():
		res = []
		nCoresAvailable = multiprocessing.cpu_count()
		groupedPoolSizes = [
			[poolSizes[pool*nCoresAvailable + group ]
			for group in range(min(nCoresAvailable, len(poolSizes)-pool*nCoresAvailable))]
			for pool in range(len(poolSizes)//nCoresAvailable+1)]

		for group in groupedPoolSizes:
			if group == []:
				continue
			with multiprocessing.Pool(len(group)) as p:
				res += p.starmap(mode, ((strat, infectedIndividuals, poolSize, falseNegativeRate) for poolSize in group))
			if pbar:
				pbar.update(len(group))
		results.append(res)
		p = plt.plot(poolSizes, np.array(res)/len(infectedIndividuals), label=strat.__doc__+" (min: "+str(poolSizes[np.argmin(res)])+")")
	plt.legend(loc="lower right")

	return results

def getStratNames():
	return [strat.__doc__ for strat in ts.getAllStrats()]