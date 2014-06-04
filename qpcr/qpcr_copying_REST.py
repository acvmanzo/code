
#This script is written to generate the expression ratio as performed in REST.
#Basically, it takes each paired set of c_ref and c_goi values and calculates
#the expression ratio using each paired set of m_ref and m_goi values. This
#bootstrapping method generates a distribution of expression ratios, with the
#median expression as the reported ratio. A 95% CI is also generated by finding
#the minimum and maximum ratios that encompass 95% of all the points.

import math
import numpy as np

e_ref = 1.995
e_goi = 1.968

c_refs = [16.77, 16.85, 16.72, 16.63, 16.72, 16.73, 16.64, 16.54, 16.57]
c_gois = [18.83, 18.84, 18.79, 18.49, 18.57, 18.46, 18.4, 18.56, 18.45]

m_refs = [17.09, 17.11, 17.06, 16.57, 16.47, 16.44, 16.63, 16.59, 16.42]
m_gois = [20.1, 20.08, 19.97, 19.68, 19.61, 19.52, 19.95, 19.92, 19.72]

c = zip(c_refs, c_gois)
m = zip(m_refs, m_gois)
#e_ref = 2
#e_goi = 2

#c_goi = 18
#m_goi = 17

#c_ref = 17
#m_ref = 17
ratios = []
for crg in c:
    c_ref = crg[0]
    c_goi = crg[1]
    for mrg in m:
        m_ref = mrg[0]
        m_goi = mrg[1]
        ratio = (e_goi**(c_goi - m_goi))/(e_ref**(c_ref - m_ref))
        ratios.append(ratio)

r = sorted(ratios)
lower95ci =  r[int(np.floor(0.05/2*len(r)))]
upper95ci = r[int(np.floor(1-(0.05/2)*len(r)))]

print 'lower95', lower95ci
print 'upper95', upper95ci
print 'median',  np.median(ratios)
