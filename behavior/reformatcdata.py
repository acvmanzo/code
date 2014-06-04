# Reformats courtship data.

import libs.courtshiplib as cl
import sys

FNAME = sys.argv[1] # Old file format.
GNAME = sys.argv[2] # New file.

with open(GNAME, 'w') as g:
    
    with open(FNAME) as f:
        f.next()
        for l in f:
            cd = cl.courtshipline(l)
            
            newmovie = '{0}_{1}_c_PF24_x_L.MTS'.format(cd['gen'], cd['date'])
            
            if 'JW' in cd['gen']:
                g.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n'.format(newmovie,\
                'xx.MTS', cd['gen'], cd['offset'], cd['well'], cd['wingm'], \
                cd['wings'], '', 'we', ''))
                
                g.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n'.format(newmovie,\
                'xx.MTS', cd['gen'], cd['offset'], cd['well'], cd['copatt1m'], \
                cd['copatt1s'], '', 'ca', ''))
                
                g.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n'.format(newmovie,\
                'xx.MTS', cd['gen'], cd['offset'], cd['well'], cd['copsucm'], \
                cd['copsucs'], '', 'cs', ''))
            
            if cd['gen'] == 'cg30116':
                g.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n'.format(newmovie,\
                'xx.MTS', 'cg30116-Apr', cd['offset'], cd['well'], cd['wingm'], \
                cd['wings'], '', 'we', ''))
                
                g.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n'.format(newmovie,\
                'xx.MTS', 'cg30116-Apr', cd['offset'], cd['well'], cd['copatt1m'], \
                cd['copatt1s'], '', 'ca', ''))
                
                g.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n'.format(newmovie,\
                'xx.MTS', 'cg30116-Apr', cd['offset'], cd['well'], cd['copsucm'], \
                cd['copsucs'], '', 'cs', ''))
                
            if cd['gen'] == 'fz':
                g.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n'.format(newmovie,\
                'xx.MTS', 'fz-Apr', cd['offset'], cd['well'], cd['wingm'], \
                cd['wings'], '', 'we', ''))
                
                g.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n'.format(newmovie,\
                'xx.MTS', 'fz-Apr', cd['offset'], cd['well'], cd['copatt1m'], \
                cd['copatt1s'], '', 'ca', ''))
                
                g.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n'.format(newmovie,\
                'xx.MTS', 'fz-Apr', cd['offset'], cd['well'], cd['copsucm'], \
                cd['copsucs'], '', 'cs', ''))


            if cd['gen'] == 'cs-Apr':
                g.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n'.format(newmovie,\
                'xx.MTS', cd['gen'], cd['offset'], cd['well'], cd['wingm'], \
                cd['wings'], '', 'we', ''))
                
                g.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n'.format(newmovie,\
                'xx.MTS', cd['gen'], cd['offset'], cd['well'], cd['copatt1m'], \
                cd['copatt1s'], '', 'ca', ''))
                
                g.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n'.format(newmovie,\
                'xx.MTS', cd['gen'], cd['offset'], cd['well'], cd['copsucm'], \
                cd['copsucs'], '', 'cs', ''))


#['date', 'movie', 'offset', 'well', 'gen', 'wingm', 'wings', 'copsucm', 
#'copsucs', 'copatt1m', 'copatt1s']

