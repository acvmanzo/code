
#SAMFILE = 'accepted_hits_2_short.sam'
SAMFILE = 'accepted_hits_2.sam'


uniq_align = 0
multi_align = 0
with open(SAMFILE, 'r') as f:
    for l in f:
        nhval = int(l[l.find('NH:i:')+5])
        if nhval > 1:
            multi_align += 1
        if nhval == 1:
            uniq_align += 1

print('unique', uniq_align)
print('multi', multi_align)
