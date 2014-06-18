
#SAMFILE = 'accepted_hits_2_short.sam'
SAMFILE = 'accepted_hits_2.sam'
NH1FILE = 'nh=1.txt'
NHMFILE = 'nhm1.txt'
LOWMQFILE = 'lowmq.txt'

def parse_nh():
    
    uniq_align = 0
    multi_align = 0
    with open(SAMFILE, 'r') as f:
        for l in f:
            nhval = int(l[l.find('NH:i:')+5])
            if nhval > 1:
                multi_align += 1
                with open(NHMFILE, 'a') as g:
                    g.write(l)
            if nhval == 1:
                uniq_align += 1
                #with open(NH1FILE, 'a') as g:
                    #g.write(l)

    print('unique', uniq_align)
    print('multi', multi_align)

def parse_mapq():
    low_qual_reads = 0
    with open(SAMFILE, 'r') as f:
        for l in f:
            mapq = int(l.split('\t')[4])
            if mapq < 10:
                low_qual_reads +=1
                with open(LOWMQFILE, 'a') as g:
                    g.write(l)
    print('low quality reads', low_qual_reads)


def parse_nh_mapq():

    low_mapq_nh1_reads = 0
    high_mapq_nhmore_reads = 0
    with open(SAMFILE, 'r') as f:
        for l in f:
            mapq = int(l.split('\t')[4])
            nhval = int(l[l.find('NH:i:')+5])
            
            if mapq < 10 and nhval == 1:
                low_mapq_nh1_reads +=1
            if mapq > 10 and nhval > 1:
                high_mapq_nhmore_reads +=1

    print('(low quality) mapq < 10, but nh =1', low_mapq_nh1_reads)
    print('(high quality) mapq > 10, but nh > 1', high_mapq_nhmore_reads)


def main():
    parse_mapq()

if __name__ == '__main__':
   main() 
