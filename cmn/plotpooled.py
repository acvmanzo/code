#! /usr/bin/env python
from genplotlib import *


# Keys
K = ['112648-GAL4', 'UAS-TNT', '112648 x TNT']
#K = ['113990-GAL4', 'UAS-TNT', '113990 x TNT']
#K = ['0% MC', '1.5% MC', '2% MC', '2.5% MC', '3% MC']




# Plotting pooled capillary data.
from pcapm import *

#d = gendictnps('capdata.txt')
#md = genlist(d)
#plotdata(d, md, K, 's', 'nL', 'Amount consumed', ylim=10)
#plt.savefig('capdata_nl')

# Plotting pooled pump frequency data.


# Plot fraction of flies with functional muscle 12.

#genfilepercent('peakf_roi2_pooled_all.txt', 'peakf_roi2_pooled_all_percent.txt')
#genfilepercent('peakf_roi1_pooled_all.txt', 'peakf_roi1_pooled_all_percent.txt')

#d = gendict('peakf_roi1_pooled_all_percent.txt')
#md = genlist(d)
#plotdata(d, md, K, 'b', '', 'Fraction of flies with functional muscle 12', ylim=1.25, err='none')

#plt.figure()
#d = gendict('peakf_roi2_pooled_all_percent.txt')
#md = genlist(d)
#plotdata(d, md, K, 'b', '', 'Fraction of flies with functional muscle 11', ylim=1.25, err='none')

# Plot average pump frequency of all flies.

#plt.show()
#plt.figure()
#d = gendict('peakf_roi1_pooled_all.txt')
#md = genlist(d)
#plotdata(d, md, K, 's', 'Hz', 'Pumping frequency of muscle 12', ylim=8)
#plt.show()

# Plot average pump frequency with non-pumpers removed.

#removezerovalues('peakf_roi1_pooled_all.txt', 'peakf_roi1_pooled_pumpersonly.txt')
#removezerovalues('peakf_roi2_pooled_all.txt', 'peakf_roi2_pooled_pumpersonly.txt')

#d = gendict('peakf_roi1_pooled_pumpersonly.txt')
#md = genlist(d)
#plotdata(d, md, K, 's', '', 'Pumping frequency of flies with functional muscle 12', ylim=8)
#plt.savefig('peakf_roi1_pooled_pumpersonly')

#plt.figure()
#d = gendict('peakf_roi2_pooled_pumpersonly.txt')
#md = genlist(d)
#plotdata(d, md, K, 's', '', 'Pumping frequency of flies with functional muscle 11', ylim=8)
#plt.savefig('peakf_roi2_pooled_pumpersonly')

#plt.show()


# Plots phase data.

from peaklib import *

NBIN, XMIN, XMAX, TIMEBIN, PHASEBIN = HISTPLOTPARAMS

# Keys
#K = ['112648-GAL4', 'UAS-TNT', '112648 x TNT']
#K = ['113990-GAL4', 'UAS-TNT', '113990 x TNT']

FOLDERS = ['/home/andrea/Documents/lab/motor_neurons/lof/2010-1201_tnt_113990/phase_analysis/ifiles/', 
    '/home/andrea/Documents/lab/motor_neurons/lof/2010-1210_tnt/phase_analysis/ifiles/']

#FOLDERS = ['/home/andrea/Documents/lab/motor_neurons/lof/2010-1130_tnt/phase_analysis/ifiles/', 
    #'/home/andrea/Documents/lab/motor_neurons/lof/2010-1213_tnt/phase_analysis/ifiles/']

# Run from folders where the files exist.
plotandsavephasefreq(K, 'pooled_deltaphase_summ')
#plot_avgdeltatime_cycle(K, 'pooled_deltatime_1cycle_summ', ymin=0, ylim=0.4)
##plotandsavephase(K, TIME_CUTOFF, 'pooled_deltaphase_summ') # See other method below.

#o = os.getcwd() + '/'
#histdeltaphase_pool_expts(FOLDERS, PHASEBIN, o)
#plt.show()
#histdeltatime_pool_expts(FOLDERS, TIMEBIN)
#plt.show()
#plotphasefigs_poolexpts(FOLDERS, K)
#plt.show()

