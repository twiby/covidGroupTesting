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




def main(args):
	if args.nIndividuals:
		nIndividuals = args.nIndividuals
	else:
		nIndividuals = 1000000
	if args.infectionRate:
		rateInfected = infectionRate
	else:
		rateInfected = 0.1
	if args.poolSize:
		poolSize = args.poolSize
	else:
		poolSize = 20

	infectedIndividuals = infect(nIndividuals, rateInfected)
	print(np.sum(infectedIndividuals),"infected among ",nIndividuals," :",np.sum(infectedIndividuals)/nIndividuals,"%")
	print()

	for strat in ts.getAllStrats():
		ts.applyTestingStrategy(strat, infectedIndividuals, poolSize)



if __name__=="__main__":
	parser = argparse.ArgumentParser(description="Computing different tactics of testing covid")
	parser.add_argument('--nIndividuals', type=int, help="number of humans")
	parser.add_argument('--infectionRate', action='store_true', help="rate of infection")
	parser.add_argument('--poolSize', action='store_true', help="size of pools of human")
	args = parser.parse_args()
	main(args)