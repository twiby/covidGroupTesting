# covidGroupTesting
group testing of covid-19 would maybe reduce the number of tests needed. To run these computations, if you have python, you can use these commands :
```
pip install -r requirements.txt # optional, to install modules if needed
python main.py # launches actual computation
```
use the "-h" option to learn what other options you can add. The default computations are made on 1,000,000 individuals. Given an infection rate, people are infected according to a binomial law.
If you run the script a second time, it won't recompute everything.

# contribute
To add a new testing strategy, you can add one in testingStrategies.py : add your function to the class testingStrategies to return the result of your tests. Code will fail if your tests made a mistake. 
Don't forget to provide the docstring of your function for its name to appear on the figures automatically.
You can fork the repository, create a branch named after your strat, and create a pull request to merge that branch.
Other PRs are possible, but not really the goal of this project.
