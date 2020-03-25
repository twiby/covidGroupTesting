import inspect
import numpy as np
import multiprocessing
import matplotlib as mpl 
import matplotlib.pyplot as plt
import testingStrategies as ts


def pools(data, poolSize):
	if not isinstance(data, list):
		return data
	else:
		for n in range(int(len(data)/poolSize)+1):
			if data[n*poolSize:(n+1)*poolSize] == []:
				continue
			yield data[n*poolSize:(n+1)*poolSize]

class Tests(object):
	def __init__(self):
		self.nTests = 0

	def test(self, pool):
		self.nTests += 1
		if isinstance(pool, (list, np.ndarray)):
			return np.any(pool)
		else:
			return pool



def applyTestingStrategy(strat, infectedIndividuals, poolSize):
	# print("Applying", strat.__doc__,"with pool ",poolSize)
	testingMachine = Tests()
	testedPositive = strat(infectedIndividuals, poolSize, testingMachine)
	assert(np.any([testedPositive[n]!=infectedIndividuals[n] for n in range(len(infectedIndividuals))])==False)
	return testingMachine.nTests

def applyAllStrategies(infectedIndividuals, poolSizes):
	plt.figure(figsize=(15,9))

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
				res += p.starmap(applyTestingStrategy, ((strat, infectedIndividuals, poolSize) for poolSize in group))
		results.append(res)
		p = plt.plot(poolSizes, res, label=strat.__doc__+" (min: "+str(poolSizes[np.argmin(res)])+")")
	plt.xlabel("poolSize")
	plt.ylabel("number of tests performed")
	plt.title("different pooling strategies tried to reduce total number of tests (infection rate "+str(np.sum(infectedIndividuals)/len(infectedIndividuals)*100)+"%)")
	plt.legend(loc="lower right")

	return results

def getStratNames():
	return [strat.__doc__ for strat in ts.getAllStrats()]