import numpy as np

def infect(nTot, infectionRate):
	from random import shuffle, random
	nInfected = int(nTot * infectionRate)
	infectedIDs = [random()<=infectionRate for _ in range(nTot)]
	assert(len(infectedIDs) == nTot)
	shuffle(infectedIDs)
	return infectedIDs

class Tests(object):
	def __init__(self):
		self.nTests = 0

	def test(self, pool):
		self.nTests += 1
		if isinstance(pool, list):
			return np.any(pool)
		else:
			return pool


def main():
	nIndividuals = 100000
	rateInfected = 0.1
	poolSize = 20

	infectedIndividuals = infect(nIndividuals, rateInfected)
	print(np.sum(infectedIndividuals),"infected among ",nIndividuals," :",np.sum(infectedIndividuals)/nIndividuals,"%")
	print()

	print("Individual testing strategy :")
	testedPositive = []; testingMachine = Tests()
	for i in infectedIndividuals:
		testedPositive.append(testingMachine.test(i))
	assert(np.any([testedPositive[n]!=infectedIndividuals[n] for n in range(nIndividuals)])==False)
	print("done in ", testingMachine.nTests, "tests")



if __name__=="__main__":
	main()