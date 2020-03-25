import inspect
import numpy as np
import testingMachine as tm

### infectedIndividuals is a list of booleans (True for infected, False for sain)
### you MUST test with testM, as this will count the number of tests automatically
### testM.test(arg) will return True if any among arg is infected, False otherwise
### a pooling generator is available : tm.pools(individuals, poolSize)

class testingStrategies:
	def individualTesting(infectedIndividuals, poolSize, testM):
		'''individual testing'''
		res = []
		for p in tm.pools(infectedIndividuals, poolSize):
			res += [testM.test(i) for i in p]
		return res

	def simplePoolTesting(infectedIndividuals, poolSize, testM):
		'''simple pool testing'''
		res = []
		for p in tm.pools(infectedIndividuals, poolSize):
			if testM.test(p):
				res += [testM.test(i) for i in p]
			else:
				res += [False for _ in p]
		return res

	def squarePoolTesting(infectedIndividuals, poolSize, testM):
		'''2d pool testing'''
		res = []
		for p in tm.pools(infectedIndividuals, poolSize**2):
			if len(p)!=poolSize**2:
				res += testingStrategies.simplePoolTesting(p, poolSize, testM)
				continue
			temp = np.zeros([poolSize, poolSize])
			p = np.array(p).reshape([poolSize, poolSize])
			xResults = [testM.test(p[x,:]) for x in range(poolSize)]
			yResults = [testM.test(p[:,y]) for y in range(poolSize)]
			if np.sum(xResults)==1 or np.sum(yResults)==1:
				for x in range(poolSize):
					for y in range(poolSize):
						temp[x,y] = xResults[x] and yResults[y]
			else:
				for x in range(poolSize):
					for y in range(poolSize):
						if xResults[x] and yResults[y]:
							temp[x,y] = testM.test(p[x,y])
			res += list(temp.reshape([poolSize**2]))
		return res



def getAllStrats():
	return [getattr(testingStrategies,func) for func in dir(testingStrategies) if callable(getattr(testingStrategies, func)) and not func.startswith("__")]

