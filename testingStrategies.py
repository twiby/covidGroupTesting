import inspect
import numpy as np

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
		if isinstance(pool, list):
			return np.any(pool)
		else:
			return pool


def applyTestingStrategy(strat, infectedIndividuals, poolSize):
	print("Applying", strat.__doc__,":")
	testedPositive = []; testingMachine = Tests()
	for p in pools(infectedIndividuals, poolSize):
		testedPositive += strat(p, testingMachine)
	assert(np.any([testedPositive[n]!=infectedIndividuals[n] for n in range(len(infectedIndividuals))])==False)
	print("done in ", testingMachine.nTests, "tests (", testingMachine.nTests/len(infectedIndividuals)*100,"%)")
	print()


class testingStrategies:

	def individualTesting(pool, testM):
		'''individual testing'''
		return [testM.test(i) for i in pool]

	def simplePoolTesting(pool, testM):
		'''simple pool testing'''
		res = testM.test(pool)
		if res == False:
			return [False for _ in pool]
		else:
			return [testM.test(i) for i in pool]

def getAllStrats():
	return [getattr(testingStrategies,func) for func in dir(testingStrategies) if callable(getattr(testingStrategies, func)) and not func.startswith("__")]