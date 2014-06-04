# Script to extrapolate fruit fly generation times at various temperatures.

import matplotlib.pyplot as plt
import numpy as np

fig1 = plt.figure(figsize=(8, 4), dpi=1000)

temp = [12, 18, 22, 25] # Temp in deg. C
time = [50, 21, 12, 10] # Generation time in days; from personal experience and 
#http://eol.org/pages/733739/details#Life_cycle_and_reproduction 
ltemp, ltime = map(np.log, [temp, time])

ltempA = np.vstack([ltemp, np.ones(len(ltemp))]).T
m,c = np.linalg.lstsq(ltempA, ltime)[0]

time19 = np.exp(m*np.log(19) + c)

ax1 = plt.subplot(121)
plt.scatter(temp, time)
plt.plot(19, time19, 'go')
plt.text(19+1, time19+1, '19, {0:.1f}'.format(time19), color='g')
plt.xlabel('Temp in C')
plt.ylabel('Generation time in days')

ax2 = plt.subplot(122)
plt.scatter(ltemp, ltime)
plt.plot(ltemp, m*ltemp+c, 'r')
plt.xlabel('ln[Temp]')
plt.ylabel('ln[Time]')
plt.text(0.3, 0.8, 'y = {0:.3f}*x+ {1:.3f}'.format(m, c), transform=ax2.transAxes)
plt.plot(np.log(19), np.log(time19), 'go')
plt.tight_layout()

plt.savefig('Gentime_vs_temp')
