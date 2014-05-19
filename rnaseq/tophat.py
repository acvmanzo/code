import sys
import os
import glob
import cmn.cmn as cmn


#cat NA10831_ATCACG_L002_R1_001.fastq.gz NA10831_ATCACG_L002_R1_002.fastq.gz > NA10831_ATCACG_L002_R1_combined.fastq.gz

#RESULTS_BASE_DIR = '/home/andrea/rnaseqanalyze/analysis'
RESULTS_BASE_DIR = '/home/andrea/Documents/lab/RNAseq/results'
R57GFF = '/home/andrea/rnaseqanalyze/references/dmel-all-filtered-r5.57.gff'
R57MITOGFF = '/home/andrea/rnaseqanalyze/references/dmel-dmel_mitochondrion_genome-r5.57.gff'
BTINDEX = '/home/andrea/rnaseqanalyze/references/dmel-all-chromosome-r5.57'

def get_dirs(folder, globstring):
    
    os.chdir(folder)
    dirs = [os.path.abspath(x) for x in sorted(glob.glob('{0}'.format(globstring)))]
    return(dirs)

def get_exptdirs(seqbase):
    exptdirs = get_dirs(seqbase, '2014-*/')
    return(exptdirs)

def get_sampledirs(exptdir):
    seqdir = os.path.join(exptdir, 'sequences')
    sampledirs = get_dirs(seqdir, 'Sample_*') 
    return(sampledirs)

def gen_combined_gzfile(sampledir, results_base_dir):
    '''
    Input:
    sampledir = contains sequence files and has the name 'Sample_RGxx0xxx'
    '''
    samplename = os.path.basename(sampledir).split('_')[1]
    results_dir = os.path.join(results_base_dir, samplename)
    cmn.makenewdir(results_dir)

    gzfiles = ' '.join(sorted(glob.glob('*[0-9].fastq.gz')))
    #print(gzfiles)
    combined_gzpath = os.path.join(results_dir, '{}_combined.fastq.gz'.format(samplename))
    #print(os.path.exists(combined_gzpath))
    print(combined_gzpath)
    if not os.path.exists(combined_gzpath):
        catcmd = 'cat {} > {}'.format(gzfiles, combined_gzpath)
        print('Generating {}'.format(os.path.basename(combined_gzpath)))
        os.system(catcmd)
    else:
        print('{} exists'.format(combined_gzpath))
    return(combined_gzpath)

def unzip_gzfile(gzfile):
    uzfile = gzfile.strip('.gz')
    if not os.path.exists(uzfile):
        print('Unzipping {0}'.format(os.path.basename(gzfile)))
        os.system('gunzip {}'.format(gzfile))
    else:
        print('Unzipped {0} exists'.format(uzfile))


def mgen_combined_gzfile(sampledirs, results_base_dir):
    for sd in sampledirs:
        os.chdir(sd)
        combined_gzpath = gen_combined_gzfile(sd, results_base_dir)

def run_tophat(fastafile):
    tophatcmd = 'tophat -p 5 --no-coverage-search -G {0} {1} {2}'.format(R57GFF, BTINDEX, fastafile)
    print(tophatcmd)
    os.system(tophatcmd)
    with open('tophat.info', 'w') as f:
        f.write(tophatcmd)




def run_cufflinks(bamfile):
    cufflinkscmd = 'cufflinks -o cufflinks_out -p 8 -M /home/andrea/rnaseqanalyze/references/dmel-dmel_mitochondrion_genome-r5.57.gff -G /home/andrea/rnaseqanalyze/references/dmel-all-filtered-r5.57.gff -u {0} 2>&1 cufflinkslog.info'.format(bamfile)
    print(cufflinkscmd)
    with open('cufflinks.info', 'w') as f:
        f.write(cufflinkscmd)
    os.system(cufflinkscmd)

def batch_tophat():



seqbase = '/home/andrea/Documents/lab/RNAseq/sequences'
exptdirs = get_exptdirs(seqbase)
#print('extpdirs', exptdirs)
#for ed in exptdirs:
    #try:
        #seqsampledirs = get_sampledirs(ed)
        ##print('seqsampledirs', seqsampledirs)
    #except FileNotFoundError:
        #print('sequence folder does not exist')
        #continue
    #mgen_unzip_combined_gzfile(seqsampledirs, RESULTS_BASE_DIR)


os.chdir(RESULTS_BASE_DIR)
sampledirs = get_dirs('.', 'RG*')

#print(sampledirs)
for sd in sampledirs:
    #print(os.path.basename(sd))
    os.chdir(sd)
    print(sd)
    #if os.path.exists('tophat_out'):
        #print('tophat_out directory exists')
        #continue
    #fastafile = glob.glob('*combined.fastq')[0]
    #print(fastafile)
    #run_tophat(fastafile)
    #os.remove(fastafile)

    if os.path.exists('cufflinks_out'):
        print('cufflinks_out directory exists')
        continue
    bamfile = 'tophat_out/accepted_hits.bam'
    run_cufflinks(bamfile) 
    #fastafile = glob.glob('*combined.fastq')[0]
    #print(fastafile)
    #run_tophat(fastafile)t
    #os.remove(fastafile)
