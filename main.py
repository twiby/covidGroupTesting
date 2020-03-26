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




def main(nIndividuals=1000000, show=False, build=False):
	import testingMachine as tm
	from tqdm import tqdm


	if not os.path.isfile("./results_all.npz") or build:
		poolSizes = [2,3,4,5,6,7,8,9,10,12,14,17,20,25,30,40,50,60,70,80,90,100]
		infectionRates = list(np.array([i for i in range(1,30)] + [i for i in range(30,52,2)]) / 100)
		results = []

		pbar = tqdm(total=len(infectionRates)*len(poolSizes)*len(tm.getStratNames()))
		for infectionRate in infectionRates:
			infectedIndividuals = infect(nIndividuals, infectionRate)

			results.append(tm.applyAllStrategies(infectedIndividuals, poolSizes, pbar=pbar))
			plt.savefig('./results_infected'+str(int(infectionRate*100))+'%.svg', format="svg")
			plt.savefig('./results_infected'+str(int(infectionRate*100))+'%.png', format="png")
			if show:
				plt.show()
			else:
				plt.close()
		pbar.close()
		results = np.array(results)
		np.savez("./results_all", results=results, rates=infectionRates, pools=poolSizes)

	else:
		r = np.load("./results_all.npz", allow_pickle=True)
		results = r["results"]
		infectionRates = r["rates"]
		poolSizes = r["pools"]

	stratNames = tm.getStratNames()


	### Color plots
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
		cbar = plt.colorbar()
		cbar.set_label('relative number of tests compared to individual testing', rotation=270, labelpad=20)
		plt.xlabel('infectionRate')
		plt.ylabel('pool size')
		plt.savefig('./results_all('+stratNames[n]+').svg', format="svg")
		plt.savefig('./results_all('+stratNames[n]+').png', format="png")
	if show:
		plt.show()
	else:
		plt.close()


	### Optimal pool size plot
	fontsize=20
	fig = plt.figure(figsize=(15,15))
	fig.add_subplot(211)
	for n in range(len(stratNames)):
		plt.plot(infectionRates, [poolSizes[np.argmin(results[r,n,:])] if np.min(results[r,n,:])<nIndividuals else 1 for r in range(len(infectionRates))], label=stratNames[n])
	plt.title("optimal pool size", fontsize=fontsize)
	plt.ylabel("optimal pool size")
	plt.legend(loc="upper right")

	fig.add_subplot(212)
	for n in range(len(stratNames)):
		plt.plot(infectionRates, [np.min(results[r,n,:])/nIndividuals if np.min(results[r,n,:])<nIndividuals else 1 for r in range(len(infectionRates))], label=stratNames[n])
	plt.title("Number of tests needed with optimal pool size", fontsize=fontsize)
	plt.xlabel("infection rate")
	plt.ylabel("number of tests")
	plt.legend(loc="lower right")
	plt.savefig('./results_optimalPoolSize.svg', format="svg")
	plt.savefig('./results_optimalPoolSize.png', format="png")
	if show:
		plt.show()
	else:
		plt.close()


if __name__=="__main__":
	parser = argparse.ArgumentParser(description="Computing different tactics of testing covid")
	parser.add_argument('-n','--nIndividuals', type=int, help="number of humans")
	parser.add_argument('-s','--show', action='store_true', help="show figure")
	parser.add_argument('-b','--build', action='store_true', help="rebuild results")
	args = {k:v for k,v in vars(parser.parse_args()).items() if v is not None}
	main(**args)