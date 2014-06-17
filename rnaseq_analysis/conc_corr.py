#Plots a scatter plot of rna concentration and qubit values; finds Pearson 
#correlation coefficient.

import numpy as np
import psycopg2
import scipy.stats as stats
import matplotlib.pyplot as plt
import correlationlib as cl

conn = psycopg2.connect("dbname=rnaseq user=andrea")
cur = conn.cursor()

cur.execute("select rnaconc, qbitngul from autin where qbitngul is not Null order by samplenum;")
results = cur.fetchall()
rnac, qbit = zip(*results)
print(rnac)
print(qbit)

cur.close()
conn.close()

slope, intercept, r, p, std_err = stats.linregress(rnac, qbit)
print(np.square(r))

xline = np.arange(np.ceil(np.max((rnac))))
yline = [slope*x + intercept for x in xline] 
plt.plot(rnac, qbit, 'o')
plt.plot(xline, yline, c='b', ls = '--', label='Reg line')
plt.xlabel('RNA (ng/uL)')
plt.ylabel('Qubit (ng/uL)')
plt.title('R^2 = {:.2f}'.format(np.square(r)))
plt.savefig('rna_vs_qubit.png')

 
