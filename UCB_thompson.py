import pandas as pd
import matplotlib.pyplot as plt
import math
import random
from sys import argv

#Usage: UCB_thompson.py rounds ads
#Examp: UCB_thompson.py 10000 10

try:
    N = int(argv[1])
except IndexError:
    N = 500
try:
    d = int(argv[2])
except IndexError:
    d = 10

dataset = pd.read_csv('ads_simulation.csv')

ads_selected_UCB = []
ads_selected_thompson = []
random.seed(0)

#UCB
numbers_of_selections = [0] * d
sums_of_rewards = [0] * d
for n in range(N):
    ad = 0
    max_upper_bound = 0
    for i in range(d):
     if numbers_of_selections[i] != 0:
         average_reward = sums_of_rewards[i]/float(numbers_of_selections[i])
         delta_i = math.sqrt(3/2.0 * math.log(n+1.0)/numbers_of_selections[i])
         upper_bound = delta_i + average_reward
     else:
         upper_bound = 1e400
     if max_upper_bound < upper_bound:
         max_upper_bound = upper_bound
         ad = i
    ads_selected_UCB.append(ad)
    numbers_of_selections[ad] += 1
    sums_of_rewards[ad] += dataset.values[n,ad]

#Thompson
numbers_of_rewards_1 = [0]*d
numbers_of_rewards_0 = [0]*d
for n in range(N):
    ad = 0
    max_random = 0
    for i in range(d):
        theta = random.betavariate(float(numbers_of_rewards_1[i]+1), float(numbers_of_rewards_0[i]+1))
        if max_random < theta:
            max_random = theta
            ad = i
    ads_selected_thompson.append(ad)
    if dataset.values[n,ad] == 1:
        numbers_of_rewards_1[ad] += 1
    else:
        numbers_of_rewards_0[ad] += 1

fig, ax = plt.subplots(1,2,figsize=(12,6))
ax1 = plt.subplot(1,2,1)
plt.hist(ads_selected_UCB)
plt.title('UCB Algorith')
plt.xlabel('Ad number')
plt.ylabel('Times selected')

ax2 = plt.subplot(1,2,2)
plt.hist(ads_selected_thompson)
plt.title('Thompson Sampling Algorithm')
plt.xlabel('Ad number')
plt.ylabel('Times selected')

plt.show()
plt.close()
