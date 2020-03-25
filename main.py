import os
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




def main(nIndividuals=1000000, show=False):
	import testingMachine as tm
	from tqdm import tqdm


	if not os.path.isfile("./results_all.npz"):
		poolSizes = [2,3,4,5,6,7,8,9,10,12,14,17,20,25,30,40,50,60,70,80,90,100]
		infectionRates = list(np.array([i for i in range(1,30)] + [i for i in range(30,52,2)]) / 100)
		results = []
		for infectionRate in tqdm(infectionRates):
			infectedIndividuals = infect(nIndividuals, infectionRate)

			results.append(tm.applyAllStrategies(infectedIndividuals, poolSizes))
			plt.savefig('./results_infected'+str(int(infectionRate*100))+'%.svg', format="svg")
			plt.savefig('./results_infected'+str(int(infectionRate*100))+'%.png', format="png")
			if show:
				plt.show()
			else:
				plt.close()

		results = np.array(results)
		np.savez("./results_all", results=results, rates=infectionRates, pools=poolSizes)

	else:
		r = np.load("./results_all.npz", allow_pickle=True)
		results = r["results"]
		infectionRates = r["rates"]
		poolSizes = r["pools"]
	print(results.shape)

	stratNames = tm.getStratNames()

	xBoundaries = [(infectionRates[n+1]+infectionRates[n])/2 for n in range(len(infectionRates)-1)]
	xBoundaries = [2*infectionRates[0] - xBoundaries[0]] + xBoundaries + [2*infectionRates[-1] - xBoundaries[-1]]
	yBoundaries = [(poolSizes[n+1]+poolSizes[n])/2 for n in range(len(poolSizes)-1)]
	yBoundaries = [2*poolSizes[0] - yBoundaries[0]] + yBoundaries + [2*poolSizes[-1] - yBoundaries[-1]]

	xBoundaries, yBoundaries = np.meshgrid(xBoundaries, yBoundaries)


	norm = mpl.colors.DivergingNorm(vmin=0, vcenter=nIndividuals, vmax=1.5*nIndividuals)
	for n in range(len(stratNames)):
		plt.figure(figsize=(15,9))
		plt.pcolormesh(xBoundaries, yBoundaries, results[:,n,:].transpose(), cmap="seismic", norm=norm)
		plt.title('number of tests necessary ('+stratNames[n]+')')
		plt.colorbar()
		plt.xlabel('infectionRate')
		plt.ylabel('pool size')
		plt.savefig('./results_all('+stratNames[n]+').svg', format="svg")
		plt.savefig('./results_all('+stratNames[n]+').png', format="png")
	if show:
		plt.show()



if __name__=="__main__":
	parser = argparse.ArgumentParser(description="Computing different tactics of testing covid")
	parser.add_argument('-n','--nIndividuals', type=int, help="number of humans")
	parser.add_argument('-s','--show', action='store_true', help="show figure")
	args = {k:v for k,v in vars(parser.parse_args()).items() if v is not None}
	main(**args)