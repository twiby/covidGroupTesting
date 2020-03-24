import argparse
import numpy as np
import testingStrategies as ts

def infect(nTot, infectionRate):
	from random import shuffle, random
	nInfected = int(nTot * infectionRate)
	infectedIDs = [random()<=infectionRate for _ in range(nTot)]
	assert(len(infectedIDs) == nTot)
	shuffle(infectedIDs)
	return infectedIDs




def main(nIndividuals=1000000, infectionRate=0.1, poolSize=20):

	infectedIndividuals = infect(nIndividuals, infectionRate)
	print(np.sum(infectedIndividuals),"infected among ",nIndividuals," :",np.sum(infectedIndividuals)/nIndividuals,"%")
	print()

	for strat in ts.getAllStrats():
		ts.applyTestingStrategy(strat, infectedIndividuals, poolSize)



if __name__=="__main__":
	parser = argparse.ArgumentParser(description="Computing different tactics of testing covid")
	parser.add_argument('-n','--nIndividuals', type=int, help="number of humans")
	parser.add_argument('-r','--infectionRate', type=float, help="rate of infection")
	parser.add_argument('-p','--poolSize', type=int, help="size of pools of human")
	args = {k:v for k,v in vars(parser.parse_args()).items() if v is not None}
	main(**args)