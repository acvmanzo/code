
from mn.pool_results import *

KEYFILES = ['keyfile_c', 'keyfile_s', 'keyfile_v']
ROIS = [('roi1', 'muscle 12')]

for roi in ROIS:
    p_peakf_file = 'pooled_peakf_{0}.MOD'.format(roi[0])  
    
    for keyfile in KEYFILES:
        sp_key(p_peakf_file, keyfile, keyfile)
        plt.close()
        bg_key(p_peakf_file, keyfile, keyfile)
        plt.close()
