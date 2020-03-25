import argparse
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

def infect(nTot, infectionRate):
	from random import shuffle, random
	nInfected = int(nTot * infectionRate)
	infectedIDs = [random()<=infectionRate for _ in range(nTot)]
	assert(len(infectedIDs) == nTot)
	shuffle(infectedIDs)
	return infectedIDs




def main(nIndividuals=1000000, infectionRate=0.1, show=False):
	import testingMachine as tm

	infectedIndividuals = infect(nIndividuals, infectionRate)
	print(np.sum(infectedIndividuals),"infected among ",nIndividuals," :",np.sum(infectedIndividuals)/nIndividuals,"%")
	print()

	tm.applyAllStrategies(infectedIndividuals, [2,3,4,5,6,7,8,9,10,15,20,25,30,40,50,60,70,80,90,100])
	plt.savefig('./results_infected'+str(int(infectionRate*100))+'%.svg', format="svg")
	plt.savefig('./results_infected'+str(int(infectionRate*100))+'%.png', format="png")
	if show:
		plt.show()


if __name__=="__main__":
	parser = argparse.ArgumentParser(description="Computing different tactics of testing covid")
	parser.add_argument('-n','--nIndividuals', type=int, help="number of humans")
	parser.add_argument('-r','--infectionRate', type=float, help="rate of infection")
	parser.add_argument('-s','--show', action='store_true', help="show figure")
	args = {k:v for k,v in vars(parser.parse_args()).items() if v is not None}
	main(**args)